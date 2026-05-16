#!/usr/bin/env python3
"""
PE-UNIV · Domain Tag Auto-Parser v1.0
======================================
GitHub Actions changed files 목록에서 도메인 코드를 자동 추출 →
pe_univ_apply.py 에 전달할 target_domains 리스트를 생성한다.
"""

import os
import re
import json
import subprocess
from pathlib import Path

# ─────────────────────────────────────────────
# PATH → DOMAIN 매핑 테이블
# ─────────────────────────────────────────────
PATH_TO_DOMAIN = {
    "prompts/ai-platform/":        "C-31",
    "PE-CON/":                      "PE-CON",
    "prompts/strategy/":            "PE-STR",
    "applied-cases/jv-fund/":       "PE-JV",
    "PE-7/":                        "PE-7",
    "PE-11/":                       "PE-11",
    "PE-MEM/":                      "PE-MEM",
    "PE-EDU/":                      "PE-EDU",
    "PE-ICD/":                      "PE-ICD",
    "PE-MFG/":                      "PE-MFG",
    "PE-NBD/":                      "PE-NBD",
    "PE-BOARD/":                    "PE-BOARD",
    "applied-cases/PE-PAT/":        "PE-PAT",
    "applied-cases/PE-INTL/":       "PE-INTL",
    "applied-cases/PE-LR/":         "PE-LR",
}

# 파일명 키워드 기반 도메인 추론
FILENAME_PATTERNS = [
    (r"notion_\d+",    "C-31"),
    (r"pe_con",        "PE-CON"),
    (r"strat",         "PE-STR"),
    (r"jv_fund|pe_jv", "PE-JV"),
    (r"hbm|lpddr|nand|pe_mem", "PE-MEM"),
    (r"pe_board|ma_",  "PE-BOARD"),
    (r"patent|pe_pat", "PE-PAT"),
    (r"pe_lr|legal_risk", "PE-LR"),
    (r"intl|spv|holdco",  "PE-INTL"),
]


def infer_domain_from_path(filepath: str) -> str | None:
    """파일 경로에서 도메인 코드 추론"""
    # 경로 기반 매핑 (우선순위 1)
    for prefix, domain in PATH_TO_DOMAIN.items():
        if filepath.startswith(prefix):
            return domain
    # 파일명 패턴 매핑 (우선순위 2)
    fname = Path(filepath).name.lower()
    for pattern, domain in FILENAME_PATTERNS:
        if re.search(pattern, fname):
            return domain
    return None


def get_changed_files_from_git() -> list[str]:
    """git diff HEAD~1 HEAD 로 변경 파일 목록 추출 (Actions 환경)"""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
            capture_output=True, text=True, check=True
        )
        files = [f.strip() for f in result.stdout.splitlines() if f.strip()]
        return [f for f in files if f.endswith(".md") or f.endswith(".py")]
    except subprocess.CalledProcessError:
        return []


def parse_tags(changed_files: list[str] = None) -> dict:
    """
    변경 파일 목록 → {source_file, target_domains} 딕셔너리 반환
    source = C-31 도메인 파일이 있으면 해당 파일, 없으면 첫 번째
    """
    if changed_files is None:
        changed_files = get_changed_files_from_git()

    domain_map: dict[str, str] = {}  # filepath → domain
    for fp in changed_files:
        domain = infer_domain_from_path(fp)
        if domain:
            domain_map[fp] = domain

    # 소스 파일 결정: C-31 우선, 없으면 첫 번째
    source_file = None
    for fp, dm in domain_map.items():
        if dm == "C-31":
            source_file = fp
            break
    if source_file is None and domain_map:
        source_file = next(iter(domain_map))

    # 타겟 도메인: 소스 도메인 제외한 나머지
    source_domain = domain_map.get(source_file)
    target_domains = [
        dm for fp, dm in domain_map.items()
        if dm != source_domain
    ]
    # 최소 P1 MVP 3도메인 보장
    if not target_domains:
        target_domains = ["PE-CON", "PE-STR", "PE-JV"]

    result = {
        "source_file":    source_file,
        "source_domain":  source_domain,
        "target_domains": list(set(target_domains)),
        "changed_files":  changed_files,
        "domain_map":     domain_map,
    }

    # GitHub Actions 환경변수 출력
    if os.getenv("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as gho:
            gho.write(f"source_file={source_file}\n")
            gho.write(f"target_domains={','.join(target_domains)}\n")

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    parse_tags()
