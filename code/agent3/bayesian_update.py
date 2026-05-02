#!/usr/bin/env python3
"""
bayesian_update.py  —  Agent 3 / OUTPUT 3-4
Sequential Bayesian Update Engine for 4-World Scenario Probabilities
Author: Gilbert | Version: 1.0.0 | Date: 2026-05-02

§3 Evidence Protocol
────────────────────
Evidence Collection Sources:
  E1  US BIS Export Administration → tariff/control count per quarter
  E2  China Customs → rare earth export volume (monthly)
  E3  Taiwan MND → ADIZ intrusion count (weekly)
  E4  ASML IR → EUV delivery lead-time (monthly)
  E5  SK Hynix / Samsung IR → quarterly revenue (quarterly)
  E6  Nvidia channel → H100/H200 lead-time (weekly)
  E7  Freightos Baltic → container freight FBX (weekly)
  E8  USGS → rare earth price index (monthly)
  E9  Bloomberg → semiconductor CDS spread (daily → monthly avg)
  E10 USPTO / LinkedIn → talent flow proxy (monthly)
"""

import numpy as np
import pandas as pd
import json, logging
from dataclasses import dataclass, field
from typing import Dict, List
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

@dataclass
class Evidence:
    id: str
    date: str
    description: str
    source: str
    likelihood: Dict[str, float]
    confidence: float = 1.0
    tags: List[str] = field(default_factory=list)

class BayesianEngine:
    WORLDS = list("ABCD")
    WORLD_NAMES = {
        "A": "Hard Decoupling", "B": "Managed De-risking",
        "C": "AI-Boom Cooperation", "D": "Multilateral Rebalance",
    }

    def __init__(self, priors: Dict[str, float]):
        assert abs(sum(priors.values()) - 1.0) < 1e-6
        self.history: List[Dict] = []
        self._state = np.array([priors[w] for w in self.WORLDS])
        self.history.append(self._snapshot("PRIOR", "Initial prior"))

    @property
    def current(self) -> Dict[str, float]:
        return {w: round(float(v), 6) for w, v in zip(self.WORLDS, self._state)}

    def _snapshot(self, ev_id: str, desc: str) -> Dict:
        return {"event": ev_id, "description": desc,
                **{f"P_{w}": round(float(v), 6) for w, v in zip(self.WORLDS, self._state)}}

    def update(self, ev: Evidence) -> Dict[str, float]:
        """P(W|E) ∝ P(E|W) × P(W)"""
        lr = np.array([ev.likelihood[w] for w in self.WORLDS])
        lr_eff = 1.0 + (lr - 1.0) * ev.confidence
        unnorm = self._state * lr_eff
        if unnorm.sum() == 0:
            raise ValueError(f"Evidence {ev.id} zeroed all worlds")
        self._state = unnorm / unnorm.sum()
        snap = self._snapshot(ev.id, ev.description)
        self.history.append(snap)
        logger.info(f"Updated [{ev.id}] | " + " | ".join(f"P({w})={self.current[w]:.3f}" for w in self.WORLDS))
        return self.current.copy()

    def batch_update(self, evidences: List[Evidence]) -> pd.DataFrame:
        for ev in evidences:
            self.update(ev)
        return pd.DataFrame(self.history)

    def sensitivity_analysis(self, ev: Evidence, lr_range: np.ndarray = None) -> pd.DataFrame:
        if lr_range is None:
            lr_range = np.linspace(0.1, 5.0, 50)
        base_state = self._state.copy()
        rows = []
        for target_w in self.WORLDS:
            for lr_val in lr_range:
                modified = {w: ev.likelihood[w] for w in self.WORLDS}
                modified[target_w] = float(lr_val)
                lr_arr = np.array([modified[w] for w in self.WORLDS])
                lr_eff = 1.0 + (lr_arr - 1.0) * ev.confidence
                unnorm = base_state * lr_eff
                post = unnorm / unnorm.sum()
                row = {"target_world": target_w, "lr_value": round(lr_val, 3)}
                row.update({f"P_{w}": round(float(p), 6) for w, p in zip(self.WORLDS, post)})
                rows.append(row)
        return pd.DataFrame(rows)

    def export(self, path: str) -> None:
        pd.DataFrame(self.history).to_csv(path, index=False)
        logger.info(f"History exported → {path}")


