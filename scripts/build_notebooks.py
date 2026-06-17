"""
Colab용 .ipynb 5종 생성(모듈 매핑). 의존성 없이 표준 라이브러리로 유효한
nbformat v4 JSON을 직접 작성. 코드는 data/wdi_panel.csv(World Bank WDI)에 대해
사전 검증됨. 코드 셀은 입문자용으로 줄마다 한국어 주석을 단다.

  01_load_clean.ipynb         모듈2  불러오기·정제
  02_core_analysis.ipynb      모듈3  교차표·t검정/ANOVA·회귀 (STATA와 대조)
  03_panel_fe.ipynb           모듈4A 이원 고정효과(고급 인과추론)
  04_python_strength.ipynb    모듈4B 라이브 수집 + 머신러닝 (Python 고급)
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


FONT_SETUP = '''# [한 번 실행하고 넘어가세요] 한글 폰트 설정 — Colab 그래프의 한글이 깨지지 않도록(처음 1회 ~20초)
import os, matplotlib.pyplot as plt, matplotlib.font_manager as fm
try:
    p = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"   # 나눔고딕 폰트 경로
    if not os.path.exists(p):                                # 없으면
        os.system("apt-get -qq install -y fonts-nanum > /dev/null 2>&1")  # 설치
    fm.fontManager.addfont(p)                               # matplotlib에 폰트 등록
    plt.rc("font", family="NanumGothic")                   # 기본 글꼴로 지정
except Exception:
    pass                                                    # 실패해도 그냥 진행(영문은 정상)
plt.rc("axes", unicode_minus=False)                         # 마이너스 기호 깨짐 방지'''

LOAD = f'''import pandas as pd, numpy as np    # pandas=표 데이터 다루기, numpy=수치 계산
RAW = "{RAW}"                                  # GitHub에 올라간 데이터 파일 주소(URL)
df = pd.read_csv(RAW)                          # CSV 파일을 표(DataFrame)로 불러오기
print("행 x 열:", df.shape)                    # (행 수, 열 수) 확인
df.head()                                      # 맨 위 5개 행 미리보기'''

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
    code("df.info()   # 각 컬럼의 자료형(숫자/문자)과 '결측 아닌 값' 개수를 한눈에"),
    code('df.isna().sum()   # 컬럼별 결측(빈 값) 개수 — under5_mort·prim_enroll에 실제 결측'),
    md("""### 🔎 검증 포인트 — 단위·범위·상식
- 기대수명은 0~90세 범위인가? · 1인당 GDP는 양수인가? · 결측을 어떻게 다룰까?"""),
    code("""# 값이 상식 범위인지 먼저 확인(검증) — AI가 짠 코드라도 사람이 점검한다
