*===============================================================================
* 05_panel_fe.do  ·  국가 고정효과 패널 — 고급 분석 (모듈 4-A)
* base STATA · v14+ · 오프라인.  ✅ Stata 19에서 실행 검증 완료(폐쇄망 MP에서도 동일).
*  → Python 대응: notebooks/03_panel_fe.ipynb (Python은 국가 더미를 다 넣어야 함)
*===============================================================================
version 14
* 데이터: 같은 폴더에 wdi_panel.csv 있으면 로컬, 없으면 GitHub URL에서 자동(외부망 실습)
if "$csv"=="" {
    capture confirm file "wdi_panel.csv"
    if _rc global csv "https://raw.githubusercontent.com/amnotyoung/oda-ai-stats/main/data/wdi_panel.csv"
    else   global csv "wdi_panel.csv"
}
import delimited "$csv", clear varnames(1)
rename *, lower

drop if missing(gdp_pc, life_exp)
gen log_gdp = ln(gdp_pc)

* ── 패널 선언: 국가(economy)×연도 ───────────────────────────────────────────
encode economy, gen(country_id)                 // 문자열 국가코드 → 숫자 패널 ID
xtset country_id year

* ── (1) 통제 없음: 합동(pooled) 회귀 ────────────────────────────────────────
regress life_exp log_gdp
* → log_gdp ≈ 4.59

* ── (2) 국가 고정효과: 국가 고유차(제도·기후 등) 통제 ───────────────────────
xtreg life_exp log_gdp, fe vce(cluster country_id)
* → log_gdp ≈ 3.54  (Python C(economy)와 동일)

* ── (3) 이원 고정효과: 국가 + 연도 동시 통제 (고급) ─────────────────────────
xtreg life_exp log_gdp i.year, fe vce(cluster country_id)
* → log_gdp ≈ 1.26 : 전세계 시대추세(i.year)까지 빼면 효과가 또 변한다 — 식별의 문제.
*   이원 고정효과 = 차분-차분(DiD) 임팩트평가의 엔진. Python과 계수 정확히 일치(1.262).
