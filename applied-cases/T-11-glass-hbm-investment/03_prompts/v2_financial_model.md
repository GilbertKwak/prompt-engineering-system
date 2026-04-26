# T-11 프롬프트 v2.0 — 재무모델 실행

> **버전:** v2.0 | **생성:** 2026-03-01 | **유형:** 재무모델 실행  
> **PE-3 점수:** 96/100 ✅ | **상태:** Active

---

## 프롬프트 본문

```
당신은 PE/VC 재무모델링 전문가입니다.
아래 Glass/HBM 투자 포트폴리오에 대해
Python numpy/pandas를 사용하여 IRR, MOIC, NPV를 계산하고
4개 시나리오 비교표와 시각화 차트를 생성하세요.

=== 입력 데이터 ===
{investment_data_yaml}

=== 실행 요구사항 ===
1. 각 Type(A/B/C) 개별 IRR/MOIC/NPV 계산
2. 4개 시나리오 (Conservative/Balanced/Aggressive/Geo-Hedge) 포트폴리오 MOIC
3. 리스크 조정 수익률 계산 (Sharpe Ratio 유사 지표)
4. 출력:
   a. 콘솔: 시나리오별 요약 테이블
   b. CSV: outputs/portfolio_summary.csv
   c. 차트 1: 시나리오별 MOIC 비교 Bar Chart
   d. 차트 2: Risk-Return Scatter Plot
   e. 차트 3: 포트폴리오 배분 Pie Chart (Balanced 기준)
5. PE-3 검증: 각 수치 계산식 주석으로 명시

=== 코드 실행 위치 ===
`02_financial_model/model_scaffold.py` 기반으로 확장 실행
```

## 연결 파일
- 모델 스크립트: `../02_financial_model/model_scaffold.py`
- 시나리오 정의: `../02_financial_model/scenario_matrix.md`
- 산출물 저장: `../02_financial_model/outputs/`