print("기대수명 범위:", df.life_exp.min(), "~", df.life_exp.max())   # 0~90세 안이면 정상
print("1인당 GDP 음수:", (df.gdp_pc <= 0).sum(), "건")               # 음수/0이면 이상
df[["gdp_pc","life_exp","under5_mort","pop","prim_enroll"]].describe().round(1)  # 평균·최소·최대 등 요약통계"""),
    md("## 2) 정제 + 파생변수\n분석에 쓸 핵심 변수의 결측 행을 제거하고, 금액·인구는 **로그변환**(왜도 큼)."),
    code("""# 핵심 변수(gdp_pc, life_exp)가 빈 행은 제거. .copy()=원본은 두고 복사본에서 작업
work = df.dropna(subset=["gdp_pc","life_exp"]).copy()
work["log_gdp"] = np.log(work["gdp_pc"])   # 1인당 GDP는 한쪽으로 쏠려(왜도↑) → 로그변환
work["log_pop"] = np.log(work["pop"])      # 인구도 로그변환
print("정제 후 행:", len(work), "/ 원본:", len(df))   # 몇 행이 빠졌는지 확인
work.head(3)"""),
    md("## 3) 빠른 요약 — 소득그룹별 평균 기대수명"),
    code("""# 소득그룹(income_name)별로 묶어서(group) 기대수명의 '개수'와 '평균' 계산
work.groupby("income_name")["life_exp"]\\
    .agg(국가연도수="count", 평균기대수명="mean")\\
    .round(1).sort_values("평균기대수명")   # 소수 1자리 반올림 + 평균 오름차순 정렬"""),
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
from scipy import stats                       # t검정·ANOVA 등 통계 검정 함수
import statsmodels.formula.api as smf         # 회귀분석(R 스타일 수식 사용)
df = pd.read_csv("{RAW}")                      # 데이터 불러오기
df["log_gdp"] = np.log(df["gdp_pc"])           # 로그변환 변수 미리 생성
df["log_pop"] = np.log(df["pop"])
print("준비 완료:", df.shape)'''),
    md("## 1) 교차표 — 지역 × 소득그룹 (국가 수)\n지역·소득은 국가 속성이므로 **국가 단위로** 집계한다(연도 중복 제거)."),
    code("""# 지역·소득은 '국가'의 속성 → 국가당 1행만 남겨 연도 중복 제거
countries = df.drop_duplicates("economy")
# 행=지역, 열=소득그룹 으로 국가 수를 센 교차표
pd.crosstab(countries["region_name"], countries["income_name"])"""),
    md("🔁 **STATA**: `tabulate region_name income_name`  ·  코드 → `stata/02_crosstab.do`"),
    md("""## 2) 집단 비교 — 지역 격차(t검정) · 소득그룹 차이(ANOVA)
- **t검정** = *두* 집단의 평균이 다른지, **ANOVA** = *셋 이상* 집단의 평균이 다른지 검정.
- 둘 다 **`p` < 0.05면 "우연으로 보기 어렵다(통계적으로 유의)"**."""),
    code("""# t검정: 두 집단(사하라이남 아프리카 vs 그 외)의 기대수명 평균 차이
ssa  = df.loc[df.region_name == "Sub-Saharan Africa", "life_exp"].dropna()   # 사하라이남 값만
rest = df.loc[df.region_name != "Sub-Saharan Africa", "life_exp"].dropna()   # 나머지 값만
t, p = stats.ttest_ind(ssa, rest, equal_var=False)   # 분산이 달라 Welch 검정(STATA는 ttest ..., unequal)
print(f"[t검정] 사하라이남={ssa.mean():.1f}세  그외={rest.mean():.1f}세  t={t:.1f}  p={p:.1e}")  # p 작으면 차이 유의

# ANOVA: 셋 이상 집단(소득그룹 4개) 간 기대수명 평균 차이
groups = [g["life_exp"].dropna().values for _, g in df.groupby("income_name")]  # 소득그룹별 값 묶음
F, p2 = stats.f_oneway(*[g for g in groups if len(g) > 1])   # 일원분산분석(F가 클수록 차이 큼)
print(f"[ANOVA] 소득그룹별 기대수명  F={F:.0f}  p={p2:.1e}")"""),
    md("🔁 **STATA**: `ttest life_exp, by(ssa) unequal`  ·  `oneway life_exp income_n`  ·  코드 → `stata/03_group_compare.do`"),
    md("""## 3) 회귀분석 — Preston 곡선 (소득 → 기대수명)
**회귀** = 한 변수(기대수명)를 다른 변수(소득)로 설명하는 직선/곡선을 찾는 것. 1인당 GDP는 왜도가
크므로 **로그**를 취한다 — AI가 자동으로 안 할 수 있는 **설계 판단**.

> **출력 읽는 법**: `coef`=기울기(log소득 1↑당 수명 변화), `P>|t|`<0.05면 유의, `R²`=설명력(0~1)."""),
    code("""# "life_exp ~ log_gdp" = 기대수명을 log소득으로 설명. ols=최소제곱법, .fit()=계수 추정
m = smf.ols("life_exp ~ log_gdp", data=df).fit()
print(m.summary().tables[1])      # 계수표: coef(기울기)·std err(오차)·P>|t|(유의확률)
print(f"\\nR² = {m.rsquared:.3f}")  # 설명력(0~1): 소득이 기대수명 변동의 몇 %를 설명하나"""),
    md("""**해석**: `log_gdp` 계수가 **양수** → 소득이 높을수록 기대수명↑. (소득이 e배면 ≈ +계수 만큼 수명)
R²가 높아 소득만으로 기대수명 차이의 상당 부분이 설명된다.

🔁 **STATA**: `regress life_exp log_gdp` — **한 줄**.  코드 → `stata/04_regression.do`
> 양쪽 계수·R²가 같은지 **교차검증**: 같으면 신뢰, 다르면 하나가 틀린 것."""),
    md("""---
✅ **핵심**: 교차표·검정·회귀를 입문자가 첫날 직접 돌렸다. 비결은 *문법 암기*가 아니라
*무엇을·왜 분석할지 설계*하고 *검증·해석*하는 것."""),
])

# ════════════════════════ 03 · 이원 고정효과 (고급 인과추론) ════════════════════════
write_nb("03_panel_fe.ipynb", [
    md(f"""# 03 · 고급 분석: 패널 고정효과  (모듈 4-A)
{badge("03_panel_fe.ipynb")}

> 고급 계량 분석도 AI 도움으로 **양쪽 도구에서** 할 수 있다. 국가×연도 패널의 고정효과를
> Python으로, 그리고 STATA로 — **둘 다 같은 결과**. 도구는 우열이 아니라 **환경**으로 고른다."""),
    md("""## 0) 준비 — 패널 전용 라이브러리 설치
`linearmodels`는 고정효과를 전용으로 다룬다(STATA `xtreg`에 해당). Colab엔 기본 없어 한 번만 설치."""),
    code('''# linearmodels = 패널(고정효과) 전용 라이브러리. Colab에 없으면 자동 설치(~20초)
