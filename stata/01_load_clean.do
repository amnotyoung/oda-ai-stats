*===============================================================================
* 01_load_clean.do  ·  데이터 불러오기 + 구조 파악 + 검증 + 정제 (모듈 2)
* base STATA · v14+ · 오프라인.  ✅ Stata 19에서 실행 검증 완료(폐쇄망 MP에서도 동일).
*===============================================================================
version 14
if "$csv"=="" global csv "sample_crs.csv"      // 단독 실행 시 현재 폴더의 파일 사용

* ── 불러오기 ──────────────────────────────────────────────────────────────────
import delimited "$csv", clear varnames(1)
rename *, lower                                 // 변수명 소문자 통일(USD_Disbursement→usd_disbursement)
describe

* ── 검증: 결측·이상치 (AI가 짠 코드라도 사람이 먼저 확인) ──────────────────────
misstable summarize                             // 컬럼별 결측
count if usd_disbursement <= 0                  // 0 이하 집행액(있으면 안 됨)
count if usd_commitment < usd_disbursement      // 약정 < 집행 (정의상 이상)
summarize usd_commitment usd_disbursement recipientgdppc recipientpop

* ── 정제 + 파생변수(금액은 왜도가 커서 로그변환) ──────────────────────────────
drop if missing(usd_disbursement, recipientgdppc, recipientpop)
drop if usd_disbursement <= 0
gen log_disb  = ln(usd_disbursement)
gen log_gdppc = ln(recipientgdppc)
gen log_pop   = ln(recipientpop)

* ── 빠른 요약: 분야별 사업 건수·평균 집행액 ──────────────────────────────────
tabstat usd_disbursement, by(sectorname) statistics(n mean) columns(statistics)

* (선택) 정제본 저장 → 02~05에서 재사용하고 싶으면 주석 해제
* save "$datadir/crs_clean.dta", replace
