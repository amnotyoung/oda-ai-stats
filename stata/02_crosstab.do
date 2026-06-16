*===============================================================================
* 02_crosstab.do  ·  교차표(교차분석): 공여국 × 분야 (모듈 3)
* base STATA · v14+ · 오프라인.  ⚠ 폐쇄망 STATA에서 실행 확인 권장.
*  → Python 대응: notebooks/02_core_analysis.ipynb 의 pivot_table
*===============================================================================
version 14
if "$csv"=="" global csv "sample_crs.csv"
import delimited "$csv", clear varnames(1)
rename *, lower

* ── 건수 교차표 (공여국 × 분야) ──────────────────────────────────────────────
tabulate donorname sectorname

* ── 평균 집행액 교차표 ───────────────────────────────────────────────────────
table donorname sectorname, contents(mean usd_disbursement) format(%6.1f)
* └ 참고: STATA 17+ 에서는 다음 최신 문법도 가능
*    table (donorname) (sectorname), statistic(mean usd_disbursement)

* ── (선택) 분야별 비중(%) ────────────────────────────────────────────────────
* tabulate sectorname, sort