try:
    import linearmodels
except ModuleNotFoundError:
    import subprocess, sys
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "linearmodels"]); import linearmodels'''),
    code(f'''import pandas as pd, numpy as np
from linearmodels.panel import PooledOLS, PanelOLS   # 패널 회귀(합동 · 고정효과)
df = pd.read_csv("{RAW}").dropna(subset=["gdp_pc","life_exp"])  # 불러오며 핵심 결측 제거
df["log_gdp"] = np.log(df["gdp_pc"])                            # 로그변환
# 패널 구조 선언: (개체=국가, 시간=연도) 2단 인덱스를 주면 linearmodels가 패널로 인식
panel = df.set_index(["economy", "year"])
print("국가:", df["economy"].nunique(), "· 연도:", df["year"].nunique(), "· 행:", len(df))  # 패널 규모'''),
    md("""## 문제 — 국가·시대의 교란을 통제하려면? (식별의 문제)
소득과 기대수명은 둘 다 **시간이 가며 함께 오른다.** 단순 상관엔 *국가 고유차*와 *전세계 시대추세*가
뒤섞여 있다. 진짜 효과를 보려면 이 둘을 **고정효과**로 걷어내야 한다 — 임팩트평가의 핵심 아이디어.

> **고정효과(FE)** = 국가/연도별 평균 차이를 통째로 빼는 것. `linearmodels`에선 `EntityEffects`(국가)·
> `TimeEffects`(연도)만 적으면 더미를 일일이 안 만들어도 흡수한다. (개념상 국가/연도 더미를 전부 넣는 것과 동일)"""),
    md("### (1) 통제 안 함 — 합동(pooled) 회귀"),
    code('''# (1) 아무것도 통제 안 함 — 모든 국가·연도를 한 덩어리로 ("1 +"은 절편 항)
pooled = PooledOLS.from_formula("life_exp ~ 1 + log_gdp", panel).fit()
print("pooled         log_gdp =", round(pooled.params["log_gdp"], 2))'''),
    md("### (2) 국가 고정효과 — 국가 고유차 통제"),
    code('''# (2) EntityEffects = 국가 고정효과(국가 고유차 흡수)
#     cluster_entity=True = 국가 단위 클러스터 표준오차(STATA vce(cluster)와 대응)
fe = PanelOLS.from_formula("life_exp ~ log_gdp + EntityEffects", panel)\\
             .fit(cov_type="clustered", cluster_entity=True)
print("국가 FE        log_gdp =", round(fe.params["log_gdp"], 2), "(국가 고유효과 흡수)")'''),
    md("""### (3) **이원 고정효과** — 국가 + 연도 동시 통제 (고급)
연도 고정효과(`TimeEffects`)까지 더하면 전세계 공통 **시대추세**가 빠지며 효과가 또 달라진다."""),
    code('''# (3) + TimeEffects = 연도 고정효과 → 국가+연도 동시 통제(전세계 공통 시대추세 제거)
twfe = PanelOLS.from_formula("life_exp ~ log_gdp + EntityEffects + TimeEffects", panel)\\
               .fit(cov_type="clustered", cluster_entity=True)
print("이원 FE(+연도) log_gdp =", round(twfe.params["log_gdp"], 2), "(시대추세까지 흡수)")
print("\\n→ 4.59 → 3.54 → 1.26 : 무엇을 통제하느냐에 따라 답이 바뀐다(식별의 문제).")'''),
    md("""### (4) STATA에선 — 같은 분석
```stata
encode economy, gen(country_id)
xtset country_id year
xtreg life_exp log_gdp i.year, fe vce(cluster country_id)
```
- `xtreg ..., fe`가 `PanelOLS`의 `EntityEffects`에, `i.year`가 `TimeEffects`에 대응. base STATA — **폐쇄망에서 인터넷 없이 실행** ✅  코드 → `stata/05_panel_fe.do`
- 두 도구 계수가 **정확히 일치**(1.262)한다 — 교차검증.

---
✅ **포인트**: 이원 고정효과는 **차분-차분(DiD) 임팩트평가의 엔진**이다(KOICA M&E와 직결).
"무엇을 통제했나"가 결과를 좌우하므로 *설계·검증은 사람 몫* — AI는 코드를 짜고, 판단은 여러분이 한다."""),
])

