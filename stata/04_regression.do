*===============================================================================
* 04_regression.do  ·  Preston 곡선 회귀 (소득 → 기대수명) (모듈 3)
* base STATA · v14+ · 오프라인.  ✅ Stata 19에서 실행 검증 완료(폐쇄망 MP에서도 동일).
*  → Python 대응: notebooks/02_core_analysis.ipynb 의 statsmodels ols
*===============================================================================
version 14
* 데이터 자동 탐색(매 실행마다): 작업폴더에 wdi_panel.csv 있으면 로컬, 없으면 GitHub URL(외부망)
capture confirm file "wdi_panel.csv"
if _rc global csv "https://raw.githubusercontent.com/amnotyoung/oda-ai-stats/main/data/wdi_panel.csv"
else   global csv "wdi_panel.csv"
import delimited "$csv", clear varnames(1)
rename *, lower

* 1인당 GDP는 왜도가 크다 → 로그변환
summarize gdp_pc, detail
gen log_gdp = ln(gdp_pc)

* ── 회귀: 소득(log) → 기대수명 ───────────────────────────────────────────────
regress life_exp log_gdp
* 해석: log_gdp 계수 양수 → 소득 높을수록 기대수명↑ (개발경제의 Preston 곡선)
* └ 이분산이 걱정되면 강건표준오차:  regress life_exp log_gdp, vce(robust)
