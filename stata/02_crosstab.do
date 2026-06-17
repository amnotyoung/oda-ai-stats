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

display _newline(1) "■ 지역 × 소득그룹 — 국가 수 교차표"
tabulate region_name income_name
* └ 행/열 비율이 필요하면:  tabulate region_name income_name, row