# ════════════════════════ 04 · Python 고급: 라이브 수집 + 머신러닝 ════════════════════════
write_nb("04_python_strength.ipynb", [
    md(f"""# 04 · Python 고급: 라이브 수집 + 머신러닝  (모듈 4-B)
{badge("04_python_strength.ipynb")}

> **STATA로는 어려운** 두 가지를 Python으로: ① World Bank API에서 **실시간 데이터 수집**,
> ② **머신러닝**으로 예측·변수중요도. 수집·자동화·ML은 **Python의 영역**(외부망)이다."""),
    md("## 1) 라이브 API 수집 — 이 데이터가 만들어진 방식\n`wbgapi`로 World Bank에서 직접 가져온다(저장된 CSV가 아니라 라이브). 여러 지표를 한 번에 = 자동화."),
    code("""# World Bank 공식 API 패키지 불러오기 (Colab에 없으면 자동 설치)
try:
    import wbgapi as wb
except ModuleNotFoundError:
    import subprocess, sys
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "wbgapi"]); import wbgapi as wb
# 지표코드(GDP·기대수명) × 나라(한국·베트남·케냐·에티오피아) × 연도(2021)를 한 번에 수집
wb.data.DataFrame(["NY.GDP.PCAP.CD","SP.DYN.LE00.IN"], ["KOR","VNM","KEN","ETH"],
                  time=2021, columns="series", labels=False).round(1)"""),
    md("""## 2) 머신러닝 — 기대수명 예측 + 변수 중요도
"어떤 개발지표가 기대수명을 가장 잘 예측하나?"를 **랜덤포레스트**로 풀어본다.

- **머신러닝(ML)** = 규칙을 사람이 정하지 않고, 데이터에서 패턴을 *학습*해 예측하는 방법.
- **랜덤포레스트** = 수많은 '결정 트리'를 만들어 평균내는 모델. 비선형·상호작용도 잘 잡는다.
- **왜 train/test로 나누나** = 학습에 쓴 데이터로 평가하면 "외운 것"이라 점수가 부풀려진다.
  *안 본 데이터*로 평가해야 진짜 예측력을 안다(과적합 방지)."""),
    code(f'''import pandas as pd, numpy as np
from sklearn.ensemble import RandomForestRegressor      # 랜덤포레스트(여러 결정트리의 앙상블)
from sklearn.linear_model import LinearRegression       # 비교용 선형회귀
from sklearn.model_selection import train_test_split, cross_val_score
df = pd.read_csv("{RAW}").dropna(subset=["gdp_pc","life_exp","prim_enroll"]).copy()
df["log_gdp"] = np.log(df["gdp_pc"]); df["log_pop"] = np.log(df["pop"])
# X = 예측에 쓸 입력변수들. 문자형(지역·소득그룹)은 get_dummies로 0/1 더미화(drop_first=중복 제거)
X = pd.get_dummies(df[["log_gdp","log_pop","prim_enroll","region_name","income_name"]], drop_first=True)
y = df["life_exp"]                                       # y = 맞히려는 목표(기대수명)
print("특성:", X.shape[1], "개 · 표본:", len(y))'''),
    md("### train/test 분할 + 교차검증 — '예측력'을 정직하게 평가"),
    code("""# 데이터를 학습용 75% / 평가용 25%로 분할 (random_state=난수 고정 → 매번 같은 결과)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42)
rf  = RandomForestRegressor(n_estimators=300, random_state=42).fit(Xtr, ytr)  # 트리 300개로 학습
ols = LinearRegression().fit(Xtr, ytr)                                        # 비교용 선형회귀 학습
# .score = 평가용(학습에 안 쓴) 데이터에서의 R²(예측력). 1에 가까울수록 좋음
print(f"랜덤포레스트  test R² = {rf.score(Xte, yte):.3f}")
print(f"선형회귀(OLS) test R² = {ols.score(Xte, yte):.3f}   ← RF가 비선형을 더 잘 잡음")
print(f"랜덤포레스트  5-fold 교차검증 R² = {cross_val_score(rf, X, y, cv=5).mean():.3f}")  # 5번 나눠 평균(더 보수적)"""),
    md("### 변수 중요도 — 무엇이 기대수명을 가장 잘 예측하나?"),
    code("""# 변수 중요도 = 랜덤포레스트가 예측에 각 변수를 얼마나 활용했나(클수록 중요). 상위 6개
pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False).head(6).round(3)"""),
    md("""---
✅ **포인트**: 수집·자동화·머신러닝은 **Python의 영역**(STATA는 사실상 못 함). 입문자도 AI 도움으로
랜덤포레스트·교차검증을 돌린다 — 단, **train/test로 정직하게 평가**하고 결과를 **검증**하는 건 사람 몫.

🧭 **인간 검증**: 변수중요도 1위가 현장 감각과 맞나? '예측을 잘한다'를 *인과(원인)*로 오해하지 않았나?"""),
])

