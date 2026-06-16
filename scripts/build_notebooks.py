"""
Colab용 .ipynb 5종을 생성한다(모듈 매핑). 의존성 없이 표준 라이브러리만 사용해
유효한 nbformat v4 JSON을 직접 작성한다. 코드 셀은 build_sample_data.py로 만든
데이터에 대해 사전 검증된 분석이다.

생성물(notebooks/):
  01_load_clean.ipynb        모듈2  데이터 불러오기·정제
  02_core_analysis.ipynb     모듈3  교차표·t검정/ANOVA·회귀 (STATA와 대조)
  03_panel_fe.ipynb          모듈4A 패널 고정효과(고급 분석)
  04_text_analysis.ipynb     모듈4B 텍스트 분석(Python 확장 영역)
  05_human_verification.ipynb 모듈5 인간의 검증력(시각화로 오류 잡기)
"""
import json, os

OWNER, REPO, BRANCH = "amnotyoung", "oda-ai-stats", "main"
RAW = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}/data/sample_crs.csv"
HERE = os.path.dirname(os.path.abspath(__file__))
NBDIR = os.path.join(HERE, "..", "notebooks")


def badge(name):
    url = f"https://colab.research.google.com/github/{OWNER}/{REPO}/blob/{BRANCH}/notebooks/{name}"
    return f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({url})"


def md(text):
    return {"cell_type": "markdown", "metadata": {},
            "source": text.splitlines(keepends=True)}


def code(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [], "source": text.strip("\n").splitlines(keepends=True)}


