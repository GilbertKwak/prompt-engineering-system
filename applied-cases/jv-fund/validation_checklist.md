# JV Fund Prompt Validation Checklist v1.0

> **Version**: v1.0  
> **Date**: 2026-04-27  
> **Applies to**: master_prompt_v3.md + all domain variants  

---

## PE-1: 데이터 무결성 체크리스트

### 필수 항목
- [ ] 모든 수치 데이터에 출처 명시 (최소 3개 이상)
- [ ] 연도 기재 의무 (e.g. "2025년 기준", "2024E")
- [ ] 추정값 `(est.)` 또는 `(E)` 표기
- [ ] 보장 수익률 표현 금지 ("~할 것입니다" 대신 "예상됩니다")
- [ ] 시장 규모 수치: 최소 2개 독립 출처 교차 검증
- [ ] 재무 수치: 가정(Assumptions) 섹션 별도 명시

### 출처 신뢰도 등급
| 등급 | 유형 | 예시 |
|---|---|---|
| A (최우선) | 공식 기관 데이터 | Bloomberg, IEA, Gartner, IDC |
| B (우선) | 업계 보고서 | McKinsey, BCG, 산업부 |
| C (참고) | 언론/미디어 | Reuters, Nikkei |
| D (검증 필요) | AI 생성 데이터 | ⚠️ 반드시 교차 검증 |

---

## PE-3: 시나리오 균형 체크리스트

### 필수 항목
- [ ] Base Case 명시
- [ ] Bear Case 1개 이상 필수 포함
- [ ] Bull Case (선택, 단 근거 명시)
- [ ] 가정(Assumptions) 섹션 명시
- [ ] 상충 데이터 병기 (데이터 간 불일치 시)
- [ ] 수탁 리스크 플래그 (Fiduciary Risk)
- [ ] 규제 리스크 플래그
- [ ] LP 정합성 리스크 플래그

---

## 도메인별 추가 검증 항목

### HBM / Semiconductor
- [ ] TRL(기술 성숙도) 명시
- [ ] 특허 현황 확인
- [ ] 수출 규제 (반도체법, EAR) 리스크 플래그

### sCO2 / Energy
- [ ] 에너지 효율 수치 (효율 %, W/kg 등)
- [ ] 규제 인증 현황 (IEC, KS, ASME)
- [ ] 정부 보조금 의존도 리스크

### AI Infrastructure
- [ ] GPU 스펙 공식 출처 (NVIDIA, AMD 공식)
- [ ] PUE 수치 측정 기준 명시 (연간 평균 vs 최대값)
- [ ] AI 투자 싸이클 리스크 반영

---

## 자동 검증 명령어

```bash
# PE-1 검증 실행
python automation/auto_validate.py \
  --file applied-cases/jv-fund/master_prompt_v3.md \
  --rules PE-1,PE-3 \
  --output reports/jv_validation_$(date +%Y%m%d).json

# 전체 JV 프롬프트 배치 검증
for f in applied-cases/jv-fund/*.md; do
  python automation/auto_validate.py --file "$f" --rules PE-1,PE-3
done
```

---

## 리뷰 주기

| 주기 | 내용 | 담당 |
|---|---|---|
| 월 1회 | PE-1/PE-3 준수율 점검 | Gilbert |
| 분기 1회 | 도메인 데이터 최신화 | Gilbert |
| 신규 FU 보고서 발행 시 | FU-Series 연동 데이터 업데이트 | 자동 (GitHub Actions) |
