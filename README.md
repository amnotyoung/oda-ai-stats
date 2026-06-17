# 데이터 고급 통계 분석 실무 활용 — 실습 코드

> **AI로 통계 분석의 난이도를 낮춘다.** World Bank 개발지표(WDI)를
> **Python(Colab)**과 **STATA**로 분석하고, 각 도구의 쓰임과 **인간의 검증력**을 익힌다.

데이터는 World Bank 공식 API(wbgapi)로 받은 **진짜 데이터**다 — 국가×연도 개발지표 패널(2000~2022).

---

## 🧭 두 개의 환경 — 이 강의의 전제

| 외부망 (배우는 곳) | 폐쇄망 / air-gapped (일하는 곳) |
|---|---|
| AI · Python(Colab) 사용 가능 | 인터넷 X · AI X · Python X |
| **여기서 실습** (아래 Colab 배지 클릭) | **STATA O** — 현업은 여기서 |

**전략**: 외부망에서 AI·Python으로 빠르게 배우고 → **STATA `.do` 코드**를 내려받아 →
폐쇄망 STATA에서 **오프라인으로** 실행한다.

---

## 📽️ 발표 슬라이드 (39장)

강의 발표용 슬라이드(HTML · 16:9)를 [`slides/`](slides/)에 담았다.

- **보기**: 저장소를 내려받아 `slides/viewer.html`을 브라우저로 연다 — 39장을 한 번에 넘겨본다.
- **인터랙티브**: Preston 곡선 산점도·로그변환·고정효과 단계·이상치 검출 슬라이드는 클릭/호버로 동작한다.
- 개별 파일은 `slides/slide-01.html` … `slide-39.html`.

---

## 🚀 외부망 실습 — Colab에서 바로 열기 (설치 불필요)

| 모듈 | 노트북 | 열기 |
|---|---|---|
| 2 | 데이터 불러오기·정제 | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amnotyoung/oda-ai-stats/blob/main/notebooks/01_load_clean.ipynb) |
| 3 | 핵심 분석(교차표·검정·회귀) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amnotyoung/oda-ai-stats/blob/main/notebooks/02_core_analysis.ipynb) |
| 4-A | 이원 고정효과(고급 인과추론) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amnotyoung/oda-ai-stats/blob/main/notebooks/03_panel_fe.ipynb) |
| 4-B | 라이브 수집 + 머신러닝(Python 고급) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amnotyoung/oda-ai-stats/blob/main/notebooks/04_python_strength.ipynb) |
| 5 | 인간의 검증력(시각화) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/amnotyoung/oda-ai-stats/blob/main/notebooks/05_human_verification.ipynb) |

---

## 🖥️ 외부망 STATA 실습 (체험판 STATA + 인터넷)

STATA엔 Colab 같은 웹 실행기가 없지만, **각 모듈 `.do`를 URL로 바로 실행**하면 데이터가
자동으로 GitHub에서 로드된다 — 다운로드·경로설정 불필요. Stata 명령창(Command)에:

```stata
do "https://raw.githubusercontent.com/amnotyoung/oda-ai-stats/main/stata/04_regression.do"
```

- 각 `.do`는 **로컬에 wdi_panel.csv 있으면 로컬, 없으면 URL**에서 자동으로 데이터를 가져온다.
- 코드를 **읽으며** 배우려면: GitHub에서 그 `.do`를 복사 → Stata 편집기에 붙여넣고 실행.
- ⚠ **인터넷 필요**. 오프라인(폐쇄망)에선 아래 로컬 방식.
- ※ 외부망에선 모듈을 **하나씩** 실행하세요. `00_master.do`(일괄)는 로컬 파일이 필요해 외부망엔 부적합.

---

## 🏢 폐쇄망 적용 — STATA로 현업에 (오프라인)

1. 이 저장소를 **압축 다운로드**(`Code → Download ZIP`)하거나 `stata/` + `data/wdi_panel.csv`를 받는다.
2. 보안 반입 절차에 따라 폐쇄망으로 들고 들어간다.
3. `stata/00_master.do` 를 열어 맨 위 `global datadir` 만 본인 폴더로 바꾼다.
4. 전체 실행. 끝.

- 모든 `.do`는 **추가 패키지(SSC) 없이 base STATA**·**STATA 14 이상**에서 동작 → 인터넷 불필요.
- ✅ **Stata 19에서 실행·교차검증 완료** — 회귀·ANOVA·이원 고정효과(4.59→3.54→1.26)가 Python과 일치. 폐쇄망 MP에서도 동일.

---

## 🗂️ 저장소 구성

```
oda-ai-stats/
├─ notebooks/        외부망 Colab용 (Python)
│  ├─ 01_load_clean.ipynb          모듈2  불러오기·정제
│  ├─ 02_core_analysis.ipynb       모듈3  교차표·t검정/ANOVA·회귀
│  ├─ 03_panel_fe.ipynb            모듈4A 이원 고정효과(고급 인과추론)
│  ├─ 04_python_strength.ipynb     모듈4B 라이브 수집 + 머신러닝(Python 고급)
│  └─ 05_human_verification.ipynb  모듈5  인간 검증력(시각화)
├─ stata/            STATA 코드 (.do, base STATA · 데이터 로컬→URL 자동 탐색)
│  ├─ 00_master.do       ← 폐쇄망 로컬 일괄 실행
│  ├─ 01_load_clean.do  02_crosstab.do  03_group_compare.do
│  ├─ 04_regression.do  05_panel_fe.do
├─ data/
│  └─ wdi_panel.csv    World Bank WDI 패널(실데이터, 약 4,991행)
├─ handouts/
│  ├─ prompt_patterns.md        AI 분석 의뢰 프롬프트 패턴
│  └─ verification_checklist.md 인간의 3대 무기 검증 체크리스트
├─ scripts/          데이터·노트북 재생성용(강사용)
│  ├─ build_wdi_data.py     wbgapi로 WDI 패널 재생성
│  └─ build_notebooks.py
└─ slides/           발표 슬라이드 (HTML 39장 · viewer.html · 일부 인터랙티브)
```

| 분석 | Python(Colab) | STATA(폐쇄망) |
|---|---|---|
| 교차표(지역×소득) | `02_core_analysis` | `02_crosstab.do` |
| t검정·ANOVA | `02_core_analysis` | `03_group_compare.do` |
| 회귀(Preston 곡선) | `02_core_analysis` | `04_regression.do` |
| 이원 고정효과(국가+연도) | `03_panel_fe` | `05_panel_fe.do` |
| 라이브 수집 + 머신러닝 | `04_python_strength` | *(STATA로는 어려움 — Python 영역)* |

---

## 📊 데이터 컬럼 (wdi_panel.csv)

`economy`(국가코드), `name`(국가명), `year`(연도), `region_name`(지역), `income_name`(소득그룹),
`gdp_pc`(1인당 GDP, 현재 US$), `life_exp`(기대수명, 세), `under5_mort`(5세 미만 사망률),
`pop`(인구), `prim_enroll`(초등 취학률 % gross).

> 출처: World Bank World Development Indicators. 재생성: `python scripts/build_wdi_data.py` (wbgapi 필요).
