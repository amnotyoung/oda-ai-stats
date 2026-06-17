*===============================================================================
* lecture_start.do  ·  외부망 실습 시작 (STATA 체험판 + 인터넷)
*-------------------------------------------------------------------------------
* 이 파일을 "한 번만" 실행하면, 이후 모듈들이 데이터를 GitHub에서 직접 불러옵니다.
*   → 데이터 다운로드 X · 작업폴더 설정 X  (Colab처럼 바로 실습)
*
* 실행법(Stata 명령창에 붙여넣기):
*   do "https://raw.githubusercontent.com/amnotyoung/oda-ai-stats/main/stata/lecture_start.do"
* 그다음 각 모듈을, 예:
*   do "https://raw.githubusercontent.com/amnotyoung/oda-ai-stats/main/stata/04_regression.do"
*
* ※ 폐쇄망(인터넷 없음)에서는 이 파일 대신, 로컬 파일 방식인 00_master.do 를 쓰세요.
*===============================================================================
global csv "https://raw.githubusercontent.com/amnotyoung/oda-ai-stats/main/data/wdi_panel.csv"
display _newline(1) "= 외부망 실습 준비 완료 — 데이터 출처:"
display "  $csv"
display "이제 각 모듈 .do 를 복사해 붙여넣거나, do 명령(URL)으로 실행하세요."
