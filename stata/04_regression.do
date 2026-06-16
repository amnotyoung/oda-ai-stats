*===============================================================================
* 04_regression.do  ·  배분 결정요인 회귀 (모듈 3)
* base STATA · v14+ · 오프라인.  ⚠ 폐쇄망 STATA에서 실행 확인 권장.
*  → Python 대응: notebooks/02_core_analysis.ipynb 의 statsmodels ols
*===============================================================================
version 14
if "$csv"=="" global csv "sample_crs.csv"
import delimited "$csv", clear varnames(1)
rename *, lower

* ── 왜도 확인 → 로그변환 정당화 (집행액은 소수 대형사업으로 우왜도) ──────────
summarize usd_disbursement, detail            // skewness 가 크면 로그변환

gen log_disb  = ln(usd_disbursement)
gen log_gdppc = ln(recipientgdppc)
gen log_pop   = ln(recipientpop)

* ── 회귀 (로그-로그): 1인당GDP·인구 → 집행액 ───────────────────────────────
regress log_disb log_gdppc log_pop
* 해석: log_gdppc 계수 음수 → 가난한 수원국일수록 배분액↑ / log_pop 양수 → 인구 많을수록↑
* └ 이분산이 걱정되면 강건표준오차:  regress log_disb log_gdppc log_pop, vce(robust)
