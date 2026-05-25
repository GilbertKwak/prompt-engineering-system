# Vendor Map v1.2 — Optical Module & CPO Supplier Matrix

> **버전**: v1.2 | **생성일**: 2026-05-25 | **담당**: Global SCP Tracker  
> **변경 이력**: v1.1 → v1.2 — CPO(Co-Packaged Optics) 컬럼 신규 추가  
> **연계 DB**: Global SCP Tracker | **GitHub Actions**: `optical-monthly-scan.yml`

---

## 📋 벤더 맵 — 광학모듈 공급업체 매트릭스

| Vendor | Country | Tier | Product Category | Key Products | CPO Ready | CPO Roadmap | Main Customer | Revenue (FY25) | Risk Level | Notes |
|--------|---------|------|-----------------|--------------|-----------|-------------|---------------|----------------|------------|-------|
| II-VI (Coherent) | USA | T1 | Transceiver / CPO | 400G/800G OSFP, CPO Module | ✅ Yes | 2025 H2 GA | Nvidia, Meta | $4.7B | 🟡 Medium | CPO 선도 공급사, Nvidia GB200 NVL72 협력 |
| Lumentum | USA | T1 | Laser / EML | EML, VCSEL, Pump Laser | 🔵 Partial | 2026 Q1 | Coherent, II-VI | $1.6B | 🟢 Low | CPO용 EML 핵심 소재 공급 |
| Hisense Broadband | China | T2 | Transceiver | 400G/800G QSFP-DD | ❌ No | TBD | Huawei, ZTE | $0.8B | 🔴 High | BIS 규제 리스크, 대체 소싱 필요 |
| InnoLight | China | T2 | Transceiver | 400G/800G OSFP | ❌ No | 2026 H2 | Meta, Microsoft | $1.2B | 🔴 High | BIS Entity List 모니터링 중 |
| Accelink | China | T2 | Transceiver / Laser | 100G-400G, DWDM | ❌ No | TBD | China Telecom | $0.6B | 🔴 High | 내수 중심, 수출 규제 취약 |
| Fabrinet | Thailand | T1 | CM (Contract Mfg) | 광학모듈 위탁제조 | 🔵 Partial | 2025 H2 | Lumentum, Viavi | $2.4B | 🟡 Medium | CPO 시험생산 라인 구축 중 |
| Sumitomo Electric | Japan | T1 | Fiber / Component | SMF, MPO, Ribbon Fiber | ❌ No | TBD | 전 세계 통신사 | $3.1B | 🟢 Low | CPO 기판용 광섬유 핵심 공급 |
| Fujikura | Japan | T1 | Fiber / Connector | MPO, MTP, Fusion Splicer | ❌ No | TBD | 데이터센터 운영사 | $2.8B | 🟢 Low | 고밀도 연결 솔루션 강점 |
| Broadcom | USA | T1 | Silicon Photonics / ASIC | CPO Silicon Photonics IC | ✅ Yes | 2025 GA | Google, Meta | $51.6B | 🟢 Low | CPO IC 핵심 설계사, Tomahawk6 연동 |
| Intel (IFS/Mobileye) | USA | T1 | Silicon Photonics | Intel Silicon Photonics 400G | ✅ Yes | 2025 H2 | AWS, Microsoft | $53.1B | 🟡 Medium | CPO 실리콘 포토닉스 2세대 출시 예정 |
| Eoptolink | China | T2 | Transceiver | 100G-400G QSFP | ❌ No | TBD | China 통신사 | $0.4B | 🔴 High | BIS 리스크 모니터링 |
| Ranovus | Canada | T3 | CPO Engine | CPO ODIN Engine | ✅ Yes | 2025 Q3 | Nvidia, AWS | N/A (Private) | 🟡 Medium | CPO 스타트업, Nvidia 파트너십 |

---

## 🔵 CPO (Co-Packaged Optics) 컬럼 정의

| 컬럼명 | 설명 | 값 범위 |
|--------|------|--------|
| **CPO Ready** | 현재 CPO 제품 양산/샘플 출하 여부 | ✅ Yes / 🔵 Partial / ❌ No |
| **CPO Roadmap** | GA(General Availability) 예정 시기 | YYYY QN 또는 YYYY H1/H2 |

### CPO 기술 정의
- **Co-Packaged Optics (CPO)**: 광학 I/O를 네트워크 스위치 ASIC과 동일 패키지 내 집적하는 기술
- **기존 Pluggable 대비 전력 40~60% 절감**, 대역폭 밀도 4× 향상
- **주요 적용처**: AI 클러스터 (Nvidia NVL72, Google TPU Pod), 하이퍼스케일 데이터센터
- **표준화**: OIF CPO 2.0 (2025), 800G→1.6T CPO 로드맵 진행 중

---

## 📊 공급망 리스크 히트맵

| Risk Category | High 🔴 | Medium 🟡 | Low 🟢 |
|---------------|---------|----------|-------|
| **BIS/수출규제** | Hisense, InnoLight, Accelink, Eoptolink | — | — |
| **집중도 리스크** | China T2 (4개사) | Japan T1 (2개사) | USA T1 (4개사) |
| **CPO 전환 지연** | China T2 전체 | Fabrinet | Broadcom, Intel |
| **단일소싱 리스크** | EML (Lumentum 의존) | MPO (Fujikura/Sumitomo) | IC (Broadcom/Intel) |

---

## 🔄 업데이트 주기 및 자동화

- **자동 스캔**: `optical-monthly-scan.yml` — 매월 1일 09:00 KST
- **트리거 이벤트**: BIS Entity List 업데이트 / 분기 실적 발표 / CPO 로드맵 변경
- **연계 Notion DB**: Global SCP Tracker — 광학모듈 뷰 (View-OPT-01)
- **SSOT 정합성**: GitHub 버전 우선 → Notion 자동 반영

---

## 📅 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| **v1.2** | 2026-05-25 | CPO Ready / CPO Roadmap 컬럼 신규 추가 — 12개 공급업체 CPO 상태 초기 매핑 완료 |
| **v1.1** | 2026-05-10 | 광학모듈 전용 벤더 매트릭스 분리 — Tier 구분, 리스크 레벨 추가 |
| **v1.0** | 2026-04-20 | 최초 생성 — 글로벌 SCP Tracker 광학모듈 벤더 초안 |

---

> ✅ **[v1.2 | 2026-05-25 20:10 KST]** CPO 컬럼 추가 완료 — 12개 공급업체 CPO Ready/Roadmap 매핑 · BIS 리스크 히트맵 · optical-monthly-scan.yml 연동 설계 🟢
