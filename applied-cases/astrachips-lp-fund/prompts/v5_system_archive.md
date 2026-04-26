# v5.0 — 시스템 아카이브 & SSOT 구축 프롬프트

> **작성일**: 2026-04-26  
> **프롬프트 유형**: 시스템 관리 (System Archiving)  
> **적용 프로젝트**: AstraChips AI Infrastructure Fund I — 전체 프롬프트 시스템

## 📥 프롬프트 원문 (2-step)

### Step 1 — 버전 정리
```
본 스페이스에서 적용한 모든 프롬프트를 버전별로 정리 출력
```

### Step 2 — SSOT 구축
```
프롬프트를 notion & github를 참조해서 가장 적합한 장소에 업데이트
(전체 시스템 및 보고서에 적합한 장소 검증 후,
향후 참조하기 용이하고 항상 활용할 수 있는 방안 구축)
```

## 🎯 의사결정 프레임 (적합 위치 선정)

| 기준 | GitHub | Notion |
|------|--------|--------|
| 역할 | SSOT, 버전 관리, CI/CD 연동 | 내부 허브, 빠른 참조, 링크 |
| 저장 단위 | .md 파일, 디렉토리 구조 | 페이지, 데이터베이스 |
| 변경 추적 | Git commit history | 버전 이력 섹션 |
| 접근성 | 개발자·자동화 친화 | 비개발자·팀 전체 |
| 업데이트 | 명시적 commit 필요 | 즉시 편집 가능 |

**결론**: GitHub = 원본 SSOT / Notion = 참조 허브 (양방향 링크 유지)

## 📐 최종 디렉토리 구조
```
prompt-engineering-system/
└── applied-cases/
    └── astrachips-lp-fund/
        ├── PROMPT_VERSION_HISTORY.md  ← 마스터 인덱스
        ├── prompts/
        │   ├── v1_output_definition.md
        │   ├── v2_one_pager_refinement.md
        │   ├── v3_tech_vc_lp.md
        │   ├── v4_hyperscaler_cvc.md
        │   └── v5_system_archive.md
        └── outputs/
            (산출물 파일 — 별도 commit 예정)
```

## 🔄 향후 유지보수 원칙
```
1. 새 프롬프트 버전 생성 시 → prompts/v{N}_*.md 파일 추가
2. PROMPT_VERSION_HISTORY.md 버전 요약표 업데이트
3. Notion PE 허브 버전 이력 섹션 업데이트 (링크)
4. 분기 1회 전체 재사용 가이드 검토·갱신
```
