*===============================================================================
* 03_group_compare.do  ·  집단 비교: t검정 + ANOVA (모듈 3)
* base STATA · v14+ · 오프라인.  ✅ Stata 19에서 실행 검증 완료(폐쇄망 MP에서도 동일).
*  → Python 대응: notebooks/02_core_analysis.ipynb 의 ttest_ind / f_oneway
*===============================================================================
version 14
if "$csv"=="" global csv "sample_crs.csv"
import delimited "$csv", clear varnames(1)
rename *, lower

* ── t검정: 무상(Grant) vs 유상(Loan) 평균 집행액 차이 ────────────────────────
* 두 집단 분산이 크게 다르므로(유상이 훨씬 큼) Welch 검정(unequal) → Python의 equal_var=False 와 일치
ttest usd_disbursement, by(financetype) unequal
* └ financetype 은 두 값(Grant/Loan)뿐이라 by()에 바로 사용 가능

* ── ANOVA: 분야 간 평균 집행액 차이 ──────────────────────────────────────────
encode sectorname, gen(sector_n)               // 문자열 분야 → 숫자 코드(ANOVA용)
oneway usd_disbursement sector_n, tabulate
* └ 사후비교가 필요하면:  oneway usd_disbursement sector_n, bonferroni
