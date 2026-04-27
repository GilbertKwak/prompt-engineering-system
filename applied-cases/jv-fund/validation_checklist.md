# JV Fund Prompt — Validation Checklist

> **Version:** v1.0 | **2026-04-27** | **Rules:** PE-1 / PE-3  
> **Applies to:** `master_prompt_v3.md` + all `variants/*.md`

---

## ✅ PE-1 체크리스트 (출처 및 정확성)

- [ ] 모든 수치 데이터에 출처 + 연도 명시 (예: `Bloomberg 2025`)  
- [ ] 추정값에 `(est.)` 표기  
- [ ] 보장 수익률 표현 전면 금지  
- [ ] Fiduciary 리스크 명시적 플래그  
- [ ] 규제 준수 체크포인트 기재 (AIFMD / SEC / 국내 자본시장법)  
- [ ] LP 정합성 리스크 명시

## ✅ PE-3 체크리스트 (시나리오 균형)

- [ ] Base / Bull / Bear 시나리오 3종 포함  
- [ ] 반대(Bearish) 시나리오 최소 1개 이상 병기  
- [ ] 지정학 리스크 별도 섹션 기재  
- [ ] 가정 사항 명시적으로 선언  
- [ ] 상반된 전문가 견해 병기

## ✅ 구조 품질 체크리스트

- [ ] 파라미터 `{DOMAIN}`, `{STAGE}`, `{LANG}` 모두 정의됨  
- [ ] Chain-of-Thought 8단계 완비  
- [ ] OUTPUT FORMAT JSON 스키마 유효  
- [ ] Notion 호환 마크다운 문법 사용  
- [ ] GitHub Issue 명령어 작동 확인

## ✅ Domain Variant 체크리스트

| Variant | PE-1 | PE-3 | 도메인 특화 | Notion 연동 |
|---|---|---|---|---|
| `fu_series_adapter.md` | [ ] | [ ] | [ ] FU 번호 연동 | [ ] |
| `bstar_eco2_prompt.md` | [ ] | [ ] | [ ] sCO2 파트너 매핑 | [ ] |
| `ai_infra_prompt.md`   | [ ] | [ ] | [ ] AI DC 공급망 | [ ] |

---

## 🔄 자동 검증 명령어

```bash
# 단일 파일 검증
python automation/auto_validate.py \
  --file applied-cases/jv-fund/master_prompt_v3.md \
  --rules PE-1,PE-3 \
  --output reports/validation_$(date +%Y%m%d).json

# 전체 JV Fund 프롬프트 일괄 검증
for f in applied-cases/jv-fund/**/*.md; do
  python automation/auto_validate.py --file "$f" --rules PE-1,PE-3
done
```

---

*v1.0 | 2026-04-27 | Gilbert Kwak*