MAY2026_EVIDENCE: List[Evidence] = [
    Evidence(id="E2026Q1_01", date="2026-01-15",
             description="US 반도체 관세 25% 행정명령 서명 (HBM 포함)",
             source="BIS Federal Register",
             likelihood={"A":2.8, "B":1.6, "C":0.2, "D":0.9}, confidence=0.95,
             tags=["tariff","US_policy"]),
    Evidence(id="E2026Q1_02", date="2026-02-20",
             description="Taiwan 예외 조항 확정: 15% 상한 (TSMC CoWoS 유지)",
             source="USTR Press Release",
             likelihood={"A":0.3, "B":1.8, "C":1.4, "D":1.1}, confidence=0.90,
             tags=["tariff","Taiwan_exception"]),
    Evidence(id="E2026Q1_03", date="2026-03-10",
             description="SK하이닉스 Q4-2025 실적: HBM 매출 $11.2B (사상 최대)",
             source="SK Hynix IR",
             likelihood={"A":0.6, "B":1.5, "C":2.2, "D":1.0}, confidence=0.98,
             tags=["earnings","HBM"]),
    Evidence(id="E2026Q1_04", date="2026-03-25",
             description="TSMC Q4-2025 실적: 매출 $26.9B (+39% YoY)",
             source="TSMC IR",
             likelihood={"A":0.5, "B":1.4, "C":2.0, "D":0.9}, confidence=0.98,
             tags=["earnings","foundry"]),
    Evidence(id="E2026Q2_05", date="2026-04-08",
             description="중국, H200 라이선스 요구 보복 발표",
             source="MOFCOM Beijing",
             likelihood={"A":2.5, "B":1.3, "C":0.2, "D":0.8}, confidence=0.88,
             tags=["China_retaliation","export_control"]),
    Evidence(id="E2026Q2_06", date="2026-04-22",
             description="Section 301 반도체 추가 조사 개시 (HBM 포함)",
             source="USTR Federal Register",
             likelihood={"A":2.2, "B":1.2, "C":0.3, "D":0.9}, confidence=0.85,
             tags=["tariff","Section_301"]),
    Evidence(id="E2026Q2_07", date="2026-04-30",
             description="Nvidia Q1-2026 Data Center 매출 $35.6B (+85% YoY)",
             source="Nvidia IR",
             likelihood={"A":0.7, "B":1.3, "C":2.5, "D":1.0}, confidence=0.97,
             tags=["earnings","AI_chip","demand"]),
]

def main():
    PRIORS = {"A":0.05, "B":0.48, "C":0.40, "D":0.07}
    engine = BayesianEngine(PRIORS)
    engine.batch_update(MAY2026_EVIDENCE)
    out = Path("output")
    out.mkdir(exist_ok=True)
    engine.export(str(out / "bayesian_history.csv"))
    engine.sensitivity_analysis(MAY2026_EVIDENCE[0]).to_csv(out / "bayesian_sensitivity.csv", index=False)
    posterior = engine.current
    print("\n=== Final Posterior (2026-05-02) ===")
    for w, p in posterior.items():
        print(f"  World {w} ({BayesianEngine.WORLD_NAMES[w]}): {p*100:.1f}%")
    result = {"date":"2026-05-02", "n_evidence":len(MAY2026_EVIDENCE),
              "priors":PRIORS, "posterior":posterior,
              "dominant_world": max(posterior, key=posterior.get)}
    (out / "bayesian_posterior.json").write_text(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
