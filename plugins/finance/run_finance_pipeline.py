#!/usr/bin/env python3
"""
PE-7 P2-2: Finance Pipeline Orchestrator with Approval Gate
============================================================
Step 1: cowork_finance_runner.py  -> finance_output_v1.1.json
Step 2: excel_model_generator.py  -> AstraChips_Finance_Model_v1.1.xlsx

Approval Gate Logic:
  - Step 1 완료 후 자동 일시정지
  - Gilbert의 APPROVE / REJECT 응답 대기
  - 미연라 시 checkpoint 저장 -> 이후 --resume 가능
  - Timeout(default 24h) 바게 되면 스로 승인 혹은 취소 (설정 가능)

Usage:
  python run_finance_pipeline.py                     # 일반 실행 (gate 사용)
  python run_finance_pipeline.py --dry-run           # Step 1만 시뮬레이션
  python run_finance_pipeline.py --approve           # gate 승인 후 재개 (--resume 대안)
  python run_finance_pipeline.py --resume            # checkpoint에서 재개
  python run_finance_pipeline.py --skip-approval     # gate 없이 전체 실행
  python run_finance_pipeline.py --reject            # checkpoint 취소 + 종료
  python run_finance_pipeline.py --status            # 현재 checkpoint 상태 출력
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ────────────────────────────────────────
CONFIG = {
    "config_path":    "plugins/finance/finance_config.yaml",
    "runner_script":  "plugins/finance/cowork_finance_runner.py",
    "excel_script":   "plugins/finance/excel_model_generator.py",
    "json_output":    "reports/finance_output_v1.1.json",
    "xlsx_output":    "reports/AstraChips_Finance_Model_v1.1.xlsx",
    "checkpoint":     "reports/.pipeline_checkpoint.json",
    "audit_log":      "reports/.pipeline_audit.log",
    "gate_timeout_h": 24,           # 24시간 이내 미응답 시 동작 (아래 설정)
    "timeout_action": "cancel",     # "cancel" | "auto_approve"
    "poll_interval_s": 5,           # 대화형 프롬프트 폴링 간격
}

STATUS_PENDING  = "PENDING_APPROVAL"
STATUS_APPROVED = "APPROVED"
STATUS_REJECTED = "REJECTED"
STATUS_DONE     = "DONE"
STATUS_FAILED   = "FAILED"


# ────────────────────────────────────────
# Checkpoint 유틸
class Checkpoint:
    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, data: dict):
        data["updated_at"] = datetime.now(timezone.utc).isoformat()
        self.path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    def load(self) -> dict | None:
        if self.path.exists():
            return json.loads(self.path.read_text())
        return None

    def clear(self):
        if self.path.exists():
            self.path.unlink()


# ────────────────────────────────────────
# Audit Log
def audit(msg: str, log_path: str = CONFIG["audit_log"]):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{ts}] {msg}"
    print(line)
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(line + "\n")


# ────────────────────────────────────────
# Step 1: Runner
def run_step1(dry_run: bool = False) -> bool:
    audit("=== STEP 1 START: cowork_finance_runner.py ===")
    if dry_run:
        audit("[DRY-RUN] Step 1 시뮬레이션 실행 (실제 JSON 생성 안함)")
        # dry-run: config 읽어서 가상 출력
        _print_config_summary()
        return True

    cmd = [
        sys.executable,
        CONFIG["runner_script"],
        "--config", CONFIG["config_path"],
        "--output", CONFIG["json_output"],
    ]
    ret = subprocess.run(cmd, capture_output=False)
    if ret.returncode != 0:
        audit(f"[FAIL] Step 1 실패 (exit {ret.returncode})")
        return False
    audit(f"[OK] Step 1 완료 -> {CONFIG['json_output']}")
    return True


# Step 2: Excel Generator
def run_step2() -> bool:
    audit("=== STEP 2 START: excel_model_generator.py ===")
    cmd = [
        sys.executable,
        CONFIG["excel_script"],
        "--input",  CONFIG["json_output"],
        "--output", CONFIG["xlsx_output"],
    ]
    ret = subprocess.run(cmd, capture_output=False)
    if ret.returncode != 0:
        audit(f"[FAIL] Step 2 실패 (exit {ret.returncode})")
        return False
    audit(f"[OK] Step 2 완료 -> {CONFIG['xlsx_output']}")
    return True


# ────────────────────────────────────────
# Approval Gate: 대화형 (terminal)
def interactive_gate(cp: Checkpoint, state: dict) -> str:
    """
    Step 1 결과를 보여주고 APPROVE / REJECT 입력 대기.
    대기 중 checkpoint는 PENDING_APPROVAL 상태로 유지.
    timeout 도래 도달 시 timeout_action 적용.
    """
    timeout_s = CONFIG["gate_timeout_h"] * 3600
    deadline  = time.time() + timeout_s

    print("\n" + "="*60)
    print(" APPROVAL GATE ─ PE-7 P2-2 Finance Pipeline")
    print("="*60)
    print(f" JSON 출력: {CONFIG['json_output']}")
    print(f" 다음 단계: {CONFIG['xlsx_output']} 생성")
    print(f" Timeout : {CONFIG['gate_timeout_h']}h (만료 시 {CONFIG['timeout_action']})") 
    print("="*60)
    print(" ▶ APPROVE 하려면  -->  [A] Enter")
    print(" ▶ REJECT  하려면  -->  [R] Enter")
    print(" ▶ 나중에 계속하려면 Ctrl+C 후  --resume 플래그 사용")
    print("="*60 + "\n")

    while time.time() < deadline:
        remaining = int(deadline - time.time())
        h, m = divmod(remaining // 60, 60)
        prompt = f" [{h:02d}h {m:02d}m 남음] Approve(A) / Reject(R) / Status(S): "
        try:
            ans = input(prompt).strip().upper()
        except (EOFError, KeyboardInterrupt):
            # Ctrl+C 또는 non-interactive 환경
            audit("[GATE] 사용자 인터럽트 — checkpoint PENDING_APPROVAL 유지")
            cp.save({**state, "gate_status": STATUS_PENDING})
            sys.exit(0)          # 0으로 종료 -> --resume 시 계속

        if ans == "A":
            audit("[GATE] APPROVED by user")
            return STATUS_APPROVED
        elif ans == "R":
            audit("[GATE] REJECTED by user")
            return STATUS_REJECTED
        elif ans == "S":
            _print_state(state)
        else:
            print("  A 또는 R만 입력하세요.")

    # Timeout
    action = CONFIG["timeout_action"]
    audit(f"[GATE] Timeout 도달 -> {action}")
    return STATUS_APPROVED if action == "auto_approve" else STATUS_REJECTED


# ────────────────────────────────────────
# 도우미──────────────────────────────────
SEP = "\u2500" * 55

def _print_state(state: dict):
    print(f"\n{SEP}")
    print(f" Pipeline State: {state.get('gate_status', 'N/A')}")
    print(f" Step 1: {state.get('step1', 'not run')}")
    print(f" Step 2: {state.get('step2', 'not run')}")
    print(f" Updated: {state.get('updated_at', 'N/A')}")
    print(f"{SEP}\n")

def _print_config_summary():
    print(f"\n{SEP}")
    print(" [DRY-RUN] 설정 요약")
    for k, v in CONFIG.items():
        print(f"   {k:30s}: {v}")
    print(f"{SEP}\n")


# ────────────────────────────────────────
# 메인
def main():
    parser = argparse.ArgumentParser(description="PE-7 Finance Pipeline with Approval Gate")
    parser.add_argument("--dry-run",       action="store_true", help="Step 1 시뮬레이션만 (JSON 미생성)")
    parser.add_argument("--skip-approval", action="store_true", help="Gate 없이 Step1→Step2 직접 실행")
    parser.add_argument("--approve",       action="store_true", help="PENDING checkpoint 승인 후 Step2 재개")
    parser.add_argument("--resume",        action="store_true", help="checkpoint에서 상태 확인 후 재개")
    parser.add_argument("--reject",        action="store_true", help="PENDING checkpoint 취소 + 종료")
    parser.add_argument("--status",        action="store_true", help="현재 checkpoint 상태만 출력")
    args = parser.parse_args()

    cp    = Checkpoint(CONFIG["checkpoint"])
    state = cp.load() or {}

    # ── --status ──────────────────────────────
    if args.status:
        if state:
            _print_state(state)
        else:
            print(" checkpoint 없음 (pipeline 미실행)")
        return

    # ── --reject ─────────────────────────────
    if args.reject:
        audit("[GATE] 사용자가 --reject 플래그로 취소")
        cp.save({**state, "gate_status": STATUS_REJECTED})
        cp.clear()
        audit("[DONE] Pipeline 취소, checkpoint 삭제")
        return

    # ── --approve / --resume ───────────────────
    if args.approve or args.resume:
        if not state or state.get("gate_status") != STATUS_PENDING:
            print(" PENDING checkpoint이 없습니다. 먼저 일반 실행하세요.")
            return
        if state.get("step1") != "OK":
            print(" Step 1이 완료되지 않았습니다. pipeline을 다시 실행하세요.")
            return
        audit("[GATE] --approve/--resume: Step 2 재개")
        cp.save({**state, "gate_status": STATUS_APPROVED})
        ok2 = run_step2()
        final = STATUS_DONE if ok2 else STATUS_FAILED
        cp.save({**state, "gate_status": final, "step2": "OK" if ok2 else "FAIL"})
        if ok2:
            cp.clear()
        audit(f"[PIPELINE] 완료 — {final}")
        return

    # ── 일반 실행 ──────────────────────────
    audit("[PIPELINE] 시작 (v1.1)")
    state = {"gate_status": "RUNNING", "step1": "pending", "step2": "pending"}
    cp.save(state)

    # Step 1
    ok1 = run_step1(dry_run=args.dry_run)
    state["step1"] = "OK" if ok1 else "FAIL"
    if not ok1:
        state["gate_status"] = STATUS_FAILED
        cp.save(state)
        audit("[PIPELINE] Step 1 실패 — 종료")
        sys.exit(1)

    # --skip-approval: gate 미사용
    if args.skip_approval or args.dry_run:
        if args.dry_run:
            audit("[DRY-RUN] Gate 바이패스, Step 2 실제 실행 안함")
            cp.clear()
            return
        audit("[GATE] --skip-approval: Gate 바이패스")
        gate_result = STATUS_APPROVED
    else:
        # Approval Gate (대화형)
        state["gate_status"] = STATUS_PENDING
        cp.save(state)
        gate_result = interactive_gate(cp, state)

    cp.save({**state, "gate_status": gate_result})

    if gate_result == STATUS_APPROVED:
        ok2 = run_step2()
        state["step2"] = "OK" if ok2 else "FAIL"
        final = STATUS_DONE if ok2 else STATUS_FAILED
        cp.save({**state, "gate_status": final})
        if ok2:
            cp.clear()           # 정상 완료 시 checkpoint 제거
        audit(f"[PIPELINE] 완료 — {final}")
        sys.exit(0 if ok2 else 1)
    else:
        audit("[PIPELINE] 취소 (REJECTED). checkpoint 유지")
        cp.save({**state, "gate_status": STATUS_REJECTED})
        cp.clear()
        sys.exit(2)


if __name__ == "__main__":
    main()
