*===============================================================================
* 02_crosstab.do  ·  교차표: 지역 × 소득그룹 (모듈 3)
* base STATA · v14+ · 오프라인.  ✅ Stata 19에서 실행 검증 완료(폐쇄망 MP에서도 동일).
*  → Python 대응: notebooks/02_core_analysis.ipynb 의 crosstab
*===============================================================================
version 14
set more off

* ── 데이터 불러오기 + 국가 단위 집계 (조용히) ────────────────────────────────
quietly {
    capture confirm file "wdi_panel.csv"
    if _rc global csv "https://raw.githubusercontent.com/amnotyoung/oda-ai-stats/main/data/wdi_panel.csv"
    else   global csv "wdi_panel.csv"
    import delimited "$csv", clear varnames(1)
    rename *, lower
    bysort economy (year): keep if _n==1        // 지역·소득은 국가 속성 → 국가당 1행
}

display _newline(1) as result "■ 지역 × 소득그룹 — 국가 수 교차표"
display as text          "   각 지역에 어느 소득그룹 나라가 몇 개 있는지(국가 단위)."
tabulate region_name income_name
display as text "   {bf:→ 해석:} 저소득국 다수가 사하라이남에, 고소득국은 유럽·동아태 등에 분포."
