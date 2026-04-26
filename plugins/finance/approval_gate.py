#!/usr/bin/env python3
"""
PE-7 Approval Gate Module
==========================
재사용 가능한 Approval Gate 라이브러리.
run_finance_pipeline.py 또는 다른 pipeline에서 import하여 사용.

Usage:
    from approval_gate import ApprovalGate
    gate = ApprovalGate(name="Step2", timeout_hours=24, on_timeout="cancel")
    result = gate.wait()   # "approved" | "rejected" | "timeout_cancel" | "timeout_approve"
"""

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


class ApprovalGate:
    """
    단계별 Approval Gate.
    checkpoint JSON을 통해 상태를 지속하며,
    시스템 재시작 후 --resume로 재개 가능.
    """

    APPROVED        = "approved"
    REJECTED        = "rejected"
    TIMEOUT_CANCEL  = "timeout_cancel"
    TIMEOUT_APPROVE = "timeout_approve"
    PENDING         = "pending"

    def __init__(
        self,
        name: str = "Gate",
        timeout_hours: float = 24.0,
        on_timeout: str = "cancel",      # "cancel" | "auto_approve"
        checkpoint_path: str = "reports/.gate_checkpoint.json",
        audit_log_path: str  = "reports/.gate_audit.log",
    ):
        self.name           = name
        self.timeout_s      = timeout_hours * 3600
        self.on_timeout     = on_timeout
        self.cp_path        = Path(checkpoint_path)
        self.audit_path     = Path(audit_log_path)
        self.cp_path.parent.mkdir(parents=True, exist_ok=True)

    # ─── Audit ──────────────────────────────────────
    def _log(self, msg: str):
        ts   = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        line = f"[{ts}][{self.name}] {msg}"
        print(line)
        with open(self.audit_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    # ─── Checkpoint ───────────────────────────────
    def _save(self, status: str, meta: dict = {}):
        data = {
            "gate_name": self.name,
            "status":    status,
            "saved_at":  datetime.now(timezone.utc).isoformat(),
            **meta,
        }
        self.cp_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    def _load(self) -> dict | None:
        if self.cp_path.exists():
            return json.loads(self.cp_path.read_text())
        return None

    def clear_checkpoint(self):
        if self.cp_path.exists():
            self.cp_path.unlink()

    # ─── 메인 Gate ───────────────────────────────
    def wait(self, context_msg: str = "") -> str:
        """
        대화형 Approval Gate.
        대기 중 Ctrl+C 시 checkpoint를 PENDING으로 저장하고 종료.
        이후 resume() 호출로 재개.
        """
        deadline = time.time() + self.timeout_s
        self._save(self.PENDING, {"context": context_msg})
        self._log(f"Gate 열림 (timeout={self.timeout_s/3600:.1f}h, on_timeout={self.on_timeout})")

        if context_msg:
            print(f"\n  Context: {context_msg}")

        sep = "=" * 55
        print(f"\n{sep}")
        print(f" APPROVAL GATE: {self.name}")
        print(f" A = Approve  |  R = Reject  |  Ctrl+C = 나중에 --resume")
        print(f"{sep}\n")

        while time.time() < deadline:
            remaining = int(deadline - time.time())
            h, m = divmod(remaining // 60, 60)
            try:
                ans = input(f" [{h:02d}h {m:02d}m] A/R: ").strip().upper()
            except (EOFError, KeyboardInterrupt):
                self._log("Ctrl+C — PENDING 저장, 이후 resume() 호출")
                sys.exit(0)

            if ans == "A":
                self._save(self.APPROVED)
                self._log("APPROVED")
                return self.APPROVED
            elif ans == "R":
                self._save(self.REJECTED)
                self._log("REJECTED")
                return self.REJECTED
            else:
                print("  A 또는 R만 입력.")

        # Timeout
        result = self.TIMEOUT_APPROVE if self.on_timeout == "auto_approve" else self.TIMEOUT_CANCEL
        self._save(result)
        self._log(f"Timeout -> {result}")
        return result

    def resume(self) -> str | None:
        """
        checkpoint를 읽어 PENDING 상태면 gate 재개.
        APPROVED/REJECTED/timeout이면 상태를 반환.
        """
        state = self._load()
        if not state:
            self._log("검사할 checkpoint 없음")
            return None
        status = state.get("status")
        self._log(f"resume() — checkpoint status={status}")
        if status == self.PENDING:
            return self.wait(context_msg=state.get("context", ""))
        return status
