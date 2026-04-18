# AUTO_VALIDATE_RUN.md
> 관리자: Gilbert Kwak | 버전: v1.3 | 최종 업데이트: 2026-04-18

---

## 📋 실행 이력

### ✅ Run #2 — 2026-04-18 (KG 생성 후 --full 재실행)

```bash
# Step 1: KG 생성
python scripts/build_kg.py --input reports/ --output knowledge_graph.json

# Step 2: 전체 검증 재실행
python auto_validate.py --full --report-dir reports/ --kg knowledge_graph.json
```

| 검증 항목 | 상태 | 비고 |
|----------|------|------|
| `knowledge_graph.json` | ✅ 생성됨 | build_kg.py 실행으로 해소 |
| RCA-001 메타데이터 헤더 완전성 | ✅ PASS | title·date·version·status 필드 확인 |
| RCA-002 섹션 구조 일관성 | ✅ PASS | H2/H3 템플릿 순서 준수 |
| RCA-003 크로스 레퍼런스 (파일 존재) | ✅ PASS | 참조 대상 파일 실존 확인 |
| RCA-003 순환 참조 탐지 (KG) | ✅ PASS | 순환 참조 없음 |
| RCA-003 고립 문서 탐지 (KG) | ⚠️ WARN | orphan 노드 확인 필요 |
| RCA-004 언어 일관성 KO/EN | ✅ PASS | KO↔EN 섹션 수 일치 |
| KG-001 노드 연결도 | ✅ PASS | |
| KG-002 태그 클러스터 | ✅ PASS | |

**권장 후속 조치:**
```bash
# FAIL/WARN 항목만 필터링
python auto_validate.py --full --filter FAIL --export validation_report_20260418.csv

# KG 시각화
python scripts/visualize_kg.py --input knowledge_graph.json --output kg_viz.html
```

---

### ⚠️ Run #1 — 2026-04-18 (KG SKIP 상태)

| 항목 | 상태 | 비고 |
|------|------|------|
| `knowledge_graph.json` | ❌ SKIP | 파일 미존재 — KG 체크 전체 건너뜀 |
| `reports/` MD 파일 검증 | ✅ 실행됨 | RCA-001~004 규칙 적용 |
| RCA-003 순환 참조 탐지 | ❌ SKIP | KG 미존재로 심층 탐지 불가 |
| RCA-003 고립 문서 탐지 | ❌ SKIP | KG 미존재 |
| KG-001 / KG-002 | ❌ SKIP | KG 미존재 |

---

## 🔗 연동 페이지
- Notion: [🔧 RCA/CAPA 문제 해결 관리 시스템](https://www.notion.so/33d55ed436f081bfa2aeccc26f344de5)
- GitHub README: [docs/rca-capa/README.md](https://github.com/GilbertKwak/prompt-engineering-system/blob/main/docs/rca-capa/README.md)
