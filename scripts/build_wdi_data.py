"""
강의용 World Bank WDI 패널 데이터 생성기.

World Bank 공식 API를 wbgapi로 호출해 국가×연도 개발지표 패널을 만든다.
실제 데이터(가공 없음). 인터넷 필요. 결과: ../data/wdi_panel.csv

  설치:  pip install wbgapi pandas
  실행:  python build_wdi_data.py
"""
import os
import wbgapi as wb
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data", "wdi_panel.csv")

SERIES = {
    "NY.GDP.PCAP.CD": "gdp_pc",      # 1인당 GDP (현재 US$)
    "SP.DYN.LE00.IN": "life_exp",    # 기대수명(세)
    "SH.DYN.MORT":    "under5_mort", # 5세 미만 사망률(출생 1,000명당)
    "SP.POP.TOTL":    "pop",         # 총인구
    "SE.PRM.ENRR":    "prim_enroll", # 초등 취학률(% gross)
}
YEARS = range(2000, 2023)  # 2000~2022

# 코드→이름 (World Bank 표준 분류)
INCOME = {"HIC": "High income", "UMC": "Upper middle income", "LMC": "Lower middle income",
          "LIC": "Low income", "INX": "Not classified"}
REGION = {"EAS": "East Asia & Pacific", "ECS": "Europe & Central Asia",
          "LCN": "Latin America & Caribbean", "MEA": "Middle East & North Africa",
          "NAC": "North America", "SAS": "South Asia", "SSF": "Sub-Saharan Africa"}

# 1) 지표 패널 (economy×time, 시리즈=컬럼)
raw = wb.data.DataFrame(list(SERIES), economy="all", time=YEARS, columns="series", labels=False)
df = raw.rename(columns=SERIES).reset_index()
tcol = "time" if "time" in df.columns else df.columns[1]
df["year"] = df[tcol].astype(str).str.replace("YR", "", regex=False).astype(int)

# 2) 메타: 실제 국가만(집계 제외) + 지역·소득그룹 이름
info = wb.economy.DataFrame()
info = info[info["aggregate"] == False]   # "World", "Sub-Saharan Africa" 등 집계 제거
meta = info[["name", "region", "incomeLevel"]].copy()
meta["region_name"] = meta["region"].map(REGION).fillna(meta["region"])
meta["income_name"] = meta["incomeLevel"].map(INCOME).fillna(meta["incomeLevel"])
meta = meta.reset_index().rename(columns={"index": "economy", "id": "economy"})

# 3) 병합(집계 자동 제외) + 정리 + 저장
out = meta.merge(df, on="economy", how="inner")
cols = ["economy", "name", "year", "region_name", "income_name",
        "gdp_pc", "life_exp", "under5_mort", "pop", "prim_enroll"]
out = out[[c for c in cols if c in out.columns]].sort_values(["economy", "year"]).reset_index(drop=True)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
out.to_csv(OUT, index=False, encoding="utf-8")

print(f"[OK] 저장: {os.path.normpath(OUT)}  ({out.shape[0]}행 x {out.shape[1]}열)")
print(f"국가 {out['economy'].nunique()} · 연도 {out['year'].nunique()}")
print("\n[head]\n", out.head(3).to_string())
print("\n[소득그룹별 평균 기대수명]")
print(out.groupby("income_name")["life_exp"].mean().round(1).sort_values().to_string())
