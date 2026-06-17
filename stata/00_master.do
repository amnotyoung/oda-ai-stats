*===============================================================================
* 00_master.do  ·  데이터 고급 통계 분석 실무 활용 — 폐쇄망 일괄 실행
*-------------------------------------------------------------------------------
* 사용법: 이 .do 파일들과 wdi_panel.csv 를 "한 폴더"에 두고,
*         Stata 작업폴더를 그 폴더로 바꾼 뒤(File > Change working directory…) 실행.
* 외부망(인터넷) 실습은 이 파일 대신 각 모듈 .do 를 URL로 하나씩 실행하세요.
* base STATA·v14+·오프라인. ✅ Stata 19 검증 완료(Python과 일치). 폐쇄망 MP도 동일.
*===============================================================================
clear all
set more off
version 14

* ── 작업폴더 확인: 모듈 .do 가 현재 폴더에 있나? (없으면 작업폴더가 잘못된 것) ──
capture confirm file "01_load_clean.do"
if _rc {
    display as error "✗ 현재 작업폴더에서 모듈 .do 를 찾지 못했습니다."
    display as error "  → File > Change working directory 로, 이 파일들이 있는 폴더를 지정한 뒤 다시 실행하세요."
    exit 601
}

* ── 모듈 순서대로 실행 (각 .do 가 wdi_panel.csv 를 알아서 불러옴) ─────────────
do 01_load_clean.do        // 모듈2  불러오기·정제·검증
do 02_crosstab.do          // 모듈3  교차표(지역 x 소득그룹)
do 03_group_compare.do     // 모듈3  지역 t검정 · 소득그룹 ANOVA
do 04_regression.do        // 모듈3  Preston 곡선 회귀(소득→기대수명)
do 05_panel_fe.do          // 모듈4A 국가 고정효과 패널

display "==== 전체 실행 완료 ===="
