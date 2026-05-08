---
title: "🇸🇬 VCC-TAX-01 · Singapore VCC 세금 구조 상세 설계 v1.0"
domain: PE-INTL
linked: [SPV-04, SPV-KR-TAX, INTL-LEG-01, SPV-SUBSTANCE]
created: 2026-05-08
status: active
pe3_target: 93+
notion_id: 35a55ed4-36f0-8188-abe5-dea3f3dce3b9
notion_url: https://www.notion.so/35a55ed436f08188abe5dea3f3dce3b9
---

# 🇸🇬 VCC-TAX-01 · Singapore VCC 세금 구조 상세 설계 v1.0

> **도메인**: PE-INTL | **연계**: SPV-04 · SPV-KR-TAX · INTL-LEG-01  
> **작성일**: 2026-05-08 | **상태**: 🟢 Active | **PE-3 목표**: 93+

---

## 🎯 문서 목적

싱가포르 VCC(Variable Capital Company) 구조에서 한국 포트폴리오 투자 시 발생하는
원천세(WHT)를 최소화하는 Sub-Fund 설계 전략을 실무 기준으로 정의한다.

---

## 🏗️ 1. VCC 기본 법인 구조

| 항목 | 내용 |
|------|------|
| **근거법** | Variable Capital Companies Act 2018 (시행 2020.01) |
| **주식** | NAV 기준 발행·상환 가능 |
| **배당** | 자본에서 직접 지급 가능 |
| **회원 명부** | 비공개 (일반 Pte. Ltd.와 차별) |
| **Sub-Fund** | 단일 VCC 아래 복수 설치, 자산·부채 완전 분리 |
| **세무 처리** | VCC 전체 = 단일 법인 (법인세 신고서 1건) |

---

## 💰 2. 3대 세제 인센티브 Scheme (2026 현행)

| 구분 | S.13D (역외) | S.13O (거주자) | S.13U (강화등급) |
|------|-------------|--------------|----------------|
| 최소 AUM | 없음 | S$10M | S$50M |
| 현지 지출 | 없음 | S$200K/년 | S$500K/년 |
| 펀드매니저 | CMS 라이선스 | SG 소재 필수 | SG 소재 필수 |
| COR 발급 | 제한적 | ✅ 가능 | ✅ 가능 |
| 적합 대상 | 비거주자 통제 | 중형 PE/FO | 대형 기관 |
| **2025 개정** | — | AUM 티어제 도입 | AUM 티어제 도입 |

> ⚠️ 2025년 1월 1일부터 S.13O·13U의 Local Business Spending이 AUM 연동 티어제로 변경

---

## 📋 3. 면제 소득(Specified Income) 범위

- **자본이득**: 싱가포르 CGT 미도입 → 원천적 비과세
- **배당**: One-Tier System → 수취 주주 단계 면세
- **이자·금융소득**: 적격 펀드의 비거주자 이자 지급 WHT 면제
- **GST**: Sub-Fund 단위 GST Remission 적용

---

## 🇰🇷 4. 한-싱 조세조약 연동 WHT 최소화 핵심

| 소득 유형 | 한국 국내법 WHT | 조약 경감 세율 | 절감액 | 비고 |
|----------|--------------|-------------|------|----- |
| 배당 | 20% | 10% (지분 25%↑) / 15% (기타) | 최대 10%p | §10 |
| 이자 | 20% | 10% | 10%p | §11 |
| 로열티 | 20% | 15% | 5%p | §12 |
| 자본이득 (주식) | 10~25% | 0% (일반주식) | 최대 25%p | §13 |

> **조약 혜택 수령 조건**: COR(Certificate of Residence) 발급 선행 필수

---

## 🏢 5. Sub-Fund WHT 최소화 실전 구조

### 5-1. 권고 엄브렐라 구조

```
[한국 LP / 패밀리오피스]
         │
         ▼
[SG VCC Umbrella — S.13U 승인]
  ├─ Sub-Fund A: 한국 VC·PE 투자 (지분 25%+ 타겟 → 배당 WHT 10%)
  ├─ Sub-Fund B: 동남아 실물자산 (자본이득 WHT 0% 활용)
  └─ Sub-Fund C: 글로벌 상장주식 (이자·배당 혼합)
         │
         ▼
  [SG 소재 CMS 라이선스 펀드매니저]
```

