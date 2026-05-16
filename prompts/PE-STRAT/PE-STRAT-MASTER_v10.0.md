# 🧭 PE-STRAT-MASTER_v10.0 — 전략 통합 마스터 프롬프트

<!--
  pe-ip-id     : PE-STRAT-MASTER
  version      : v10.0
  status       : Active
  category     : PE-STRAT
  parent       : PE-IP > T-09
  created      : 2026-05-16
  notion_page  : https://www.notion.so/36255ed436f081a0b132d7dfb5e35d30
  pe3_threshold: 93
-->

---

## 메타데이터

| 항목 | 값 |
|------|----|
| 버전 | v10.0 |
| 상태 | Active |
| 카테고리 | PE-STRAT |
| 상위 경로 | PE-IP > T-09 |
| 생성일 | 2026-05-16 |
| PE-3 임계치 | 93 |

---

## 개요

PE-STRAT-MASTER v10.0은 전략 분석·신사업 평가·의사결정 지원을 위한 **통합 마스터 프롬프트**입니다.
PE-STR v1.0 라이브러리의 모든 체인(CHAIN-01~12)을 오케스트레이션하며,
T-09 생태계 내 PE-DD·PE-FIN·PE-CON·PE-INV와 직접 바인딩됩니다.

---

## 오케스트레이터 선언

```xml
<orchestrator id="PE-STRAT-MASTER" version="v10.0">
  <role>전략 통합 마스터 오케스트레이터</role>
  <chain_registry>CHAIN-01 CHAIN-02 CHAIN-03 CHAIN-04 CHAIN-05 CHAIN-06
                  CHAIN-07 CHAIN-08 CHAIN-09 CHAIN-10 CHAIN-11 CHAIN-12</chain_registry>
  <execution_mode>sequential | parallel | conditional</execution_mode>
  <downstream_binding>PE-DD PE-FIN PE-CON PE-INV PE-SEMI PE-DC PE-TECH-RE PE-PAT PE-MFG PE-BOARD</downstream_binding>
</orchestrator>
```

---

## 체인 구성 (CHAIN-01 ~ CHAIN-12)

| 체인 | 역할 | 다운스트림 바인딩 | 실행 모드 |
|------|------|------------------|-----------|
| CHAIN-01 | 시장 구조 분석 (TAM/SAM/SOM) | PE-DD, PE-FIN | sequential |
| CHAIN-02 | 경쟁사 포지셔닝 맵 | PE-CON, PE-STR | parallel |
| CHAIN-03 | MECE 전략 프레임 분해 | PE-7, PE-OPT | sequential |
| CHAIN-04 | 신사업 기회 탐색 (Blue Ocean) | PE-INV, PE-DD | conditional |
| CHAIN-05 | 리스크 폭포 분석 (Cascade) | PE-FIN, PE-MIN | sequential |
| CHAIN-06 | 포트폴리오 전략 최적화 | PE-INV, PE-CON | parallel |
| CHAIN-07 | 지정학·규제 리스크 스캐닝 | PE-SEMI, PE-DC | conditional |
| CHAIN-08 | M&A 전략 시나리오 | PE-DD, PE-BOARD | sequential |
| CHAIN-09 | ESG·지속가능 전략 통합 | PE-CON, PE-MFG | parallel |
| CHAIN-10 | 기술 로드맵·IP 전략 연계 | PE-TECH-RE, PE-PAT | sequential |
| CHAIN-11 | 의사결정 트리 자동생성 | PE-7, PE-OPT | conditional |
| CHAIN-12 | 전략 보고서 자동 구조화 | PE-IP 전체 | sequential |

---

## 실행 프로토콜

```xml
<execution_protocol>
  <step id="1">INPUT 수집 — 분석 대상 문서/데이터 로드</step>
  <step id="2">CHAIN 선택 — 목적에 따라 단일/전체 체인 지정</step>
  <step id="3">CHAIN 순차 실행 — downstream 바인딩 자동 라우팅</step>
  <step id="4">PE-3 자기검증 — 총점 93점 임계치 적용</step>
  <step id="5">출력 구조화 — CHAIN-12로 보고서 자동 생성</step>
  <step id="6">Notion 동기화 — pe-strat-report --output notion</step>
</execution_protocol>
```

---

## 자기검증 프로토콜

```xml
<self_validation>
  <rule id="SV-01">PE-3 총점 < 93 → 자동재생성 (max 2회)</rule>
  <rule id="SV-02">PE-3 < 95 → PE-OPT 자동트리거</rule>
  <rule id="SV-03">CHAIN 커버리지 < 80% → 누락 체인 강제 실행</rule>
  <rule id="SV-04">바인딩 오류 → PE-IP 인덱서 재동기화</rule>
  <rule id="SV-05">출력 구조 불완전 → CHAIN-12 재실행</rule>
</self_validation>
```

---

## 입력 바인딩

```xml
<input_binding>
  <accepts>전략 문서, IR Deck, 시장 리포트, M&A 제안서, 사업계획서</accepts>
  <format>PDF | DOCX | MD | JSON | 구조화 텍스트</format>
  <min_context>500 tokens</min_context>
  <max_context>200,000 tokens</max_context>
</input_binding>
```

---

## 출력 형식

```xml
<output_format>
  <primary>구조화 전략 보고서 (Markdown)</primary>
  <secondary>IC Memo | 의사결정 트리 | 리스크 매트릭스</secondary>
  <sync_target>Notion PE-IP 라이브러리 | GitHub prompts/PE-STRAT/</sync_target>
</output_format>
```

---

## Notion 동기화 설정

```xml
<notion_sync>
  <page_id>36255ed436f081a0b132d7dfb5e35d30</page_id>
  <url>https://www.notion.so/36255ed436f081a0b132d7dfb5e35d30</url>
  <parent>PE-IP > T-09</parent>
  <category>PE-STRAT</category>
  <version>v10.0</version>
  <status>Active</status>
</notion_sync>
```

---

## 명령어 허브 (CMD)

```bash
# 전략 분석 전체 실행
pe-strat-run --target [회사명/섹터] --chain all --version v10.0

# 단일 체인 실행
pe-strat-run --chain CHAIN-03 --input [전략문서]

# PE-3 검증
pe-ip-validate --target PE-STRAT-MASTER --threshold 93

# IC Memo 보고서 생성
pe-strat-report --format IC_MEMO --output notion

# 리스크 폭포 분석만
pe-strat-run --chain CHAIN-05 --input [리스크입력]
```

---

## 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| v10.0 | 2026-05-16 | CHAIN-10~12 신규 추가, GNN 연동 강화, PE-SEMI/PE-DC 바인딩 |
| v9.0 | 2026-04-28 | CHAIN-07~09 추가, ESG 모듈 통합 |
| v8.0 | 2026-03-15 | 초기 마스터 통합본 |
