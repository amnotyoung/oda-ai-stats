*===============================================================================
* 03_group_compare.do  ·  집단 비교: t검정 + ANOVA (모듈 3)
* base STATA · v14+ · 오프라인.  ✅ Stata 19에서 실행 검증 완료(폐쇄망 MP에서도 동일).
*  → Python 대응: notebooks/02_core_analysis.ipynb 의 ttest_ind / f_oneway
*===============================================================================
version 14
set more off

* ── 데이터 + 그룹 변수 준비 (조용히) ─────────────────────────────────────────
quietly {
    capture confirm file "wdi_panel.csv"
    if _rc global csv "https://raw.githubusercontent.com/amnotyoung/oda-ai-stats/main/data/wdi_panel.csv"
    else   global csv "wdi_panel.csv"
    import delimited "$csv", clear varnames(1)
    rename *, lower
    gen byte ssa = (region_name=="Sub-Saharan Africa")   // 사하라이남=1, 그 외=0
    label define ssalbl 0 "Other" 1 "Sub-Saharan Africa"
    label values ssa ssalbl
    encode income_name, gen(income_n)                    // 문자열 소득그룹 → 숫자 코드
}

display _newline(1) as result "■ [1] t검정 — 사하라이남 vs 그 외 (기대수명)"
display as text          "   두 집단(2개)의 평균이 다른지 검정. 분산이 달라 Welch(unequal) 사용."
ttest life_exp, by(ssa) unequal
display as text "   {bf:→ 해석:} 두 지역 차이 ≈ " as result %3.1f (r(mu_1)-r(mu_2)) as text "세, p = " as result %5.3f r(p) as text " (<0.05면 통계적으로 유의)."

display _newline(1) as result "■ [2] ANOVA — 소득그룹 간 기대수명 차이"
display as text          "   3개 이상 집단(소득그룹 4개)의 평균이 다른지 검정."
oneway life_exp income_n, tabulate
display as text "   {bf:→ 해석:} F = " as result %6.0f r(F) as text ", p<0.05 → 소득그룹 간 기대수명 차이 유의."
