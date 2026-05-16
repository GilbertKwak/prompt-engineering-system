# CMD-FS · Financial Signal 커맨드 템플릿
<!-- version: 2.1 | updated: 2026-05-17 | YAML-safe -->

## 메타데이터

```yaml
cmd_id:        "CMD-FS-{NN}"           # 예: CMD-FS-03
domain:        "SEMI-OPT-GNN"          # PE-SEMI / PE-FIN / PE-STRAT
model_layer:   "GraphSAGE-3L"          # GNN 레이어 수
graph_version: "v4.3"                  # knowledge-graph 버전
run_date:      "YYYY-MM-DD"
author:        "GilbertKwak"
```

---

## 1. 커맨드 목적

> 한 줄 요약: 어떤 그래프/신호 분석을 수행하는가?

| 항목 | 내용 |
|------|------|
| 분석 유형 | 노드-엣지 맵 / 알파 신호 / 경로 충격 |
| 입력 엔티티 | 종목 코드 또는 노드 ID 목록 |
| 출력 형식 | PNG(시각화) + JSON(신호 테이블) |

---

## 2. 파라미터 슬롯

```yaml
params:
  nodes:          []        # 대상 노드 리스트 (티커 or 내부 ID)
  sectors:        []        # 필터링 섹터 (Equipment/Foundry/Chemical/Memory/OSAT)
  edge_types:     []        # SUPPLY / PROCESS / RISK (복수 선택 가능)
  alpha_filter:   "ALL"     # BUY / NEUTRAL / AVOID / ALL
  importance_min: 0.0       # 노드 importance 하한 (0.0–1.0)
  layout:         "sector"  # sector / spring / circular / kamada_kawai
  output_format:  "png+json" # png / json / png+json
```

---

## 3. 실행 체크리스트

- [ ] `graph_version` 최신 여부 확인 (`docs/knowledge-graph/` 참조)
- [ ] `nodes` 목록이 현재 그래프에 존재하는지 검증
- [ ] `edge_types` 누락 없이 지정 (기본값: SUPPLY+PROCESS+RISK 전체)
- [ ] 시각화 저장 경로: `docs/charts/CMD-FS-{NN}_{date}.png`
- [ ] 메타 JSON 저장: `docs/charts/CMD-FS-{NN}_{date}.png.meta.json`
- [ ] GitHub 커밋 후 Notion `PE-SEMI` 페이지에 차트 링크 동기화

---

## 4. 출력 구조

### 4-1. 시각화 (PNG)

```
섹터별 계층 배치:
  Equipment(상단) → Foundry(중앙) → Chemical/Memory/OSAT(주변)
  노드 크기:    importance 비례
  노드 테두리:  BUY=흰색 / NEUTRAL=금색 / AVOID=적색
  엣지 색상:    SUPPLY=파랑 / PROCESS=초록 / RISK=빨강
  엣지 굵기:    weight 비례 (0.5–3.0px)
```

### 4-2. 신호 JSON 스키마

```json
{
  "cmd_id": "CMD-FS-{NN}",
  "run_date": "YYYY-MM-DD",
  "graph_version": "v4.3",
  "nodes": [
    {
      "id": "NODE_ID",
      "sector": "Equipment",
      "importance": 0.95,
      "alpha_signal": "BUY",
      "irr_adj_bps": 131
    }
  ],
  "edges": [
    {
      "source": "NODE_A",
      "target": "NODE_B",
      "type": "SUPPLY",
      "weight": 0.87
    }
  ],
  "summary": {
    "total_nodes": 0,
    "total_edges": 0,
    "buy_count": 0,
    "avoid_count": 0,
    "top_hub": ""
  }
}
```

---

## 5. YAML-safe 실행 가이드

> **YAML 문법 충돌 방지 원칙** (pe7_product_mece_loop.yml L82 교훈)

```bash
# ✅ 올바른 방법: 별도 Python 스크립트 호출
python automation/pe7_summary.py --cmd CMD-FS-{NN} --output $GITHUB_STEP_SUMMARY

# ❌ 금지: run: | 블록 안 인라인 python3 -c "..."에서 \"딕셔너리 키\" 이스케이프 사용
```

---

## 6. 연관 커맨드

| CMD ID | 설명 |
|--------|------|
| CMD-FS-01 | GraphSAGE 알파 신호 스크리닝 |
| CMD-FS-02 | 섹터별 엣지 가중치 히트맵 |
| **CMD-FS-03** | **노드-엣지 전체 맵 시각화** ← 현재 |
| CMD-FS-04 | 경로 충격 전파 분석 (PE-MIN HHI 연동) |

---

## 7. 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v1.0 | 2026-04-30 | 최초 생성 |
| v2.0 | 2026-05-16 | pe7_summary.py 연동, YAML-safe 섹션 추가 |
| **v2.1** | **2026-05-17** | 파라미터 슬롯 세분화, 출력 JSON 스키마 확장, 연관 CMD 테이블 추가 |
