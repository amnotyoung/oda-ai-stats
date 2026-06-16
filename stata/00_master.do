*===============================================================================
* 00_master.do  ·  데이터 고급 통계 분석 실무 활용 (폐쇄망 STATA용)
*-------------------------------------------------------------------------------
* 사용법: 아래 ★ 'datadir'만 본인 폴더로 바꾸고 전체 실행(Do).
* 데이터: World Bank WDI 패널(국가×연도). 추가 패키지 없이 base STATA·v14+·오프라인.
* ✅ Stata 19에서 실행·교차검증 완료 (회귀·ANOVA·패널이 Python과 일치). 폐쇄망 MP에서도 동일.
*===============================================================================
clear all
set more off
version 14

* ★★★ 여기만 본인 환경에 맞게 수정 ★★★
global datadir "C:/wdi"                       // wdi_panel.csv 가 들어있는 폴더
global csv     "$datadir/wdi_panel.csv"

do 01_load_clean.do        // 모듈2  불러오기·정제·검증
do 02_crosstab.do          // 모듈3  교차표(지역 x 소득그룹)
do 03_group_compare.do     // 모듈3  지역 t검정 · 소득그룹 ANOVA
do 04_regression.do        // 모듈3  Preston 곡선 회귀(소득→기대수명)
do 05_panel_fe.do          // 모듈4A 국가 고정효과 패널

display "==== 전체 실행 완료 ===="
