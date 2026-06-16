*===============================================================================
* 05_panel_fe.do  ·  패널 고정효과 — STATA가 빛나는 분석 (모듈 4-A)
* base STATA · v14+ · 오프라인.  ⚠ 폐쇄망 STATA에서 실행 확인 권장.
*  → Python 대응: notebooks/03_panel_fe.ipynb (Python은 쌍 더미를 다 넣어야 함)
*===============================================================================
version 14
if "$csv"=="" global csv "sample_crs.csv"
import delimited "$csv", clear varnames(1)
rename *, lower

gen log_disb  = ln(usd_disbursement)
gen log_gdppc = ln(recipientgdppc)
gen log_pop   = ln(recipientpop)

* ── 패널 선언: 공여국-수원국 쌍(pair_id)을 패널 단위로 ───────────────────────
xtset pair_id
* └ 한 쌍·연도에 여러 분야 사업이 있어 '쌍 고정효과'만 선언(시간변수 미지정).
*   Python 노트북의 C(pair_id)와 동일한 모형.

* ── 고정효과 회귀 + 클러스터 강건표준오차: 단 한 줄로 끝 ─────────────────────
xtreg log_disb log_gdppc log_pop, fe vce(cluster pair_id)
* └ 60개 쌍의 고유효과를 xtreg,fe 가 알아서 흡수. Python에선 더미 59개를 직접 다뤄야 했다.

* ── 비교용: 고정효과 없는 합동(pooled) 회귀 ─────────────────────────────────
regress log_disb log_gdppc log_pop
* 두 결과의 계수 변화를 보면 '쌍 고유효과'가 통제됐음을 알 수 있다.
