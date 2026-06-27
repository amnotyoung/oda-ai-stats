# 데이터 고급 통계 분석 실무 활용 — 강의 슬라이드덱

## Meta
- **Topic**: AI로 통계 분석의 난이도를 낮춘다 — 외부망에서 배우고, 폐쇄망 STATA로 현업 적용
- **Target Audience**: 사내 동료 (Python·STATA 모두 입문, 통계 기초 보유), 국제개발협력 실무자
- **Tone/Mood**: 기관/정책 진중 톤, 신뢰감 (Corporate Blue)
- **Style**: corporate-blue
- **Slide Count**: 40 slides (+slide-40 에필로그 "생각해보기") (수정 라운드 1 반영 — 신규 slide-33 "미다룬 기법" 삽입, 이후 34~39 시프트)
- **Aspect Ratio**: 16:9 (720pt × 405pt)
- **Source**: 강의안.md · 01_도입_python_vs_stata.md · 02_데이터_소개_WDI.md · github.com/amnotyoung/oda-ai-stats
- **밀도 정책**: slides-grab 디자인 토큰은 따르되 "one idea/텍스트 최소화"는 강의교재용으로 완화 — 코드 대조·표·수치를 충분히. dense 슬라이드와 statement/divider를 교차.

## Slide Composition

### 모듈 0 — 오프닝
- Slide 1 — Cover: 제목 "데이터 고급 통계 분석 실무 활용" / 부제 / WDI 실데이터 / 대상·180분
- Slide 2 — Statement: 도발("문법은 안 외운다") + 약속("폐쇄망 STATA 코드 꾸러미를 들고 귀환")
- Slide 3 — Diagram: 우리 회사의 두 환경 (외부망 ↔ 폐쇄망 air-gapped)
- Slide 4 — Content: 두 축 메시지 (①설계→생성→검증 ②인간의 3대 무기) + 학습성과

### 모듈 1 — Python vs STATA
- Slide 5 — Section Divider: 모듈 1
- Slide 6 — Content: 한 문장 차이 (전용 SW vs 범용 언어) + 공방/공구 비유
- Slide 7 — Code Compare: 같은 회귀, 두 세계 (regress 한 줄 ↔ statsmodels 조립)
- Slide 8 — Table: 7가지 실제 차이 (학습곡선 강조)
- Slide 9 — Content: 누가 어디서 쓰나 (분야 지도) + 개발협력 두 부족
- Slide 10 — Statement: 반전 — AI가 게임을 바꿨다 (도구 선택 기준 이동)
- Slide 11 — Table: 도입 한 장 요약 + 오늘의 전략

### 모듈 2 — 데이터 소개 + AI로 첫 분석
- Slide 12 — Section Divider: 모듈 2
- Slide 13 — Content: WDI란 (세계은행 개발지표)
- Slide 14 — Table: 오늘의 데이터 (217국×23년=4,991행) + 변수 10개
- Slide 15 — Statistics: 한 행 읽기 (에티오피아/베트남/한국) → Preston 곡선 예고
- Slide 16 — Content: 진짜 데이터라서 (결측·미분류)
- Slide 17 — Content: AI 분석 의뢰 프롬프트 (기본 골격)
- Slide 18 — Statement: ★폐쇄망 핵심 프롬프트
- Slide 19 — Code Compare: 불러오기·정제 (pandas ↔ STATA .do) + 첫 검증

### 모듈 3 — 같은 분석 양쪽으로
- Slide 20 — Section Divider: 모듈 3 (분석 3종 개요 + 교차검증 철학)
- Slide 21 — Code Compare: ① 교차표 (crosstab ↔ tabulate)
- Slide 22 — Code Compare: ② 집단비교 (t검정/ANOVA)
- Slide 23 — Statistics: ② 결과 해석 (F=1877, p값의 의미)
- Slide 24 — Content: ③ 회귀 설계 (왜 로그변환? 왜도)
- Slide 25 — Code Compare: ③ 회귀 코드+결과 (계수 4.59 / R² 0.68, 양쪽 일치)
- Slide 26 — Statement: 교차검증 정리 ("숫자는 같다, 출력만 다르다")

### 모듈 4 — 고급 분석: 인과추론 + ML
- Slide 27 — Section Divider: 모듈 4
- Slide 28 — Content: 4-A 식별의 문제 (소득·기대수명 동반 상승, 교란)
- Slide 29 — Statistics: 4-A 통제로 답이 바뀐다 (4.59→3.54→1.26 계단)
- Slide 30 — Code Compare: 4-A 코드 (xtreg+i.year ↔ PanelOLS EntityEffects+TimeEffects)
- Slide 31 — Content: 4-A 포인트 (이원FE = DiD 엔진, KOICA M&E)
- Slide 32 — Content: 4-B 라이브 수집 + 랜덤포레스트 (RF R²0.96 > OLS 0.82)
- Slide 33 — Table: 4-C 도구 선택은 환경·작업으로

### 모듈 5 — 인간의 검증력
- Slide 34 — Section Divider: 모듈 5
- Slide 35 — Statistics: 🖼️ 시각화로 잡기 (단위 1,000배 오류, before/after)
- Slide 36 — Content: 🧭 도메인 지식 + 👥 동료 회람
- Slide 37 — Table: 3대 무기 종합 (AI 약점 ↔ 인간 강점)

### 모듈 6 — 마무리
- Slide 38 — Closing: 핵심 3줄 + 코드 꾸러미(GitHub) + 폐쇄망 실행 + 다음 학습 + Q&A
