*===============================================================================
* 01_load_clean.do  ·  데이터 불러오기 + 구조 + 검증 + 정제 (모듈 2)
* base STATA · v14+ · 오프라인.  ✅ Stata 19에서 실행 검증 완료(폐쇄망 MP에서도 동일).
* ※ 출력이 좁게 줄바꿈되면 Results 창을 넓게/최대화하세요.
*===============================================================================
version 14
set more off                                    // 출력 중간에 멈추지 않게(--more-- 끔)

* ── 데이터 불러오기 (조용히 — 작업폴더에 있으면 로컬, 없으면 GitHub URL) ───────
quietly {
    capture confirm file "wdi_panel.csv"
    if _rc global csv "https://raw.githubusercontent.com/amnotyoung/oda-ai-stats/main/data/wdi_panel.csv"
    else   global csv "wdi_panel.csv"
    import delimited "$csv", clear varnames(1)
    rename *, lower                             // 변수명 소문자 통일
}

display _newline(1) "■ [1] 데이터 구조 (행·열·자료형)"
describe

display _newline(1) "■ [2] 결측 현황 — under5_mort·prim_enroll에 실제 결측"
misstable summarize

display _newline(1) "■ [3] 검증 — 음수 소득(0이어야 정상) · 핵심 변수 요약"
count if gdp_pc <= 0
summarize gdp_pc life_exp under5_mort pop prim_enroll

* ── 정제 + 파생변수 (조용히): 결측 제거, 소득·인구는 왜도 커서 로그변환 ────────
quietly {
    drop if missing(gdp_pc, life_exp)
    gen log_gdp = ln(gdp_pc)
    gen log_pop = ln(pop)
}

display _newline(1) "■ [4] 소득그룹별 평균 기대수명"
tabstat life_exp, by(income_name) statistics(n mean) columns(statistics)
