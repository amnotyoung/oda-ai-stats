"""
OECD CRS 구조를 모사한 강의용 합성 데이터 생성기.

실제 CRS(Creditor Reporting System) 마이크로데이터의 핵심 구조를 본떠,
강의에서 다루는 모든 분석(교차표·t검정·ANOVA·회귀·패널 고정효과·텍스트 분석)이
의미 있는 신호를 내도록 설계했다. 실제 원조액이 아니라 교육용 가상 데이터다.

재현성: 시드 고정(42). 다시 돌리면 항상 같은 데이터가 나온다.
출력: ../data/sample_crs.csv  (USD 백만 단위, 인구 백만 명 단위)
"""
import os
import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data", "sample_crs.csv")

# ── 1. 마스터 차원 ────────────────────────────────────────────────────────────
DONORS = {  # 공여국: (규모 배율)
    "Korea": 0.9, "Japan": 1.3, "United States": 1.6,
    "Germany": 1.2, "France": 1.0, "United Kingdom": 1.1,
}
# 수원국: (1인당 GDP USD, 인구 백만)  — 빈곤할수록 1인당 원조 ↑ 가 되도록 신호 설계
RECIPIENTS = {
    "Ethiopia": (925, 120.0), "Tanzania": (1100, 63.0), "Kenya": (2080, 53.0),
    "Bangladesh": (2460, 167.0), "Nepal": (1340, 30.0), "Cambodia": (1620, 16.5),
    "Vietnam": (4160, 97.0), "Ghana": (2360, 32.0), "Peru": (6690, 33.0),
    "Bolivia": (3550, 11.8),
}
SECTORS = {  # 분야: (규모 배율, 대출 성향[0~1])  — 인프라는 크고 대출 많음
    "Health": (0.8, 0.10), "Education": (0.7, 0.10),
    "Water & Sanitation": (0.9, 0.25), "Agriculture": (0.8, 0.20),
    "Transport Infrastructure": (1.8, 0.70), "Governance": (0.5, 0.05),
}
YEARS = list(range(2014, 2024))  # 2014~2023 (10년)

# 분야별 어휘(텍스트 분석이 의미 있게 나오도록)
VOCAB = {
    "Health": ["maternal and child health", "vaccination campaign", "primary healthcare clinic",
               "disease prevention", "essential medicines", "community health workers"],
    "Education": ["primary school construction", "teacher training program", "curriculum development",
                  "girls education", "vocational training", "scholarship support"],
    "Water & Sanitation": ["clean water supply", "sanitation facilities", "borehole drilling",
                           "hygiene promotion", "wastewater treatment", "water resource management"],
    "Agriculture": ["smallholder farmers", "irrigation system", "crop productivity",
                    "agricultural extension", "food security", "rural livelihoods"],
    "Transport Infrastructure": ["road rehabilitation", "bridge construction", "rural road access",
                                 "transport corridor", "highway upgrading", "feeder roads"],
    "Governance": ["public financial management", "capacity building", "anti-corruption",
                   "local government", "civil service reform", "rule of law"],
}
GENERIC = ["sustainable development", "poverty reduction", "technical assistance",
           "institutional strengthening", "monitoring and evaluation", "gender equality"]

# 공여국·수원국 쌍의 잠재 효과(패널 고정효과 demo용): 쌍마다 고유 baseline
PAIR_FE = {(d, r): RNG.normal(0, 0.45) for d in DONORS for r in RECIPIENTS}

rows = []
for year in YEARS:
    growth = 1 + 0.03 * (year - 2014)  # 연도별 완만한 성장
    for donor, dmult in DONORS.items():
        for recip, (gdppc0, pop0) in RECIPIENTS.items():
            gdppc = gdppc0 * growth * RNG.normal(1, 0.02)
            pop = pop0 * (1 + 0.015 * (year - 2014))
            for sector, (smult, loan_p) in SECTORS.items():
                # 모든 조합에 사업이 있진 않음 → 약 55%만 표본에 등장(현실적 희소성)
                if RNG.random() > 0.55:
                    continue
                finance = "Loan" if RNG.random() < loan_p else "Grant"
                loan_effect = 0.55 if finance == "Loan" else 0.0  # 대출이 평균적으로 큼

                # log 집행액 = 기준 + 분야 + 공여국 + 인구(+) + 1인당GDP(-) + 쌍효과 + 대출 + 잡음
                mu = (1.4
                      + np.log(smult) + np.log(dmult)
                      + 0.45 * np.log(pop)
                      - 0.40 * np.log(gdppc / 1000.0)
                      + PAIR_FE[(donor, recip)]
                      + loan_effect)
                disb = float(np.exp(mu + RNG.normal(0, 0.55)))   # 우왜도(로그정규)
                disb = round(max(disb, 0.02), 3)                 # USD 백만, 하한
                commit = round(disb / RNG.uniform(0.6, 1.0), 3)  # 약정 ≥ 집행

                # 텍스트(분야 어휘 2~3개 + 일반 1개). 보일러플레이트를 최소화해
                # TF-IDF가 '분야 내용'을 드러내도록 — 설명문은 사실상 어구 나열.
                phrases = list(RNG.choice(VOCAB[sector], size=RNG.integers(2, 4), replace=False))
                phrases.append(str(RNG.choice(GENERIC)))
                title = f"{phrases[0].title()} Project in {recip}"
                desc = ". ".join(p.capitalize() for p in phrases) + "."

                rows.append([year, donor, recip, sector, finance,
                             commit, disb, round(gdppc, 1), round(pop, 2),
                             title, desc])

df = pd.DataFrame(rows, columns=[
    "Year", "DonorName", "RecipientName", "SectorName", "FinanceType",
    "USD_Commitment", "USD_Disbursement", "RecipientGDPpc", "RecipientPop",
    "ProjectTitle", "LongDescription",
])
# 편의 컬럼: 공여국-수원국 쌍 식별자(패널용). STATA에서도 쓰기 쉽게 정수 인코딩 동봉.
df["DonorRecipient"] = df["DonorName"] + " - " + df["RecipientName"]
df["pair_id"] = df["DonorRecipient"].astype("category").cat.codes + 1

df = df.sort_values(["Year", "DonorName", "RecipientName", "SectorName"]).reset_index(drop=True)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
df.to_csv(OUT, index=False, encoding="utf-8")

# ── 검증: 강의에서 쓸 신호가 실제로 들어있는지 확인 ────────────────────────────
print(f"[OK] 저장: {os.path.normpath(OUT)}")
print(f"행/열: {df.shape[0]} x {df.shape[1]}")
print("\n[head]\n", df.head(3).to_string())
print("\n[분야별 평균 집행액(USD백만) — ANOVA 신호]")
print(df.groupby("SectorName")["USD_Disbursement"].mean().round(2).sort_values(ascending=False).to_string())
print("\n[무상 vs 유상 평균 집행액 — t검정 신호]")
print(df.groupby("FinanceType")["USD_Disbursement"].mean().round(2).to_string())
print(f"\n공여국 {df.DonorName.nunique()} · 수원국 {df.RecipientName.nunique()} · "
      f"분야 {df.SectorName.nunique()} · 연도 {df.Year.nunique()} · 쌍 {df.pair_id.nunique()}")
print(f"집행액 왜도(로그변환 필요 신호): {df.USD_Disbursement.skew():.2f}")
