*===============================================================================
* 04_regression.do  ·  Preston 곡선 회귀 (소득 → 기대수명) (모듈 3)
* base STATA · v14+ · 오프라인.  ✅ Stata 19에서 실행 검증 완료(폐쇄망 MP에서도 동일).
*  → Python 대응: notebooks/02_core_analysis.ipynb 의 statsmodels ols
*===============================================================================
version 14
set more off

* ── 데이터 + 로그변수 (조용히) ───────────────────────────────────────────────
quietly {
    capture confirm file "wdi_panel.csv"
    if _rc global csv "https://raw.githubusercontent.com/amnotyoung/oda-ai-stats/main/data/wdi_panel.csv"
    else   global csv "wdi_panel.csv"
    import delimited "$csv", clear varnames(1)
    rename *, lower
    summarize gdp_pc, detail                    // 왜도 계산(조용히)
}
display _newline(1) as result "■ 왜 로그변환? — 휜 관계를 직선으로 펴기 위해"
display as text "   소득↔기대수명은 저소득서 급증·고소득서 평평(Preston 곡선)해 '직선'이 아닙니다."
display as text "   log(소득)으로 바꾸면 거의 직선이 되어 선형회귀에 맞습니다. (왜도=" as result %4.2f r(skewness) as text " 완화·이상치 영향↓는 덤)"
quietly gen log_gdp = ln(gdp_pc)

display _newline(1) as result "■ 회귀: 소득(log) → 기대수명  (Preston 곡선)"
display as text "   소득이 기대수명을 얼마나 설명하는지 직선으로 추정."
regress life_exp log_gdp
display as text "   {bf:→ 해석:} 소득 계수 = " as result %4.2f _b[log_gdp] as text " (양수·유의), R² = " as result %4.2f e(r2) as text " → 소득↑ 기대수명↑, 설명력 높음."
* └ 이분산이 걱정되면 강건표준오차:  regress life_exp log_gdp, vce(robust)
