# 글로벌 반도체 설계 서비스 기업 발굴 프로젝트

> **버전:** 2.0 | **최종 업데이트:** 2026-04-25  
> **상태:** 🟢 활성  
> **Notion 연동:** [PE-7 심층 프롬프트 v2.0](https://www.notion.so/34955ed436f081149dd6de25dba027d7)

---

## 📁 디렉터리 구조

```
semiconductor-design-service/
├── MASTER-v2.0.yaml              # 마스터 프롬프트 (YAML 구조화)
├── README.md                     # 본 파일
├── variants/
│   ├── VARIANT-A-v2.yaml         # 동남아·인도·아세안 특화
│   ├── VARIANT-B-v2.yaml         # TSMC DCA/VCA/CoWoS 파트너 한정
│   ├── VARIANT-C-v2.yaml         # 재무·투자·M&A 분석
│   ├── VARIANT-v2.1-EU.yaml      # 유럽 집중 탐색
│   ├── VARIANT-v2.2-RISCV.yaml   # RISC-V 전문 필터
│   └── VARIANT-v2.3-AI-ASIC.yaml # AI ASIC/NPU 전문
└── validation/
    └── PE-3-checklist-design-service.md  # PE-3 자동검증 체크리스트
```

---

## 🔑 핵심 개념

### 기업 유형 분류
| 유형 | 정의 | 예시 기업 |
|------|------|----------|
| **Type A** | 순수 설계 서비스 (Design House/ASIC) | Alchip, Faraday, Open-Silicon |
| **Type B** | TSMC/GF 공식 파트너 (DCA/VCA/CoWoS) | GUC, Alchip, PGC |
| **Type C** | EDA·SW 도구·IP 라이선스 | Flexcompute, AllSpice, Silvaco |
| **Type D** | 신흥 팹리스 (Post-Series-A) | Axelera AI, Blaize, Alif |

### 앵커 기업 (검증 기준점)
| 기업 | 유형 | 역할 |
|------|------|------|
| Alchip Technologies | B | TWSE 상장, TSMC DCA 최고 기준 |
| GUC (Global Unichip) | B | TSMC VCA/CoWoS 기준 |
| Faraday Technology | A | 순수 설계 서비스 기준 |
| Flexcompute | C | EDA/시뮬레이션 SW 기준 |
| AllSpice | C | 설계 협업 플랫폼 기준 |

---

## ⚡ 실행 방법

### 전체 탐색 (기본)
```
마스터 프롬프트 MASTER-v2.0.yaml 실행
→ D1 생성 후 PE-3 검증 실행
→ PASS 시 D2~D4 생성
```

### 특화 탐색 (변형)
```
목적에 맞는 VARIANT 파일 선택
→ extends 기반으로 마스터 상속
→ OVERRIDE 섹션 조건 추가 적용
→ PE-3 Layer 3 변형 정합성 검증
```

---

## 🔗 연동 시스템

| 시스템 | 위치 | 역할 |
|--------|------|------|
| **Notion PE-7** | [34955ed4...](https://www.notion.so/34955ed436f081149dd6de25dba027d7) | 메인 저장·실행 공간 |
| **Notion PE Hub v2.0** | [33955ed4...](https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b) | 3-Engine 허브 등록 |
| **Notion SSOT** | [f392046f...](https://www.notion.so/f392046f06ff491698ca249849f03a40) | 마스터 디렉터리 인덱스 |
| **GitHub (본 저장소)** | `prompt-engineering-system` | YAML 파일 버전 관리 |
| **GitHub (산출물)** | `global-semiconductor-ai-research` | D1~D4 결과물 저장 |

---

## 📋 변경 이력

| 버전 | 날짜 | 주요 변경 |
|------|------|-----------|
| v1.0 | 2026-04-24 | 최초 작성 (텍스트 서술식) |
| v2.0 | 2026-04-25 | YAML 구조화, 변형 A/B/C 수정, v2.1~v2.3 신규 추가, PE-3 체크리스트 추가 |