### 5-2. Sub-Fund별 WHT 최적화 전략

#### Sub-Fund A — 한국 PE 투자
- 한국 피투자 법인 지분 **25% 이상** 취득 → 배당 WHT 10% (vs 국내법 20%)
- 엑싯 시 주식 양도차익 → 조약 §13 면제 (0%)
- CFC 리스크: Sub-Fund A 독립 Substance 증빙 필수
- 추천 투자 구조: SG VCC → KR OpCo 직접 지분 보유

#### Sub-Fund B — 동남아 실물자산
- SG 법인이 직접 보유 → 자본이득 비과세
- 임대 수익: SG 내 처리 → 유효세율 10~13% 구간
- 국가별 조세조약 활용 (SG는 90개국+ 조약 체결)

#### Sub-Fund C — 글로벌 상장
- S.13O/13U Specified Income 면제 범위 내 운용
- 비거주자 이자 지급 WHT 면제 구조 설계
- 포트폴리오 회전율 최소화 → 거래세 절감

### 5-3. 배당 지급 구조 최적화
- **One-Tier 배당**: SG VCC → 한국 LP 배당 시 추가 배당세 없음
- **한국 수취자 세무**: 외국납부세액공제(FTC) 적용 검토
- **지분율 관리**: 25% 기준선 유지 → 조약 §10(2)(a) 적용

---

## ✅ 6. Substance 요건 실무 체크리스트

- [ ] CMS 라이선스 보유 SG 펀드매니저 선임 (MAS 요건)
- [ ] SG 소재 독립 이사 1인 이상
- [ ] 연 2회 이상 이사회 SG 현지 개최 + 의사록 보관
- [ ] SG 소재 감사인(Auditor) 선임
- [ ] Sub-Fund별 별도 회계 기록 유지
- [ ] S$200K~500K/년 현지 사업 지출 (AUM 티어 연동)
- [ ] UBO 등록 (ACRA) + CRS 보고 이행
- [ ] COR 발급 신청 → IRAS 제출

---

## ⚡ 7. 한국 CFC 교차 리스크 매트릭스

| 리스크 항목 | 내용 | 대응 방안 |
|-----------|------|----------|
| 저율과세국 판정 | 실질 세율 ≈0% → CFC 저촉 가능 | Substance 증빙 + 실질활동 예외 주장 |
| 유보소득 합산과세 | 한국 주주 과세 | S.13U + Substance → 실질활동 예외 적용 |
| 조약 혜택 부인 (PPT) | BEPS PPT 테스트 미통과 | 사업 목적 문서화 + COR 유지 |
| 사전답변(Ruling) | 불확실성 해소 | 한국 국세청 Ruling 선제 취득 권고 |

---

## 📅 8. 실행 타임라인

| 시점 | 액션 | 담당 |
|-----|------|------|
| D+0~30 | VCC 설립 신청 + MAS 펀드매니저 계약 | SG 법무법인 |
| D+30~60 | S.13U 신청 + IRAS 제출 | SG 세무사 |
| D+60~90 | Sub-Fund 3종 설계 확정 + COR 신청 | CFO + 세무팀 |
| D+90~180 | 한국 CFC Ruling 신청 (선제) | 한국 세무사 |
| 연간 | Substance 증빙 갱신 + CRS 보고 | 운영팀 |

---

## 🔗 PE-INTL 연계 프롬프트

- **SPV-04**: Singapore Investment SPV 법적 리스크 → CFC·자본시장법 심화
- **SPV-KR-TAX**: 한국 세법 특화 (CFC·Outbound 배당)
- **INTL-LEG-01**: 아시아 3국 비교법 리스크 분석
- **SPV-SUBSTANCE**: Substance 요건 자동점검 체크리스트

---

> ⚠️ **면책 고지**: 본 문서는 정보 제공 목적이며 법률·세무 자문이 아닙니다.  
> 실제 구조 설계 전 SG 현지 법률사무소 및 IRAS 공인 세무사의 확인이 필요합니다.

---

*작성: Perplexity AI Assistant | 세션: 2026-05-08 | Notion SSOT: [VCC-TAX-01](https://www.notion.so/35a55ed436f08188abe5dea3f3dce3b9)*
