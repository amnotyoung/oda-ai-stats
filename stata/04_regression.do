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
display _newline(1) "■ 1인당 GDP 왜도(skewness) = " %5.2f r(skewness) "  → 크므로 로그변환"
quietly gen log_gdp = ln(gdp_pc)

display _newline(1) "■ 회귀: 소득(log) → 기대수명  (Preston 곡선)"
regress life_exp log_gdp
* 해석: log_gdp 계수 양수 → 소득 높을수록 기대수명↑.  R²=설명력.
* └ 이분산이 걱정되면 강건표준오차:  regress life_exp log_gdp, vce(robust)
