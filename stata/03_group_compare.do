*===============================================================================
* 03_group_compare.do  ·  집단 비교: t검정 + ANOVA (모듈 3)
* base STATA · v14+ · 오프라인.  ⚠ 폐쇄망 STATA에서 실행 확인 권장.
*  → Python 대응: notebooks/02_core_analysis.ipynb 의 ttest_ind / f_oneway
*===============================================================================
version 14
if "$csv"=="" global csv "sample_crs.csv"
import delimited "$csv", clear varnames(1)
rename *, lower

* ── t검정: 무상(Grant) vs 유상(Loan) 평균 집행액 차이 ────────────────────────
ttest usd_disbursement, by(financetype)
* └ financetype 은 두 값(Grant/Loan)뿐이라 by()에 바로 사용 가능

* ── ANOVA: 분야 간 평균 집행액 차이 ──────────────────────────────────────────
encode sectorname, gen(sector_n)               // 문자열 분야 → 숫자 코드(ANOVA용)
oneway usd_disbursement sector_n, tabulate
* └ 사후비교가 필요하면:  oneway usd_disbursement sector_n, bonferroni
