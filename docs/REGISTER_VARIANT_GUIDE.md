# Variant 자동 등록 워크플로우 가이드 v2.1

> **워크플로우 파일**: `.github/workflows/register_variant.yml`  
> **스크립트**: `.github/scripts/register_variant.py`  
> **인덱스**: `prompts/jv_fund/VARIANT_INDEX.json`

---

## 개요

`register_variant.yml`은 Variant 파일(`prompts/**/variants/*.md`) push를 감지하여  
PE-1/PE-3 자동 검증 → VARIANT_INDEX.json 갱신 → 요약 Issue 생성을 완전 자동화합니다.

---

## 트리거 조건

| 트리거 | 조건 |
|---|---|
| **자동 (push)** | `prompts/**/variants/*.md` 파일이 `main` 브랜치에 push될 때 |
| **수동 (workflow_dispatch)** | GitHub Actions UI에서 수동 실행 |

---

## Job 구성

```
┌─ Job 1: detect-variants ──────────────────────────────────────┐
│  변경된 Variant 파일 목록 수집                                   │
└────────────────────────────────────────────────────────────────┘
         ↓
┌─ Job 2: validate-variants (PE-1 || PE-3 병렬) ───────────────┐
│  PE-1: 출처·연도·추정값 검증                                     │
│  PE-3: 반대 시나리오·리스크 섹션 검증                             │
└────────────────────────────────────────────────────────────────┘
         ↓
┌─ Job 3: update-index ─────────────────────────────────────────┐
│  VARIANT_INDEX.json 자동 갱신 + CHANGELOG.md 업데이트 + 커밋     │
└────────────────────────────────────────────────────────────────┘
         ↓
┌─ Job 4: create-summary-issue ─────────────────────────────────┐
│  등록 완료 요약 Issue 자동 생성 (label: variant-registration)    │
└────────────────────────────────────────────────────────────────┘
```

---

## Variant 파일 규격

### 필수 Frontmatter

```yaml
---
id: VARIANT_MY_NEW          # 고유 ID (대문자·언더스코어)
title: 내 Variant 제목
version: "1.0"
domain: JV-Fund             # JV-Fund | FU-Thermal | B-Star-eCO2 | AI-Infra | General
tags: [tag1, tag2]
description: 한 줄 설명
created_at: 2026-04-28
status: active
---
```

### PE-1 충족 조건

- `[출처: ...]` 또는 URL 링크 포함
- 수치 데이터에 연도 기재 (`2025년`, `2026년` 등)
- 추정값에 `(est.)` 태그

### PE-3 충족 조건

- 반대 시나리오 섹션 (`반대 시나리오`, `리스크 매트릭스`, `단점`, `대안` 등 키워드)

---

## 수동 실행 방법

### GitHub UI

1. `Actions` 탭 → `🧬 Variant Auto-Registration v2.1` 선택
2. `Run workflow` 클릭
3. 옵션 설정:
   - `variant_path`: 특정 파일 지정 또는 `all`
   - `dry_run`: `true`(검증만) / `false`(실제 등록)
   - `create_issue`: `true`/`false`

### CLI

```bash
# 특정 Variant 등록
gh workflow run register_variant.yml \
  -f variant_path="prompts/jv_fund/variants/variant_new.md" \
  -f dry_run=false \
  -f create_issue=true

# 전체 Variant 재스캔 (Dry-run)
gh workflow run register_variant.yml \
  -f variant_path=all \
  -f dry_run=true

# 로컬 스크립트 직접 실행 (검증만)
python .github/scripts/register_variant.py \
  --mode validate \
  --rule PE-1 \
  --files "prompts/jv_fund/variants/variant_new.md" \
  --output validation_result.json

# 로컬 스크립트 직접 실행 (등록)
python .github/scripts/register_variant.py \
  --mode register \
  --files "prompts/jv_fund/variants/variant_new.md" \
  --index prompts/jv_fund/VARIANT_INDEX.json \
  --output registration_result.json
```

---

## 신규 Variant 추가 절차 (SOP)

```bash
# 1. Variant 파일 생성
cp prompts/jv_fund/variants/variant_fu_series.md \
   prompts/jv_fund/variants/variant_NEW_DOMAIN.md
# frontmatter의 id, title, domain, description 수정

# 2. 로컬 검증 (선택)
python .github/scripts/register_variant.py \
  --mode validate --rule PE-1 \
  --files prompts/jv_fund/variants/variant_NEW_DOMAIN.md \
  --output /tmp/check.json

# 3. 커밋 & Push → 워크플로우 자동 실행
git add prompts/jv_fund/variants/variant_NEW_DOMAIN.md
git commit -m "feat(variant): 신규 Variant 추가 — NEW_DOMAIN"
git push origin main
# → register_variant.yml 자동 트리거
# → PE-1/PE-3 검증 → VARIANT_INDEX.json 갱신 → Issue 생성
```

---

## VARIANT_INDEX.json 스키마

```json
{
  "schema_version": "2.1",
  "updated_at": "ISO-8601",
  "total": 4,
  "variants": [
    {
      "id": "VARIANT_ID",
      "file": "상대 경로",
      "domain": "도메인",
      "version": "1.0",
      "title": "제목",
      "description": "설명",
      "tags": [],
      "registered_at": "ISO-8601",
      "status": "active",
      "pe1_passed": true,
      "pe3_passed": true
    }
  ]
}
```

---

## 관련 파일

| 파일 | 역할 |
|---|---|
| `.github/workflows/register_variant.yml` | 워크플로우 메인 |
| `.github/scripts/register_variant.py` | 검증·등록·CHANGELOG 스크립트 |
| `prompts/jv_fund/VARIANT_INDEX.json` | Variant 레지스트리 |
| `prompts/jv_fund/master_v3.md` | JV Fund Master Prompt v3 |
| `prompts/jv_fund/variants/` | Variant 파일 디렉터리 |
| `CHANGELOG.md` | 자동 갱신 변경 이력 |
