*===============================================================================
* 01_load_clean.do  ·  데이터 불러오기 + 구조 + 검증 + 정제 (모듈 2)
* base STATA · v14+ · 오프라인.  ✅ Stata 19에서 실행 검증 완료(폐쇄망 MP에서도 동일).
* ※ 출력이 좁게 줄바꿈되면 Results 창을 넓게/최대화하세요.
*===============================================================================
version 14
set more off

* ── 데이터 불러오기 (조용히 — 작업폴더에 있으면 로컬, 없으면 GitHub URL) ───────
quietly {
    capture confirm file "wdi_panel.csv"
    if _rc global csv "https://raw.githubusercontent.com/amnotyoung/oda-ai-stats/main/data/wdi_panel.csv"
    else   global csv "wdi_panel.csv"
    import delimited "$csv", clear varnames(1)
    rename *, lower
}

display _newline(1) as result "■ [1] 데이터 구조 (행·열·자료형)"
display as text          "   국가×연도 패널 — 한 행 = 한 나라의 한 해."
describe

display _newline(1) as result "■ [2] 결측 현황"
display as text          "   진짜 데이터라 일부 지표에 값이 빠져 있습니다(정상). 어디에 얼마나 빠졌나 확인."
misstable summarize

display _newline(1) as result "■ [3] 검증 — 음수 소득 · 요약통계"
display as text          "   소득(gdp_pc)이 0 이하면 오류. 아래 카운트가 0이어야 정상."
count if gdp_pc <= 0
summarize gdp_pc life_exp under5_mort pop prim_enroll

* ── 정제 + 파생변수 (조용히): 결측 제거, 소득·인구는 왜도 커서 로그변환 ────────
quietly {
    drop if missing(gdp_pc, life_exp)
    gen log_gdp = ln(gdp_pc)
    gen log_pop = ln(pop)
}

display _newline(1) as result "■ [4] 소득그룹별 평균 기대수명"
tabstat life_exp, by(income_name) statistics(n mean) columns(statistics)
display as text "   {bf:→ 해석:} 소득그룹이 높을수록 평균 기대수명↑ (저소득 ~58세 → 고소득 ~78세)."
