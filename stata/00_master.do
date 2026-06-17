*===============================================================================
* 00_master.do  ·  데이터 고급 통계 분석 실무 활용 (폐쇄망 STATA용)
*-------------------------------------------------------------------------------
* 데이터: World Bank WDI 패널. 추가 패키지 없이 base STATA·v14+·오프라인.
* ✅ Stata 19에서 실행·교차검증 완료 (회귀·ANOVA·패널이 Python과 일치). 폐쇄망 MP에서도 동일.
* ※ 이 파일은 폐쇄망(로컬 파일 일괄 실행)용. 외부망(인터넷) 실습은 각 모듈 .do 를
*    URL로 하나씩 실행하세요 — 예: do "https://raw.githubusercontent.com/amnotyoung/oda-ai-stats/main/stata/04_regression.do"
*===============================================================================
clear all
set more off
version 14

*━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
* ① 데이터(wdi_panel.csv) 위치 알려주기 — 둘 중 하나만 하면 됩니다
*   (A) 가장 쉬움: wdi_panel.csv 와 이 .do 파일들을 "한 폴더"에 두고,
*       Stata 작업폴더를 그 폴더로 바꾼다 →  메뉴 File > Change working directory…
*       (또는 명령창에:  cd "C:/내폴더/경로" )   → 그러면 아래 datadir 은 비워둔 채 OK.
*   (B) 데이터가 다른 폴더면 datadir 에 그 폴더 "전체 경로"를 적는다 (슬래시는 / 사용).
*━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
global datadir ""        // 예) "C:/Users/hong/Desktop/wdi"   (A 방식이면 비워두기)

global csv "wdi_panel.csv"
if "$datadir" != "" global csv "$datadir/wdi_panel.csv"

* ── 데이터 파일이 있는지 먼저 확인 (없으면 친절한 안내 후 중단) ────────────────
capture confirm file "$csv"
if _rc {
    display as error "✗ wdi_panel.csv 를 찾지 못했습니다 → $csv"
    display as error "  해결 (A) 데이터와 .do를 한 폴더에 두고, File > Change working directory 로 그 폴더 지정"
    display as error "  해결 (B) 위 6번째 줄 datadir 에 데이터 폴더의 전체 경로를 입력 (슬래시는 /)"
    exit 601
}
display "✓ 데이터 확인: $csv"

*━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
* ② 모듈 순서대로 실행 (각 .do 는 이 폴더에 함께 있어야 함)
*━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
do 01_load_clean.do        // 모듈2  불러오기·정제·검증
do 02_crosstab.do          // 모듈3  교차표(지역 x 소득그룹)
do 03_group_compare.do     // 모듈3  지역 t검정 · 소득그룹 ANOVA
do 04_regression.do        // 모듈3  Preston 곡선 회귀(소득→기대수명)
do 05_panel_fe.do          // 모듈4A 국가 고정효과 패널

display "==== 전체 실행 완료 ===="
