"""
Colab용 .ipynb 5종 생성(모듈 매핑). 의존성 없이 표준 라이브러리로 유효한
nbformat v4 JSON을 직접 작성. 코드는 data/wdi_panel.csv(World Bank WDI)에 대해
사전 검증됨.

  01_load_clean.ipynb         모듈2  불러오기·정제
  02_core_analysis.ipynb      모듈3  교차표·t검정/ANOVA·회귀 (STATA와 대조)
  03_panel_fe.ipynb           모듈4A 패널 고정효과(고급 분석)
  04_python_strength.ipynb    모듈4B 라이브 API 수집·자동화 (Python 확장 영역)
  05_human_verification.ipynb 모듈5  인간 검증력(시각화)
"""
import json, os

OWNER, REPO, BRANCH = "amnotyoung", "oda-ai-stats", "main"
RAW = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}/data/wdi_panel.csv"
HERE = os.path.dirname(os.path.abspath(__file__))
NBDIR = os.path.join(HERE, "..", "notebooks")


def badge(name):
    url = f"https://colab.research.google.com/github/{OWNER}/{REPO}/blob/{BRANCH}/notebooks/{name}"
    return f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({url})"


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
            "source": text.strip("\n").splitlines(keepends=True)}


def write_nb(name, cells):
    nb = {"cells": cells,
          "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                       "language_info": {"name": "python"}, "colab": {"provenance": []}},
          "nbformat": 4, "nbformat_minor": 5}
    with open(os.path.join(NBDIR, name), "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print("[OK]", name, f"({len(cells)} cells)")


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

LOAD = f'''import pandas as pd, numpy as np
RAW = "{RAW}"
df = pd.read_csv(RAW)
print("행 x 열:", df.shape)
df.head()'''

# ════════════════════════════ 01 · 불러오기·정제 ════════════════════════════
write_nb("01_load_clean.ipynb", [
    md(f"""# 01 · 데이터 불러오기와 정제  (모듈 2)
{badge("01_load_clean.ipynb")}

> **World Bank 개발지표(WDI) 패널**을 GitHub에서 바로 불러와 구조를 보고 정제한다.
> 국가×연도 데이터(2000~2022). 오늘의 원칙: **AI가 코드를 짜고 → 우리가 검증한다.**

지표: 1인당 GDP, 기대수명, 5세 미만 사망률, 인구, 초등 취학률 + 지역·소득그룹."""),
    md("## 0) 불러오기 — GitHub에서 바로 (설치 불필요)"),
    code(LOAD),
    md("## 1) 구조 파악 — 컬럼·자료형·결측\n진짜 데이터는 **결측이 있다**. 어디에 얼마나 빠졌는지 먼저 본다."),
    code("df.info()"),
    code("df.isna().sum()   # 컬럼별 결측 — under5_mort·prim_enroll에 실제 결측 존재"),
    md("""### 🔎 검증 포인트 — 단위·범위·상식
- 기대수명은 0~90세 범위인가? · 1인당 GDP는 양수인가? · 결측을 어떻게 다룰까?"""),
    code("""print("기대수명 범위:", df.life_exp.min(), "~", df.life_exp.max())
print("1인당 GDP 음수:", (df.gdp_pc <= 0).sum(), "건")
df[["gdp_pc","life_exp","under5_mort","pop","prim_enroll"]].describe().round(1)"""),
    md("## 2) 정제 + 파생변수\n분석에 쓸 핵심 변수의 결측 행을 제거하고, 금액·인구는 **로그변환**(왜도 큼)."),
    code("""work = df.dropna(subset=["gdp_pc","life_exp"]).copy()
work["log_gdp"] = np.log(work["gdp_pc"])
work["log_pop"] = np.log(work["pop"])
print("정제 후 행:", len(work), "/ 원본:", len(df))
work.head(3)"""),
    md("## 3) 빠른 요약 — 소득그룹별 평균 기대수명"),
    code("""work.groupby("income_name")["life_exp"]\\
    .agg(국가연도수="count", 평균기대수명="mean")\\
    .round(1).sort_values("평균기대수명")"""),
    md("""---
✅ **정리**: 불러오기 → 구조·결측 파악 → 검증 → 정제 → 요약. AI에게 시켜도 **이 흐름과 검증은 사람 몫**.

🔁 **폐쇄망 STATA로는?** 같은 작업을 `stata/01_load_clean.do` 에."""),
])

# ════════════════════════ 02 · 핵심 분석 (STATA와 대조) ════════════════════════
write_nb("02_core_analysis.ipynb", [
    md(f"""# 02 · 핵심 분석: 교차표·집단비교·회귀  (모듈 3)
{badge("02_core_analysis.ipynb")}

> 대표 분석 3종을 Python으로 수행하고, **같은 분석을 STATA로도**(각 절 🔁) 해서
> 두 결과의 숫자가 같은지 **교차검증**한다. — "숫자는 같다. 출력 모양만 다르다.\""""),
    code(f'''import pandas as pd, numpy as np
from scipy import stats
import statsmodels.formula.api as smf
df = pd.read_csv("{RAW}")
df["log_gdp"] = np.log(df["gdp_pc"])
df["log_pop"] = np.log(df["pop"])
print("준비 완료:", df.shape)'''),
    md("## 1) 교차표 — 지역 × 소득그룹 (국가 수)\n지역·소득은 국가 속성이므로 **국가 단위로** 집계한다."),
    code("""countries = df.drop_duplicates("economy")
pd.crosstab(countries["region_name"], countries["income_name"])"""),
    md("🔁 **STATA**: `tabulate region_name income_name`  ·  코드 → `stata/02_crosstab.do`"),
    md("## 2) 집단 비교 — 지역 격차(t검정), 소득그룹 차이(ANOVA)"),
    code("""# t검정: 사하라이남 아프리카 vs 그 외 (기대수명) — 분산이 달라 Welch 사용
ssa  = df.loc[df.region_name == "Sub-Saharan Africa", "life_exp"].dropna()
rest = df.loc[df.region_name != "Sub-Saharan Africa", "life_exp"].dropna()
t, p = stats.ttest_ind(ssa, rest, equal_var=False)   # Welch → STATA는 ttest ..., unequal
print(f"[t검정] 사하라이남={ssa.mean():.1f}세  그외={rest.mean():.1f}세  t={t:.1f}  p={p:.1e}")

# ANOVA: 소득그룹 간 기대수명
groups = [g["life_exp"].dropna().values for _, g in df.groupby("income_name")]
F, p2 = stats.f_oneway(*[g for g in groups if len(g) > 1])
print(f"[ANOVA] 소득그룹별 기대수명  F={F:.0f}  p={p2:.1e}")"""),
    md("🔁 **STATA**: `ttest life_exp, by(ssa) unequal`  ·  `oneway life_exp income_n`  ·  코드 → `stata/03_group_compare.do`"),
    md("""## 3) 회귀분석 — Preston 곡선 (소득 → 기대수명)
개발경제의 고전. 1인당 GDP는 왜도가 크므로 **로그**를 취한다 — AI가 자동으로 안 할 수 있는 **설계 판단**."""),
    code("""m = smf.ols("life_exp ~ log_gdp", data=df).fit()
print(m.summary().tables[1])
print(f"\\nR² = {m.rsquared:.3f}")"""),
    md("""**해석**: `log_gdp` 계수가 **양수** → 소득이 높을수록 기대수명↑. (소득 e배 ≈ +계수 만큼 수명)
R²가 높아 소득만으로 기대수명 차이의 상당 부분이 설명된다.

🔁 **STATA**: `regress life_exp log_gdp` — **한 줄**.  코드 → `stata/04_regression.do`
> 양쪽 계수·R²가 같은지 **교차검증**: 같으면 신뢰, 다르면 하나가 틀린 것."""),
    md("""---
✅ **핵심**: 교차표·검정·회귀를 입문자가 첫날 직접 돌렸다. 비결은 *문법 암기*가 아니라
*무엇을·왜 분석할지 설계*하고 *검증·해석*하는 것."""),
])

# ════════════════════════ 03 · 패널 고정효과 (STATA 강점) ════════════════════════
write_nb("03_panel_fe.ipynb", [
    md(f"""# 03 · 고급 분석: 패널 고정효과  (모듈 4-A)
{badge("03_panel_fe.ipynb")}

> 고급 계량 분석도 AI 도움으로 **양쪽 도구에서** 할 수 있다. 국가×연도 패널의 고정효과를
> Python으로, 그리고 STATA로 — **둘 다 같은 결과**. 도구는 우열이 아니라 **환경**으로 고른다."""),
    code(f'''import pandas as pd, numpy as np
import statsmodels.formula.api as smf
df = pd.read_csv("{RAW}").dropna(subset=["gdp_pc","life_exp"])
df["log_gdp"] = np.log(df["gdp_pc"])
print("국가:", df["economy"].nunique(), "· 연도:", df["year"].nunique(), "· 행:", len(df))'''),
    md("""## 문제 — 국가의 고유 특성을 통제하려면?
제도·기후·역사처럼 **잘 변하지 않는 국가 고유 효과**를 빼고, *한 나라 안에서* 소득이 오를 때
기대수명이 어떻게 변하는지 보려면 **고정효과**가 필요하다."""),
    md("### (1) 통제 안 함 — 단순 회귀(pooled)"),
    code("""pooled = smf.ols("life_exp ~ log_gdp", data=df).fit()
print("pooled  log_gdp 계수 =", round(pooled.params["log_gdp"], 2))"""),
    md("### (2) Python으로 국가 고정효과 (더미를 다 넣어야 함)"),
    code("""fe = smf.ols("life_exp ~ log_gdp + C(economy)", data=df).fit()
n = sum(c.startswith("C(economy)") for c in fe.params.index)
print("국가FE  log_gdp 계수 =", round(fe.params["log_gdp"], 2), "(국가효과 흡수로 변화)")
print("추가된 국가 더미 =", n, "개 (국가 고정효과)")"""),
    md("""### (3) STATA에선 — 같은 분석
```stata
encode economy, gen(country_id)
xtset country_id year
xtreg life_exp log_gdp, fe vce(cluster country_id)
```
- `xtreg, fe` 가 200여 개 국가 고정효과를 흡수하고, `vce(cluster ...)`로 강건표준오차까지. 위 Python의 `C(economy)`와 **동일한 모형**.
- 코드 → `stata/05_panel_fe.do`  ·  **`xtreg`는 폐쇄망에서 인터넷 없이 실행** ✅

---
✅ **포인트**: 고급 계량 모형도 이제 **양쪽에서** 가능 — AI가 코드를 짜준다.
도구는 *우열*이 아니라 **환경**으로 고른다(폐쇄망 현업은 STATA, 외부망 탐색·확장은 Python)."""),
])

# ════════════════════════ 04 · Python 확장 영역: 라이브 API 수집 ════════════════════════
write_nb("04_python_strength.ipynb", [
    md(f"""# 04 · Python의 확장 영역: 라이브 API 데이터 수집  (모듈 4-B)
{badge("04_python_strength.ipynb")}

> **STATA로는 하기 어려운** 일. World Bank API에서 **실시간으로 데이터를 수집하고 자동화**한다.
> 사실 *이 강의 데이터 자체*가 이렇게 만들어졌다. 수집·API·자동화·ML은 **Python의 영역**이고 외부망에서 한다."""),
    code("""# World Bank 공식 API 패키지 (Colab에 없으면 설치)
try:
    import wbgapi as wb
except ModuleNotFoundError:
    import subprocess, sys
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "wbgapi"])
    import wbgapi as wb
import pandas as pd
print("wbgapi 준비 완료")"""),
    md("## 1) 한 줄로 실시간 수집 — 1인당 GDP, 최근\nAPI를 직접 호출해 **방금 만든** 데이터를 가져온다(저장된 CSV가 아니라 라이브)."),
    code("""wb.data.DataFrame("NY.GDP.PCAP.CD", ["KOR","VNM","KEN","ETH"], range(2019, 2023)).round(0)"""),
    md("## 2) 자동화 — 여러 지표를 한 번에 수집\n사람이 일일이 복사할 일을 코드가 반복한다(자동화의 핵심)."),
    code("""series = {"NY.GDP.PCAP.CD":"gdp_pc", "SP.DYN.LE00.IN":"life_exp", "IT.NET.USER.ZS":"internet_%"}
live = wb.data.DataFrame(list(series), ["KOR","VNM","KEN","ETH"], time=2021, columns="series", labels=False)
live.rename(columns=series).round(1)"""),
    md("## 3) 검색도 코드로 — '기대수명' 지표 찾기"),
    code("""for s in wb.series.info(q="life expectancy").items[:5]:
    print(s["id"], "—", s["value"])"""),
    md("""---
✅ **포인트**: 이건 **Python만의 능력**이다(수집·API·자동화·텍스트·ML).
"이런 분석이 오면 Python, 외부망에서" 라고 판단하면 된다. STATA로는 사실상 못 한다.

🧭 **인간 검증**: API가 준 값이 현장과 맞는지(예: 한국 인터넷 보급률)는 **도메인 지식**으로 확인한다."""),
])

# ════════════════════════ 05 · 인간의 검증력 (시각화) ════════════════════════
write_nb("05_human_verification.ipynb", [
    md(f"""# 05 · 인간의 검증력: 시각화로 오류 잡기  (모듈 5)
{badge("05_human_verification.ipynb")}

> AI가 만든 "그럴듯한 분석"을 **인간의 3대 무기 — 🖼️시각화 · 🧭도메인 지식 · 👥동료 회람**으로 검증한다.
> AI는 빠르지만 *보지 못하고, 맥락이 없고, 혼자* 일한다."""),
    code(FONT_SETUP),
    code(f'''import pandas as pd, numpy as np, matplotlib.pyplot as plt
df = pd.read_csv("{RAW}").dropna(subset=["gdp_pc","life_exp"]).copy()
df["log_gdp"] = np.log(df["gdp_pc"])'''),
    md("""## 시나리오 — "소득이 높을수록 기대수명이 길다"
AI에게 분석을 시켰더니 상관계수를 줬다. **숫자만 보면 완벽해 보인다.**"""),
    code("""print("상관계수(log소득 vs 기대수명):", round(df["log_gdp"].corr(df["life_exp"]), 3))"""),
    md("""### 🖼️ 무기 1 — **그려본다**
현업 데이터엔 입력 오류가 섞이기 쉽다. 한 나라의 1인당 GDP가 **단위 실수로 1,000배** 잘못
입력됐다고 하자(흔한 오류). 숫자로는 안 보이지만 **그리면** 바로 드러난다."""),
    code("""dirty = df.copy()
idx = dirty.index[dirty["economy"].eq("VNM") & dirty["year"].eq(2021)]
dirty.loc[idx, "gdp_pc"] = dirty.loc[idx, "gdp_pc"] * 1000     # 단위 오류 주입
dirty["log_gdp"] = np.log(dirty["gdp_pc"])

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].scatter(dirty["log_gdp"], dirty["life_exp"], s=8); ax[0].set_title("AI가 받은 데이터(오류 포함)")
ax[1].scatter(df["log_gdp"], df["life_exp"], s=8, c="green"); ax[1].set_title("정상")
for a in ax: a.set_xlabel("log(1인당 GDP)"); a.set_ylabel("기대수명")
plt.tight_layout(); plt.show()"""),
    md("→ 왼쪽 그림에 **오른쪽으로 멀리 튄 점**이 한눈에. 표의 숫자만 봤다면 회귀가 왜곡됐을 것이다."),
    code("""# 범인 찾기: 비정상적으로 부유해 보이는 나라-연도
sus = dirty.sort_values("gdp_pc", ascending=False).head(3)
sus[["name","year","gdp_pc","life_exp"]]"""),
    md("""### 🧭 무기 2 — **도메인 지식**
"베트남 1인당 GDP가 한 해에 갑자기 세계 최고? 현장을 아는 사람은 *말이 안 된다*는 걸 안다."
AI엔 현장의 사실(ground truth)이 없다. **여러분에겐 있다.**

### 👥 무기 3 — **동료 회람**
1장 요약을 그 지역을 아는 **동료에게 회람**: "이 수치 단위가 이상한데요?"
한 사람(혹은 AI)이 놓친 걸 **여러 눈**이 잡는다.

---
✅ **결론**: AI가 분석을 *쉽게* 만들어도, *맞게* 만드는 건 인간이다.
시각화·도메인·회람 — 이 무기를 매번 쓰자. (체크리스트 → `handouts/verification_checklist.md`)"""),
])

print("\\n전체 노트북 생성 완료.")
