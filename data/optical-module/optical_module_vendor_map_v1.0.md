# 광학모듈 벤더 Tier 맵 v1.0

> **출처**: Jake Lee, 2026-05  
> **파일 ID**: optical_module_vendor_map_v1.0  
> **관련 프롬프트**: PE-OPTICAL-01 · PE-OPTICAL-02 (섹터 비교)  
> **용도**: OPTICAL-MODULE-DEEP STAGE 2 (시장 포지셔닝·경쟁 구조 분석) 참조 데이터

---

## Tier-1 벤더 (글로벌 주요 공급자)

| 업체명 | 브랜드명 | 본사 | 주력 / 포지션 |
|---|---|---|---|
| Innolight | — | 중국(쑤저우) | 업계 전세계 1위, Tier-0 OEM 공급 (NVIDIA 800G의 50%+) |
| Coherent | 구 II-V / Finisar | 캘리포니아 | Nvidia 납품 2번째 OEM |
| Eoptolink | — | 중국(청두) | Nvidia 납품 3번째 |
| Accelink | — | 중국(우한) | 국유기업, 통신에 강점 |
| Hisense Broadband | — | 중국(칭다오) | — |
| Lumentum | — | 캘리포니아 | — |
| **HG genuine** | — | 중국(우한) | **800G, 1.6T 공급가능 세계 8-9위권** |
| Marvell | — | 캘리포니아 | 광모듈 자체 제작 |
| Broadcom | — | 캘리포니아 | DSP칩, VCSEL 자체제작 |

---

## Tier-2 벤더 (틈새·OEM 공급자)

| 업체명 | 브랜드명 | 본사 | 주력 / 포지션 |
|---|---|---|---|
| Applied Optoelectronics (AOI) | — | 대만 | 데이터센터, 100G/400G |
| TFC / Tianfu Communication | — | 중국(쑤저우) | Nvidia 위탁생산, 광부품 |
| Fabrinet | — | 태국 | 광모듈 위탁조립, Nvidia 위탁생산 |
| Credo Technology | — | 캘리포니아 | AEC |
| Fujitsu Optical Components | — | 일본 | 통신사, Coherent |
| MACOM | — | 메사추세츠 | IC |
| **Gigalight** | — | 중국(선전) | **800G, 데이터센터** |

---

## Tier-3 벤더 (호환·화이트박스·OEM 중심)

| 업체명 | 브랜드명 | 본사 | 주력 / 포지션 |
|---|---|---|---|
| HYC | — | 중국(선전) | 25G~400G OEM |
| FS.com | — | 중국(선전) | 호환모듈 |
| Linktel | — | 중국(우한) | 800G 공급가능 |
| Sino-Telecom | — | 중국(항저우) | Coherent 모듈 |
| **Naddod** | — | 싱가포르, 우한 | **과거 OEM에서 Naddod 자체 브랜드 공급, Nvidia 호환에 주력** |
| **Esoptic** | — | 중국(우한) | **1.6T, 800G, OEM 중심, White Box** |
| **Etulink** | — | 중국(선전) | **다양한 호환모듈, 800G까지 공급** |

---

## 분석 메모

### 지역 클러스터링
- **중국 우한 클러스터**: Accelink(국유), HG genuine, Linktel, Naddod, Esoptic → 우한은 중국 광통신 핵심 산지
- **중국 선전 클러스터**: Gigalight, HYC, FS.com, Etulink → 화이트박스·OEM 중심
- **중국 쑤저우**: Innolight(세계 1위), TFC → 최상위 공급망 허브
- **캘리포니아**: Coherent, Lumentum, Marvell, Broadcom, Credo → 칩·VCSEL·DSP 설계 강점

### 공급망 리스크 포인트
- NVIDIA 800G 납품 상위 3사(Innolight 50%+, Coherent, Eoptolink) 고농도 집중 리스크
- 중국 국유기업(Accelink) 포함 → 지정학적 디커플링 시 대체 벤더 필요
- 1.6T 공급가능 업체: HG genuine(T1), Esoptic(T3) — 차세대 전환 가속 시 포지셔닝 주목

### 투자 스크리닝 시사점
- **Fabrinet(T2)**: 순수 위탁조립 → AI Capex 직접 수혜, 매출 가시성 높음
- **Coherent(T1)**: II-V 통합 이후 포트폴리오 재편 중 → DD 우선순위
- **Credo Technology(T2)**: AEC(Active Electrical Cable) 포지셔닝 — 광케이블 대비 가격 경쟁력 포인트
- **AOI(T2)**: 100G/400G 중심 → 800G 전환 타이밍 리스크 존재

---

## 연계 프롬프트 활용 가이드

```
[이 파일 활용 시나리오]

STAGE 2 (시장 포지셔닝) 입력 시:
  → Tier 분류 + 지역 클러스터 + Nvidia 납품 순위 참조

STAGE 3 (공급망 리스크) 입력 시:
  → 중국 비중, 국유기업 여부, 1개사 의존도(Innolight 50%+) 참조

PE-OPTICAL-02 (섹터 비교) 활용 시:
  → T1 vs T2 마진 구조, OEM vs 자체브랜드 전략 차이 비교

PE-RISK v4.0-OPT 연계 시:
  → 지정학 리스크 매트릭스 → 우한/쑤저우 클러스터 집중도 점수화
```

---

## 버전 이력

| 버전 | 날짜 | 변경 내용 |
|---|---|---|
| v1.0 | 2026-05-20 | 초기 등록 — Jake Lee 202605 자료 기반, Tier 1/2/3 분류 + 지역 클러스터 + 투자 메모 구조화 |