def write_nb(name, cells):
    nb = {"cells": cells,
          "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                       "language_info": {"name": "python"},
                       "colab": {"provenance": []}},
          "nbformat": 4, "nbformat_minor": 5}
    path = os.path.join(NBDIR, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print("[OK]", os.path.normpath(path), f"({len(cells)} cells)")


LOAD = f'''import pandas as pd, numpy as np
RAW = "{RAW}"
df = pd.read_csv(RAW)
print("행 x 열:", df.shape)
df.head()'''

# 한글 폰트 설정 셀(그래프가 있는 노트북에만 삽입). Colab 밖에서도 에러 없이 통과하도록 예외처리.
FONT_SETUP = '''# 한글 폰트 설정 — Colab 그래프의 한글이 깨지지 않도록 (처음 1회 약 20초)
import os, matplotlib.pyplot as plt, matplotlib.font_manager as fm
try:
    p = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
    if not os.path.exists(p):
        os.system("apt-get -qq install -y fonts-nanum > /dev/null 2>&1")
    fm.fontManager.addfont(p)
    plt.rc("font", family="NanumGothic")
except Exception:
    pass
plt.rc("axes", unicode_minus=False)'''

# ════════════════════════════ 01 · 데이터 불러오기·정제 ════════════════════════════
write_nb("01_load_clean.ipynb", [
    md(f"""# 01 · 데이터 불러오기와 정제  (모듈 2)
{badge("01_load_clean.ipynb")}

> **OECD CRS(원조사업) 데이터**를 GitHub에서 바로 불러와 구조를 파악하고 정제한다.
> 오늘의 원칙: **AI가 코드를 짠다 → 우리는 검증한다.** 셀을 실행하며 "이 숫자가 맞나?"를 계속 묻자.

이 데이터는 실제 원조액이 아니라 CRS 구조를 모사한 **교육용 합성 데이터**다."""),
    md("## 0) 데이터 불러오기 — GitHub에서 바로 (설치 불필요)"),
    code(LOAD),
    md("## 1) 구조 파악 — 컬럼·자료형·결측\n각 컬럼이 무엇인지, 빠진 값은 없는지 먼저 본다."),
    code("df.info()"),
    code("df.isna().sum()   # 컬럼별 결측 개수"),
    md("""### 🔎 검증 포인트 — 단위·정의·이상치
AI가 정제 코드를 짜주기 전에, **사람이 먼저 데이터의 상식을 확인**한다.
- 금액 단위는? (여기선 **USD 백만**) · 음수/0 집행액은 없나? · 약정액 ≥ 집행액인가?"""),
    code("""print("집행액이 0 이하인 행:", (df["USD_Disbursement"] <= 0).sum())
print("약정액 < 집행액(이상)인 행:", (df["USD_Commitment"] < df["USD_Disbursement"]).sum())
df[["USD_Commitment", "USD_Disbursement", "RecipientGDPpc", "RecipientPop"]].describe().round(1)"""),
    md("## 2) 간단 정제 + 파생변수\n분석에 쓸 형태로 다듬는다. 금액은 왜도가 크므로 **로그변환** 변수도 만든다."),
    code("""work = df.dropna(subset=["USD_Disbursement", "RecipientGDPpc", "RecipientPop"]).copy()
work = work[work["USD_Disbursement"] > 0]
work["log_disb"]  = np.log(work["USD_Disbursement"])
work["log_gdppc"] = np.log(work["RecipientGDPpc"])
work["log_pop"]   = np.log(work["RecipientPop"])
print("정제 후 행 수:", len(work))
work.head(3)"""),
    md("## 3) 빠른 요약 — 분야별 사업 건수·평균 집행액"),
    code("""work.groupby("SectorName")["USD_Disbursement"]\\
    .agg(건수="count", 평균_백만USD="mean")\\
    .round(2).sort_values("평균_백만USD", ascending=False)"""),
    md("""---
✅ **정리**: 불러오기 → 구조 파악 → 검증 → 정제 → 요약. AI에게 시켜도 **이 흐름과 검증은 사람의 몫**.

🔁 **폐쇄망 STATA로는?** 같은 작업을 `stata/01_load_clean.do` 에. 외부망에서 배우고, 그 `.do`를 폐쇄망에서 실행한다."""),
])

# ════════════════════════ 02 · 핵심 분석 (STATA와 대조) ════════════════════════
write_nb("02_core_analysis.ipynb", [
    md(f"""# 02 · 핵심 분석: 교차표·집단비교·회귀  (모듈 3)
{badge("02_core_analysis.ipynb")}

> 대표 분석 3종을 Python으로 수행한다. **같은 분석을 STATA로도** 하고(각 절의 🔁),
> 두 결과의 숫자가 같은지 **교차검증**한다. — "숫자는 같다. 출력 모양만 다르다.\""""),
    code(f'''import pandas as pd, numpy as np
from scipy import stats
import statsmodels.formula.api as smf
df = pd.read_csv("{RAW}")
df["log_disb"]  = np.log(df["USD_Disbursement"])
df["log_gdppc"] = np.log(df["RecipientGDPpc"])
df["log_pop"]   = np.log(df["RecipientPop"])
print("준비 완료:", df.shape)'''),
    md("## 1) 교차표(교차분석) — 공여국 × 분야별 평균 집행액"),
    code("""pd.pivot_table(df, values="USD_Disbursement",
               index="DonorName", columns="SectorName",
               aggfunc="mean").round(1)"""),
    md("""🔁 **STATA**: `table donorname sectorname, contents(mean usd_disbursement)`  ·  코드 → `stata/02_crosstab.do`"""),
    md("## 2) 집단 비교 — 무상 vs 유상(t검정), 분야 간(ANOVA)"),
    code("""grant = df.loc[df.FinanceType == "Grant", "USD_Disbursement"]
loan  = df.loc[df.FinanceType == "Loan",  "USD_Disbursement"]
t, p = stats.ttest_ind(grant, loan, equal_var=False)
print(f"[t검정] 무상 평균={grant.mean():.1f}  유상 평균={loan.mean():.1f}  t={t:.2f}  p={p:.2e}")

groups = [g["USD_Disbursement"].values for _, g in df.groupby("SectorName")]
F, p2 = stats.f_oneway(*groups)
print(f"[ANOVA] 분야 간 평균 차이  F={F:.2f}  p={p2:.2e}")"""),
    md("""🔁 **STATA**: `ttest usd_disbursement, by(financetype)`  ·  `oneway usd_disbursement sector_n`  ·  코드 → `stata/03_group_compare.do`"""),
    md("""## 3) 회귀분석 — 배분 결정요인 (로그변환의 이유)
집행액은 **왜도가 크다**(소수 대형사업). 그대로 쓰면 분석이 왜곡되므로 **로그**를 취한다.
→ AI가 자동으로 안 해줄 수 있는 **설계 판단**이고, 이게 사람의 역할이다."""),
    code("""print("집행액 왜도:", round(df["USD_Disbursement"].skew(), 2), "→ 큼 → 로그변환 필요")
m = smf.ols("log_disb ~ log_gdppc + log_pop", data=df).fit()
print(m.summary().tables[1])
print(f"\\nR² = {m.rsquared:.3f}")"""),
    md("""**해석**: `log_gdppc` 계수가 **음수** → 1인당 GDP가 낮은(가난한) 수원국일수록 배분액↑.
`log_pop` 계수가 **양수** → 인구가 많을수록 배분액↑.

🔁 **STATA**: `regress log_disb log_gdppc log_pop` — **한 줄**.  코드 → `stata/04_regression.do`
> 두 도구의 계수·p값이 같은지 **교차검증**: 같으면 신뢰, 다르면 하나가 틀린 것."""),
    md("""---
✅ **핵심**: 교차표·검정·회귀 — 입문자가 첫날 직접 돌렸다. 비결은 *문법 암기*가 아니라
*무엇을·왜 분석할지 설계*하고 *결과를 검증·해석*하는 것."""),
])

# ════════════════════════ 03 · 고급 분석: 패널 고정효과 ════════════════════════
write_nb("03_panel_fe.ipynb", [
    md(f"""# 03 · 고급 분석: 패널 고정효과  (모듈 4-A)
{badge("03_panel_fe.ipynb")}

> 고급 계량 분석도 AI 도움으로 **양쪽 도구에서** 할 수 있다. 패널 고정효과를 Python으로,
> 그리고 STATA로 — **둘 다 같은 결과**. 도구는 우열이 아니라 **환경(폐쇄망/외부망)**으로 고른다."""),
    code(f'''import pandas as pd, numpy as np
import statsmodels.formula.api as smf
df = pd.read_csv("{RAW}")
df["log_disb"]  = np.log(df["USD_Disbursement"])
df["log_gdppc"] = np.log(df["RecipientGDPpc"])
df["log_pop"]   = np.log(df["RecipientPop"])
print("공여국-수원국 쌍 수:", df["pair_id"].nunique(), "· 연도:", df["Year"].nunique())'''),
    md("""## 문제 — 쌍(공여국×수원국)의 고유 특성을 통제하려면?
역사·외교관계처럼 **잘 변하지 않는 쌍 고유 효과**를 빼고 순수 효과를 보려면 **고정효과**가 필요하다."""),
    md("### (1) 통제 안 함 — 단순 회귀(pooled)"),
    code("""pooled = smf.ols("log_disb ~ log_gdppc + log_pop", data=df).fit()
print("pooled  log_pop 계수 =", round(pooled.params["log_pop"], 3))"""),
    md("### (2) Python으로 고정효과 (쌍 효과 흡수)"),
    code("""fe = smf.ols("log_disb ~ log_gdppc + log_pop + C(pair_id)", data=df).fit()
n_dummies = sum(c.startswith("C(pair_id)") for c in fe.params.index)
print("FE      log_pop 계수 =", round(fe.params["log_pop"], 3), "(쌍효과 흡수로 변화)")
print("추가된 쌍 더미 개수 =", n_dummies, "개 (쌍 고정효과)")"""),
    md("""### (3) STATA에선 — 같은 분석
```stata
xtset pair_id
xtreg log_disb log_gdppc log_pop, fe vce(cluster pair_id)
```
- `xtreg, fe` 가 60개 쌍의 고정효과를 흡수하고, `vce(cluster ...)`로 강건표준오차까지. 위 Python의 `C(pair_id)`와 **동일한 모형**.
- (한 쌍·연도에 여러 분야 사업이 있어 **쌍 고정효과만** 선언.)
- 코드 → `stata/05_panel_fe.do`  ·  **`xtreg`는 폐쇄망에서 인터넷 없이 실행** ✅

---
✅ **포인트**: 고급 계량 모형도 이제 **양쪽에서** 가능 — AI가 코드를 짜준다.
도구는 *우열*이 아니라 **환경**으로 고른다(폐쇄망 현업은 STATA, 외부망 탐색·확장은 Python)."""),
])

# ════════════════════════ 04 · Python의 확장 영역: 텍스트 ════════════════════════
write_nb("04_text_analysis.ipynb", [
    md(f"""# 04 · Python의 확장 영역: 사업설명 텍스트  (모듈 4-B)
{badge("04_text_analysis.ipynb")}

> **STATA로는 사실상 못 하는** 분석. 수천 개 사업 설명문에서 "우리가 실제로 무엇을 하나"를
> 텍스트로 들여다본다. 이런 일(텍스트·수집·자동화·ML)은 **Python의 영역**이고 외부망에서 한다."""),
    code(FONT_SETUP),
    code(f'''import pandas as pd, numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
df = pd.read_csv("{RAW}")
print("사업 설명문 예시:")
for s in df["LongDescription"].head(3):
    print(" -", s)'''),
    md("## 1) 전체 상위 키워드 (TF-IDF)\n어떤 표현이 포트폴리오 전반에서 두드러지나?"),
    code("""tf = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_df=0.6, max_features=15)
X = tf.fit_transform(df["LongDescription"])
scores = np.asarray(X.mean(axis=0)).ravel()
top = pd.Series(scores, index=tf.get_feature_names_out()).sort_values()
top.tail(10).plot.barh(figsize=(7, 4), title="전체 상위 키워드 (TF-IDF)")
plt.tight_layout(); plt.show()"""),
    md("## 2) 분야별 대표 키워드 — 텍스트가 드러내는 '사업의 실제 내용'\n숫자가 아니라 **내용**을 분석한다. 분야마다 무엇을 하는지 키워드로 확인."),
    code("""def top_keywords(texts, k=3):
    v = TfidfVectorizer(stop_words="english", ngram_range=(2, 2))
    M = v.fit_transform(texts)
    s = np.asarray(M.mean(axis=0)).ravel()
    return ", ".join(pd.Series(s, index=v.get_feature_names_out()).sort_values().tail(k).index[::-1])

for sec, g in df.groupby("SectorName"):
    print(f"{sec:26s}: {top_keywords(g['LongDescription'])}")"""),
    md("""---
✅ **포인트**: 이건 **Python만의 능력**이다(텍스트·수집·자동화·ML도 같은 결).
"이런 분석이 오면 Python, 외부망에서" 라고 판단하면 된다.

🧭 **인간 검증**: 키워드가 분야와 맞는지(예: Health→primary healthcare)는 **도메인 지식**으로 확인한다 —
AI도 사람도, 결과가 현장과 맞는지는 사람이 안다."""),
])

# ════════════════════════ 05 · 인간의 검증력 (시각화) ════════════════════════
write_nb("05_human_verification.ipynb", [
    md(f"""# 05 · 인간의 검증력: 시각화로 오류 잡기  (모듈 5)
{badge("05_human_verification.ipynb")}

> AI가 만든 "그럴듯한 분석"을 **인간의 3대 무기 — 🖼️시각화 · 🧭도메인 지식 · 👥동료 회람**으로 검증한다.
> AI는 빠르지만 *보지 못하고, 맥락이 없고, 혼자* 일한다."""),
    code(FONT_SETUP),
    code(f'''import pandas as pd, numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv("{RAW}")'''),
    md("""## 시나리오 — "보건 분야 ODA는 어떻게 변했나?"
AI에게 분석을 시켰더니 아래 표를 줬다. **표만 보면 완벽해 보인다.**"""),
    code("""health = df[df.SectorName == "Health"]
yearly = health.groupby("Year")["USD_Disbursement"].sum().round(1)
yearly  # 표: 깔끔해 보인다"""),
    md("""### 🖼️ 무기 1 — **그려본다**
현업에선 데이터에 오류가 섞이기 쉽다. 한 대형사업이 **이중계상**됐다고 해보자(흔한 실수).
표로는 안 보이지만, **그리면** 바로 드러난다."""),
    code("""# 흔한 오류를 모사: 2019년 한 대형 보건사업이 실수로 10배 중복 입력됐다고 가정
dirty = df.copy()
big = dirty[(dirty.SectorName == "Health") & (dirty.Year == 2019)].sort_values("USD_Disbursement").tail(1)
dup = pd.concat([big] * 9, ignore_index=True)        # 같은 사업 9번 더 추가(이중계상)
dirty = pd.concat([dirty, dup], ignore_index=True)

y_dirty = dirty[dirty.SectorName == "Health"].groupby("Year")["USD_Disbursement"].sum()
y_clean = df[df.SectorName == "Health"].groupby("Year")["USD_Disbursement"].sum()
plt.figure(figsize=(8, 4))
plt.plot(y_dirty.index, y_dirty.values, "o-", label="AI가 받은 데이터(오류 포함)")
plt.plot(y_clean.index, y_clean.values, "s--", label="실제(정상)")
plt.title("보건 ODA 연도별 추세 — 표는 속삭이지만 그림은 소리친다")
plt.legend(); plt.tight_layout(); plt.show()"""),
    md("→ **2019년 비정상 급등**이 한눈에. 표의 숫자만 봤다면 보고서에 그대로 들어갔을 오류다."),
    code("""# 범인 찾기: 같은 사업이 여러 번? 도메인 지식으로 '말이 되나' 확인
susp = dirty[(dirty.SectorName == "Health") & (dirty.Year == 2019)]
susp["ProjectTitle"].value_counts().head(3)   # 한 사업명이 비정상적으로 여러 번"""),
    md("""### 🧭 무기 2 — **도메인 지식**
"이 수원국이 그 해 보건 최대 수혜국? 현장을 아는 사람은 *말이 안 된다*는 걸 안다."
AI에겐 현장의 사실(ground truth)이 없다. **여러분에겐 있다.**

### 👥 무기 3 — **동료 회람**
1장 요약을 그 사업/지역을 아는 **동료에게 회람**: "그 사업 2018년에 종료됐는데?"
한 사람(혹은 AI)이 놓친 걸 **여러 눈**이 잡는다.

---
✅ **결론**: AI가 분석을 *쉽게* 만들어도, *맞게* 만드는 건 인간이다.
시각화·도메인·회람 — 이 무기를 매번 쓰자. (체크리스트 → `handouts/verification_checklist.md`)"""),
])

print("\\n전체 노트북 생성 완료.")
