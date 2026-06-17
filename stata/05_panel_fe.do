*===============================================================================
* 05_panel_fe.do  ·  국가 고정효과 패널 — 고급 분석 (모듈 4-A)
* base STATA · v14+ · 오프라인.  ✅ Stata 19에서 실행 검증 완료(폐쇄망 MP에서도 동일).
*  → Python 대응: notebooks/03_panel_fe.ipynb (linearmodels PanelOLS — EntityEffects+TimeEffects)
*===============================================================================
version 14
set more off

* ── 데이터 + 패널 선언 (조용히) ──────────────────────────────────────────────
quietly {
    capture confirm file "wdi_panel.csv"
    if _rc global csv "https://raw.githubusercontent.com/amnotyoung/oda-ai-stats/main/data/wdi_panel.csv"
    else   global csv "wdi_panel.csv"
    import delimited "$csv", clear varnames(1)
    rename *, lower
    drop if missing(gdp_pc, life_exp)
    gen log_gdp = ln(gdp_pc)
    encode economy, gen(country_id)             // 문자열 국가코드 → 숫자 패널 ID
    xtset country_id year
}
display _newline(1) as text "무엇을 통제하느냐에 따라 '소득 효과'가 어떻게 변하는지 3단계로 봅니다(식별의 문제)."

display _newline(1) as result "■ [1] 통제 없음 — 합동(pooled) 회귀"
regress life_exp log_gdp
display as text "   {bf:→} 소득 계수 = " as result %4.2f _b[log_gdp]

display _newline(1) as result "■ [2] 국가 고정효과 — 국가 고유차(제도·기후 등) 통제"
xtreg life_exp log_gdp, fe vce(cluster country_id)
display as text "   {bf:→} 소득 계수 = " as result %4.2f _b[log_gdp] as text "  (국가 차이를 빼니 줄어듦)"

display _newline(1) as result "■ [3] 이원 고정효과 — 국가 + 연도 동시 통제 (고급)"
xtreg life_exp log_gdp i.year, fe vce(cluster country_id)
display as text "   {bf:→} 소득 계수 = " as result %4.2f _b[log_gdp] as text "  (전세계 시대추세까지 제거)"
display as text "   {bf:→ 해석:} 4.59 → 3.54 → 1.26 으로 줄어듦 = 교란을 걷어낼수록 순효과에 근접. 이원 FE = DiD 임팩트평가의 엔진."