# ════════════════════════ 05 · 인간의 검증력 (시각화) ════════════════════════
write_nb("05_human_verification.ipynb", [
    md(f"""# 05 · 인간의 검증력: 시각화로 오류 잡기  (모듈 5)
{badge("05_human_verification.ipynb")}

> AI가 만든 "그럴듯한 분석"을 **인간의 3대 무기 — 🖼️시각화 · 🧭도메인 지식 · 👥동료 회람**으로 검증한다.
> AI는 빠르지만 *보지 못하고, 맥락이 없고, 혼자* 일한다."""),
    code(FONT_SETUP),
    code(f'''import pandas as pd, numpy as np, matplotlib.pyplot as plt   # plt = 그래프 그리기
df = pd.read_csv("{RAW}").dropna(subset=["gdp_pc","life_exp"]).copy()
df["log_gdp"] = np.log(df["gdp_pc"])'''),
    md("""## 시나리오 — "소득이 높을수록 기대수명이 길다"
AI에게 분석을 시켰더니 상관계수를 줬다. **숫자만 보면 완벽해 보인다.**"""),
    code("""# 상관계수 = 두 변수가 함께 움직이는 정도(-1~1, 1에 가까울수록 강한 양의 관계)
print("상관계수(log소득 vs 기대수명):", round(df["log_gdp"].corr(df["life_exp"]), 3))"""),
    md("""### 🖼️ 무기 1 — **그려본다**
현업 데이터엔 입력 오류가 섞이기 쉽다. 한 나라의 1인당 GDP가 **단위 실수로 1,000배** 잘못
입력됐다고 하자(흔한 오류). 숫자로는 안 보이지만 **그리면** 바로 드러난다."""),
    code("""dirty = df.copy()                                              # 오류를 심을 복사본
idx = dirty.index[dirty["economy"].eq("VNM") & dirty["year"].eq(2021)]  # 베트남 2021년 행의 위치
dirty.loc[idx, "gdp_pc"] = dirty.loc[idx, "gdp_pc"] * 1000      # 단위 실수 모사: GDP를 1,000배로
dirty["log_gdp"] = np.log(dirty["gdp_pc"])                      # 로그 다시 계산

fig, ax = plt.subplots(1, 2, figsize=(11, 4))                  # 그래프 2개를 가로로 나란히
# 산점도(scatter): 점 하나 = 한 나라-연도. s = 점 크기
ax[0].scatter(dirty["log_gdp"], dirty["life_exp"], s=8); ax[0].set_title("AI가 받은 데이터(오류 포함)")
ax[1].scatter(df["log_gdp"], df["life_exp"], s=8, c="green"); ax[1].set_title("정상")
for a in ax: a.set_xlabel("log(1인당 GDP)"); a.set_ylabel("기대수명")  # 두 그래프 축 라벨
plt.tight_layout(); plt.show()                                 # 여백 정리 후 화면에 표시"""),
    md("→ 왼쪽 그림에 **오른쪽으로 멀리 튄 점**이 한눈에. 표의 숫자만 봤다면 회귀가 왜곡됐을 것이다."),
    code("""# 범인 찾기: GDP가 높은 순으로 정렬해 비정상적으로 부유해 보이는 나라-연도 확인
sus = dirty.sort_values("gdp_pc", ascending=False).head(3)   # 내림차순 상위 3개
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
