# 🔗 PE-MFG Integration Map — 연동 구조

> **Version**: v1.0 | **Date**: 2026-04-27

---

## PE-7 자동화 연동 / PE-7 Automation Integration

```yaml
# pe7_daily_pipeline.yml 내 PE-MFG 호출 예시
- name: Run PE-MFG Prompt
  uses: ./.github/actions/prompt-runner
  with:
    prompt_id: PE-MFG
    domain: manufacturing
    phase: all
    ssot_notion_page: 34f55ed436f081498e16f75110c5d675
    e0n_validation: true
```

## PE-11 에이전트 라우팅 / Agent Routing

```javascript
// 도메인 분류 → 에이전트 선택
const DOMAIN_ROUTER = {
  'manufacturing': 'PE-MFG',
  'smart-factory': 'PE-MFG',
  'AI-integration': 'PE-MFG',
  'semiconductor': 'PE-ICD',
  'ic-design': 'PE-ICD',
  'strategy-analysis': 'SPU-001',
  'memory-architecture': 'PE-MEM'
};

// PE-11 Master Multi-Agent → 도메인 감지 → PE-MFG 자동 선택
```

## E-0N 자동 검증 연계 / E-0N Auto-Validation

```python
# PE-MFG 전용 E-0N 검증 규칙
PE_MFG_VALIDATION_RULES = {
    'E-07': {
        'check': lambda doc: all(k in doc for k in ['KPI', 'Phase', 'Risks']),
        'auto_fix': 'insert_template_sections'
    },
    'E-04': {
        'check': lambda doc: count_phases(doc) == 6,
        'auto_fix': 'add_missing_phases'
    }
}
```

## Notion ↔ GitHub SSOT 동기화

| 항목 | Notion | GitHub |
|------|--------|--------|
| 원본 시스템 프롬프트 | PE-MFG §A | applied-cases/PE-MFG/system_prompt.xml |
| 6단계 프레임워크 | PE-MFG §B | applied-cases/PE-MFG/deployment_steps.md |
| 연동 구조 | PE-MFG §C | applied-cases/PE-MFG/integration_map.md |
| KPI 대시보드 | PE-MFG §D | 이 파일 §KPI 섹션 |

---
*Last sync: 2026-04-27 | Next auto-sync: pe7_daily_pipeline 08:00 KST*
