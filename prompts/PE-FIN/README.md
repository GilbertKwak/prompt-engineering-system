# PE-FIN · 투자 전략 프롬프트 라이브러리

> **버전**: v1.1 | **업데이트**: 2026-05-08 | **Notion SSOT**: https://www.notion.so/34f55ed436f081c2ad05df1dc11e0ae7

## 프롬프트 인덱스

| ID | 파일 | 명칭 | 버전 | 핵심 기능 | PE-3 |
|----|------|------|------|----------|------|
| `FIN-01` | fin_01_investment_strategy.md | 투자 전략 설계 마스터 | v1.0 | 목표·위험성향 기반 맞춤 전략 | ✅ PASS |
| `FIN-02` | fin_02_risk_hedge.md | 리스크 분석 & 헤지 전략 | v1.0 | VaR·CVaR + 헤지 수단 TOP3 | ✅ PASS |
| `FIN-03` | fin_03_asset_allocation.md | 자산 배분 최적화 | v1.0 | MPT·Risk Parity·Black-Litterman | ✅ PASS |
| `FIN-04` | fin_04_macro_analysis.md | 시장 분석 & 매크로 전망 | v1.0 | 글로벌 거시 + 섹터 로테이션 | ✅ PASS |
| `FIN-05` | fin_05_alternative_investment.md | 대안 투자 (AI·반도체·에너지) | v1.0 | HBM·sCO₂·AstraChips 특화 | ✅ PASS |
| `FIN-06-BFA` | fin_06_bfa_sem.md | 사업성 분석 (BFA-SEM) | v1.0 | IRR/NPV/Payback 프로젝트 경제성 | ✅ PASS |
| **`FIN-07-EVP`** | **fin_07_evp.md** | **Enterprise Valuation (FCP)** | **v1.0** | **FCP+DCF+Comps+Precedent Tx 다보로낼** | **✅ 91%** |

## 연계 워크플로우

```
[FIN-04 매크로] → [FIN-01 전략] → [FIN-03 자산배분]
                                          ↓
[FIN-07-EVP 기업가치] ← [FIN-06-BFA IRR] ← [대상 기업 선정]
                                          ↓
[FIN-02 리스크 헤지] → [FIN-05 대안투자 실행]
```

## 빠른 실행

```bash
# FIN-07-EVP Enterprise Valuation 실행
python automation/run_prompt.py \
  --prompt prompts/PE-FIN/fin_07_evp.md \
  --company "AstraChips" --stage "Growth" \
  --sector "AI반도체" --wacc 11.0 --tgr 3.5

# PE-FIN 전체 검증
python automation/auto_validate.py \
  --dir prompts/PE-FIN/ --rules PE-1,PE-3 --threshold 90
```

## 관련 링크
- **Notion PE-FIN**: https://www.notion.so/34f55ed436f081c2ad05df1dc11e0ae7
- **PE Hub v2.0**: https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b
- **GitHub Repository**: https://github.com/GilbertKwak/prompt-engineering-system
