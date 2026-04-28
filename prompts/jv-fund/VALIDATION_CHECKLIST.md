# Global JV Fund Prompt — Validation Checklist

> **버전:** v1.0 | **날짜:** 2026-04-28  
> **적용 대상:** master_prompt_v3_optimized.md + domain_variants.md  
> **검증 엔진:** PE-1 (출처 명시) + PE-3 (반대 시나리오)

---

## ✅ PE-1 자동 검증 항목 (출처 명시 규칙)

### 데이터 품질
- [ ] 모든 시장 규모 수치에 출처 및 연도 병기
  - 예: "AI 서버 시장 $200B (IDC, 2025)"
- [ ] 성장률(CAGR)은 예측 기관 및 예측 연도 범위 명시
  - 예: "CAGR 32% (2024-2030, Gartner 2024)"
- [ ] 추정값은 반드시 `(est.)` 표기
- [ ] 비교 데이터는 동일 기준 연도 사용
- [ ] 최소 3개 이상의 독립적 출처 인용

### 재무 데이터
- [ ] IRR/DPI/TVPI 추정치는 유사 사례(Comparable) 기반
- [ ] 환율 가정 명시 (USD/KRW/JPY 기준일 포함)
- [ ] 펀드 사이즈 가정의 산출 근거 기재

### 기술 데이터
- [ ] 기술 성숙도(TRL) 수준 명시
- [ ] 특허/IP 현황 확인 여부 기재
- [ ] 경쟁 기술 대비 성능 수치 출처 명시

---

## ✅ PE-3 자동 검증 항목 (반대 시나리오 규칙)

### 시나리오 완전성
- [ ] 낙관 시나리오 (Base + Bull) 각 1개 이상
- [ ] 비관 시나리오 (Bear + Stress) 각 1개 이상
- [ ] 각 시나리오별 핵심 가정 변수 명시

### 리스크 커버리지
- [ ] 기술 리스크: 개발 지연/실패 시나리오
- [ ] 시장 리스크: 수요 부진/경쟁 심화 시나리오
- [ ] 규제 리스크: 한국/미국/EU 규제 변화
- [ ] 지정학 리스크: 한-미-중 공급망 재편 시나리오
- [ ] 파트너 리스크: 핵심 파트너사 이탈 시나리오

### 민감도 분석
- [ ] 핵심 가정 ±20% 변동 시 IRR 변화 테이블
- [ ] Break-even 분석 포함
- [ ] Exit 멀티플 범위 명시 (최소/기대/최대)

---

## ✅ 출력물 품질 체크

### 형식
- [ ] JSON 출력 구조 유효성 확인
- [ ] Notion 호환 MD 포맷 확인
- [ ] 한국어/영어 병기 완결성 확인
- [ ] 테이블 형식 비교 데이터 포함

### 내용
- [ ] Executive Summary 500자 이내 (KR)
- [ ] 다음 액션 3개 이상 명시
- [ ] LP-facing 문서 스타일 준수
- [ ] 투자 권유 언어 제외 확인

### 연계성
- [ ] 관련 레포 링크 유효성 확인
- [ ] FU 보고서 인용 번호 정확성 확인
- [ ] Notion 페이지 ID 최신 상태 확인

---

## 🔄 검증 실행 명령어

```bash
# 수동 검증 실행
python automation/auto_validate.py \
  --file prompts/jv-fund/master_prompt_v3_optimized.md \
  --rules PE-1,PE-3 \
  --output validation_report.json

# 전체 jv-fund 디렉터리 검증
python automation/auto_validate.py \
  --dir prompts/jv-fund/ \
  --rules PE-1,PE-3 \
  --output jv_fund_validation_report.json

# GitHub Actions 트리거 (push 시 자동 실행)
git push origin main  # → .github/workflows/prompt_validate.yml 자동 실행
```

---

## 📅 정기 검토 일정

| 주기 | 검토 항목 | 담당 |
|---|---|---|
| 월 1회 | 시장 데이터 최신화 여부 | Gilbert |
| 분기 1회 | 파생 프롬프트 성과 리뷰 | Gilbert |
| 반기 1회 | 전체 구조 재설계 검토 | Gilbert |
| 수시 | PE-1/PE-3 위반 즉시 수정 | Auto-Validate |

---

## 🔗 관련 파일

| 파일 | 역할 |
|---|---|
| `master_prompt_v3_optimized.md` | 최신 운영 프롬프트 |
| `master_prompt_v2_original.md` | 원본 보관본 |
| `domain_variants.md` | 도메인 특화 파생 프롬프트 |
| `../../automation/auto_validate.py` | 자동 검증 스크립트 |
| `../../CHANGELOG.md` | 전체 변경 이력 |
