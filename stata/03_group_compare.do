*===============================================================================
* 03_group_compare.do  ·  집단 비교: t검정 + ANOVA (모듈 3)
* base STATA · v14+ · 오프라인.  ✅ Stata 19에서 실행 검증 완료(폐쇄망 MP에서도 동일).
*  → Python 대응: notebooks/02_core_analysis.ipynb 의 ttest_ind / f_oneway
*===============================================================================
version 14
* 데이터 자동 탐색(매 실행마다): 작업폴더에 wdi_panel.csv 있으면 로컬, 없으면 GitHub URL(외부망)
capture confirm file "wdi_panel.csv"
if _rc global csv "https://raw.githubusercontent.com/amnotyoung/oda-ai-stats/main/data/wdi_panel.csv"
else   global csv "wdi_panel.csv"
import delimited "$csv", clear varnames(1)
rename *, lower

* ── t검정: 사하라이남 아프리카 vs 그 외 (기대수명) ───────────────────────────
gen byte ssa = (region_name=="Sub-Saharan Africa")
label define ssalbl 0 "Other" 1 "Sub-Saharan Africa"
label values ssa ssalbl
* 두 집단 분산이 달라 Welch 검정(unequal) → Python의 equal_var=False 와 일치
ttest life_exp, by(ssa) unequal

* ── ANOVA: 소득그룹 간 기대수명 차이 ─────────────────────────────────────────
encode income_name, gen(income_n)              // 문자열 소득그룹 → 숫자 코드
oneway life_exp income_n, tabulate
