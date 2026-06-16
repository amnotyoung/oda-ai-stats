*===============================================================================
* 05_panel_fe.do  ·  국가 고정효과 패널 — 고급 분석 (모듈 4-A)
* base STATA · v14+ · 오프라인.  ✅ Stata 19에서 실행 검증 완료(폐쇄망 MP에서도 동일).
*  → Python 대응: notebooks/03_panel_fe.ipynb (Python은 국가 더미를 다 넣어야 함)
*===============================================================================
version 14
if "$csv"=="" global csv "wdi_panel.csv"
import delimited "$csv", clear varnames(1)
rename *, lower

drop if missing(gdp_pc, life_exp)
gen log_gdp = ln(gdp_pc)

* ── 패널 선언: 국가(economy)×연도 ───────────────────────────────────────────
encode economy, gen(country_id)                 // 문자열 국가코드 → 숫자 패널 ID
xtset country_id year

* ── 고정효과 회귀 + 클러스터 강건표준오차: 단 한 줄로 끝 ─────────────────────
xtreg life_exp log_gdp, fe vce(cluster country_id)
* └ 200여 개 국가 고유효과를 xtreg,fe 가 흡수. Python에선 더미 213개를 직접 다뤄야 했다.

* ── 비교용: 고정효과 없는 합동(pooled) 회귀 ─────────────────────────────────
regress life_exp log_gdp
* 두 결과의 계수 변화를 보면 '국가 고유효과'가 통제됐음을 알 수 있다.
