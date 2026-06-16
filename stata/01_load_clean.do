*===============================================================================
* 01_load_clean.do  ·  데이터 불러오기 + 구조 + 검증 + 정제 (모듈 2)
* base STATA · v14+ · 오프라인.  ✅ Stata 19에서 실행 검증 완료(폐쇄망 MP에서도 동일).
*===============================================================================
version 14
if "$csv"=="" global csv "wdi_panel.csv"       // 단독 실행 시 현재 폴더의 파일

* ── 불러오기 ──────────────────────────────────────────────────────────────────
import delimited "$csv", clear varnames(1)
rename *, lower                                 // 변수명 소문자 통일
describe

* ── 검증: 결측·이상치 (진짜 데이터는 결측이 있다) ─────────────────────────────
misstable summarize                             // under5_mort·prim_enroll 등 결측
count if gdp_pc <= 0                            // 음수/0 소득(있으면 안 됨)
summarize gdp_pc life_exp under5_mort pop prim_enroll

* ── 정제 + 파생변수(소득·인구는 왜도 커서 로그변환) ───────────────────────────
drop if missing(gdp_pc, life_exp)
gen log_gdp = ln(gdp_pc)
gen log_pop = ln(pop)

* ── 요약: 소득그룹별 평균 기대수명 ───────────────────────────────────────────
tabstat life_exp, by(income_name) statistics(n mean) columns(statistics)
