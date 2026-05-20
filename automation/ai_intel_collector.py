#!/usr/bin/env python3
"""
ai_intel_collector.py  v2 — Section A · Step 1
Perplexity sonar/sonar-pro API를 통해 AI 도메인별 주간 인텔 수집

변경사항 v2:
  - ThreadPoolExecutor 병렬 수집 (--parallel)
  - --all-domains 플래그: 6개 도메인 일괄 수집
  - 쿼리 자동 생성 (--auto-queries): 도메인별 기본 쿼리 3개
  - 결과 품질 검증 (confidence < 0.4 시 경고)
  - 수집 통계 리포트 출력

Usage:
  # 단일 도메인
  python automation/ai_intel_collector.py \\
    --domain enterprise_deployment --week 2026-W21 --scope standard \\
    --auto-queries --output output/ai_intel/

  # 전체 도메인 병렬 수집
  python automation/ai_intel_collector.py \\
    --all-domains --week 2026-W21 --scope standard \\
    --parallel --output output/ai_intel/
"""

import argparse
import json
import os
import sys
import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("[ERROR] requests 패키지 없음: pip install requests", file=sys.stderr)
    sys.exit(1)

# ─── 상수 ────────────────────────────────────────────────────────────────────
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
MODEL_STANDARD     = "sonar"
MODEL_DEEP         = "sonar-pro"
MAX_RETRIES         = 3
RETRY_BASE_DELAY    = 2
MAX_WORKERS         = 3   # 병렬 도메인 수 (API rate limit 고려)

# ─── 도메인 메타데이터 ──────────────────────────────────────────────────────────
DOMAIN_META: dict[str, dict] = {
    "enterprise_deployment": {
        "label": "Enterprise AI Deployment",
        "description": "기업 AI 도입 현황, ROI 사례, 거버넌스",
        "ew_metrics": ["adoption_rate", "cost_per_query", "enterprise_deal_size"],
        "auto_queries": [
            "enterprise AI deployment adoption rate 2026 Fortune 500 latest",
            "LLM enterprise ROI cost savings case studies 2026",
            "AI governance compliance enterprise implementation challenges 2026",
        ],
    },
    "model_performance": {
        "label": "Model Performance Benchmarks",
        "description": "LLM/MLLM 벤치마크, 추론 속도, 비용 효율",
        "ew_metrics": ["benchmark_score", "tokens_per_second", "cost_per_million_tokens"],
        "auto_queries": [
            "LLM benchmark comparison GPT Claude Gemini Llama 2026 latest",
            "AI inference speed cost efficiency tokens per dollar 2026",
            "multimodal model performance breakthrough 2026 research",
        ],
    },
    "infrastructure": {
        "label": "AI Infrastructure & Chips",
        "description": "GPU/NPU 공급, 데이터센터, 전력 효율",
        "ew_metrics": ["gpu_supply_tightness", "pue", "capex_per_flop"],
        "auto_queries": [
            "NVIDIA H100 H200 GPU supply shortage data center 2026",
            "AI data center power consumption electricity demand 2026",
            "AI chip alternatives AMD Intel Qualcomm custom silicon 2026",
        ],
    },
    "regulatory": {
        "label": "AI Regulation & Policy",
        "description": "글로벌 AI 규제, 컴플라이언스, 정책 변화",
        "ew_metrics": ["compliance_deadline_count", "enforcement_action_count"],
        "auto_queries": [
            "EU AI Act implementation enforcement 2026 compliance deadline",
            "US AI executive order regulation policy update 2026",
            "AI regulatory fines enforcement actions global 2026",
        ],
    },
    "open_source": {
        "label": "Open Source AI Ecosystem",
        "description": "오픈소스 모델, 프레임워크, 커뮤니티 동향",
        "ew_metrics": ["github_stars_delta", "new_model_releases", "fork_velocity"],
        "auto_queries": [
            "open source LLM releases Llama Mistral Qwen 2026 latest",
            "Hugging Face GitHub AI model downloads trending 2026",
            "open source AI framework LangChain LlamaIndex update 2026",
        ],
    },
    "investment": {
        "label": "AI Investment & M&A",
        "description": "VC 투자, M&A, AI 스타트업 동향",
        "ew_metrics": ["funding_volume_usd", "deal_count", "valuation_multiple"],
        "auto_queries": [
            "AI startup funding VC investment Q2 2026 latest deals",
            "AI company M&A acquisition 2026 strategic deals",
            "AI unicorn valuation IPO 2026 market",
        ],
    },
}


# ─── 유틸리티 ─────────────────────────────────────────────────────────────────
def get_api_key() -> str:
    key = os.environ.get("PERPLEXITY_API_KEY", "").strip()
    if not key:
        print("[ERROR] PERPLEXITY_API_KEY 환경변수 미설정", file=sys.stderr)
        sys.exit(1)
    return key


def select_model(scope: str) -> str:
    return MODEL_DEEP if scope in ("deep", "emergency") else MODEL_STANDARD


def build_system_prompt(domain: str, week: str) -> str:
    meta = DOMAIN_META.get(domain, {"label": domain, "description": "", "ew_metrics": []})
    metrics_list = ", ".join(meta.get("ew_metrics", []))
    return (
        f"You are a senior AI industry analyst providing structured weekly intelligence.\n"
        f"Domain: {meta['label']} — {meta['description']}\n"
        f"Report week: {week}\n\n"
        f"Respond ONLY in strict JSON matching this schema exactly:\n"
        f"{{\n"
        f'  "domain": "{domain}",\n'
        f'  "week": "{week}",\n'
        f'  "collected_at": "<ISO8601>",\n'
        f'  "key_facts": ["<factual statement with source>", ...],\n'
        f'  "emerging_signals": ["<weak signal or early-stage trend>", ...],\n'
        f'  "metrics": {{"<metric_name>": <number_or_null>}},\n'
        f'  "sources": ["<url>", ...],\n'
        f'  "confidence": <0.0_to_1.0>,\n'
        f'  "summary": "<2-3 sentence executive summary>"\n'
        f"}}\n\n"
        f"Priority metrics to extract (use null if unavailable): {metrics_list}\n"
        f"Rules: Be specific with numbers. Cite URLs. Flag uncertain data with lower confidence."
    )


def parse_json_from_response(text: str) -> dict:
    """LLM 응답에서 JSON 추출 — 3단계 폴백"""
    # 1. ```json ... ``` 블록
    m = re.search(r"```(?:json)?\s*\n?({.*?})\s*\n?```", text, re.DOTALL)
    if m:
        return json.loads(m.group(1))
    # 2. 첫 번째 완전한 { } 블록
    m = re.search(r"({[\s\S]*})", text)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    # 3. 부분 파싱 후 기본값 반환
    print(f"[WARN] JSON 파싱 실패 — 기본 구조 반환. 응답: {text[:200]}", file=sys.stderr)
    return {
        "key_facts": [text[:500]],
        "emerging_signals": [],
        "metrics": {},
        "sources": [],
        "confidence": 0.3,
        "summary": text[:200],
        "_parse_failed": True,
    }


# ─── API 호출 ─────────────────────────────────────────────────────────────────
def call_perplexity(
    api_key: str,
    model: str,
    system_prompt: str,
    user_query: str,
    attempt: int = 0,
) -> dict:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_query},
        ],
        "temperature": 0.15,
        "max_tokens": 2048,
    }
    try:
        resp = requests.post(PERPLEXITY_API_URL, headers=headers, json=payload, timeout=90)
        if resp.status_code == 429 and attempt < MAX_RETRIES:
            delay = RETRY_BASE_DELAY * (2 ** attempt)
            print(f"[WARN] Rate-limit. {delay}s 대기 후 재시도 ({attempt+1}/{MAX_RETRIES})",
                  file=sys.stderr)
            time.sleep(delay)
            return call_perplexity(api_key, model, system_prompt, user_query, attempt + 1)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.Timeout:
        if attempt < MAX_RETRIES:
            delay = RETRY_BASE_DELAY * (2 ** attempt)
            print(f"[WARN] Timeout. {delay}s 후 재시도", file=sys.stderr)
            time.sleep(delay)
            return call_perplexity(api_key, model, system_prompt, user_query, attempt + 1)
        raise
    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] HTTP {resp.status_code}: {resp.text[:300]}", file=sys.stderr)
        raise


# ─── 수집 로직 ─────────────────────────────────────────────────────────────────
def collect_domain_intel(
    domain: str,
    week: str,
    scope: str,
    queries: list[str],
    api_key: str,
    verbose: bool = True,
) -> dict:
    """단일 도메인 인텔 수집 → 병합 결과 반환"""
    model = select_model(scope)
    system_prompt = build_system_prompt(domain, week)
    results, errors = [], []

    for i, query in enumerate(queries):
        if not query.strip():
            continue
        if verbose:
            print(f"  [{domain}] [{i+1}/{len(queries)}] {query[:70]}...", file=sys.stderr)
        try:
            raw = call_perplexity(api_key, model, system_prompt, query)
            content = raw["choices"][0]["message"]["content"]
            parsed = parse_json_from_response(content)
            parsed.update({"_query": query, "_model": model,
                           "collected_at": datetime.utcnow().isoformat() + "Z"})
            results.append(parsed)
            conf = parsed.get("confidence", "?")
            if verbose:
                flag = "⚠" if isinstance(conf, float) and conf < 0.4 else "✓"
                print(f"    {flag} 완료 (confidence={conf})", file=sys.stderr)
        except Exception as e:
            print(f"    ✗ 오류: {e}", file=sys.stderr)
            errors.append({"query": query, "error": str(e)})
        time.sleep(0.8)  # 쿼리 간 쿨다운

    if not results:
        print(f"[ERROR] {domain}: 수집 결과 없음", file=sys.stderr)
        return {
            "domain": domain, "week": week,
            "collected_at": datetime.utcnow().isoformat() + "Z",
            "key_facts": [], "emerging_signals": [], "metrics": {},
            "sources": [], "confidence": 0.0,
            "summary": f"[FAILED] {domain} 수집 실패",
            "_collection_errors": errors, "_scope": scope, "_query_count": 0,
            "_status": "failed",
        }

    merged = _merge_results(domain, week, results)
    merged.update({"_collection_errors": errors, "_scope": scope, "_status": "ok"})
    return merged


def _merge_results(domain: str, week: str, results: list[dict]) -> dict:
    all_facts, all_signals, all_sources = [], [], []
    merged_metrics: dict = {}
    conf_sum, summaries = 0.0, []

    for r in results:
        all_facts.extend(r.get("key_facts", []))
        all_signals.extend(r.get("emerging_signals", []))
        all_sources.extend(r.get("sources", []))
        for k, v in r.get("metrics", {}).items():
            if v is not None:
                merged_metrics[k] = v
        conf_sum += float(r.get("confidence", 0.7))
        if r.get("summary"):
            summaries.append(r["summary"])

    return {
        "domain": domain,
        "week": week,
        "collected_at": datetime.utcnow().isoformat() + "Z",
        "key_facts": list(dict.fromkeys(all_facts)),
        "emerging_signals": list(dict.fromkeys(all_signals)),
        "metrics": merged_metrics,
        "sources": sorted(set(all_sources)),
        "confidence": round(conf_sum / len(results), 3),
        "summary": " | ".join(summaries[:3]),
        "_query_count": len(results),
    }


def collect_all_domains_parallel(
    week: str,
    scope: str,
    api_key: str,
    output_dir: Path,
    dry_run: bool = False,
) -> dict[str, dict]:
    """6개 도메인 병렬 수집 — ThreadPoolExecutor 사용"""
    results: dict[str, dict] = {}

    def worker(domain: str) -> tuple[str, dict]:
        queries = DOMAIN_META[domain]["auto_queries"]
        if dry_run:
            return domain, _make_dry_run_result(domain, week, scope, queries)
        result = collect_domain_intel(domain, week, scope, queries, api_key, verbose=True)
        out_path = output_dir / f"intel_{domain}.json"
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2))
        return domain, result

    print(f"[INFO] {len(DOMAIN_META)}개 도메인 병렬 수집 시작 (workers={MAX_WORKERS})",
          file=sys.stderr)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(worker, d): d for d in DOMAIN_META}
        for future in as_completed(futures):
            domain = futures[future]
            try:
                d, result = future.result()
                results[d] = result
                status = result.get("_status", "?")
                conf   = result.get("confidence", "?")
                print(f"  [{status.upper()}] {d} (confidence={conf})", file=sys.stderr)
            except Exception as e:
                print(f"  [FAIL] {domain}: {e}", file=sys.stderr)
                results[domain] = {"_status": "failed", "error": str(e)}
    return results


def _make_dry_run_result(domain: str, week: str, scope: str, queries: list) -> dict:
    return {
        "domain": domain, "week": week,
        "collected_at": datetime.utcnow().isoformat() + "Z",
        "key_facts": [f"[DRY-RUN] {domain} 테스트 실행"],
        "emerging_signals": ["[DRY-RUN] 시그널 없음"],
        "metrics": {m: None for m in DOMAIN_META[domain].get("ew_metrics", [])},
        "sources": [],
        "confidence": 0.0,
        "summary": f"[DRY-RUN] {domain} — 실제 API 호출 없음",
        "_scope": scope,
        "_query_count": len(queries),
        "_collection_errors": [],
        "_status": "dry_run",
    }


# ─── 통계 리포트 ────────────────────────────────────────────────────────────────
def print_collection_report(results: dict[str, dict]) -> None:
    print("\n" + "="*60, file=sys.stderr)
    print("수집 통계 리포트", file=sys.stderr)
    print("="*60, file=sys.stderr)
    ok = [d for d, r in results.items() if r.get("_status") == "ok"]
    fail = [d for d, r in results.items() if r.get("_status") == "failed"]
    dry  = [d for d, r in results.items() if r.get("_status") == "dry_run"]
    print(f"  성공: {len(ok)}개 | 실패: {len(fail)}개 | DRY-RUN: {len(dry)}개",
          file=sys.stderr)
    for d, r in results.items():
        qc   = r.get("_query_count", 0)
        conf = r.get("confidence", 0)
        errs = len(r.get("_collection_errors", []))
        print(f"  {d:30s} queries={qc} conf={conf:.2f} errors={errs}", file=sys.stderr)
    print("="*60 + "\n", file=sys.stderr)


# ─── CLI ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Perplexity API AI 도메인 인텔 수집 v2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""예시:
  # 단일 도메인 (자동 쿼리)
  python ai_intel_collector.py --domain infrastructure --week 2026-W21 \\
      --auto-queries --output output/ai_intel/

  # 전체 도메인 병렬 (DRY-RUN)
  python ai_intel_collector.py --all-domains --week 2026-W21 \\
      --dry-run --output output/ai_intel/
""",
    )

    # 도메인 선택 (둘 중 하나 필수)
    domain_grp = parser.add_mutually_exclusive_group(required=True)
    domain_grp.add_argument(
        "--domain",
        choices=list(DOMAIN_META.keys()),
        help="수집 대상 단일 도메인",
    )
    domain_grp.add_argument(
        "--all-domains",
        action="store_true",
        help="6개 도메인 전체 병렬 수집",
    )

    parser.add_argument("--week",   required=True, help="ISO 주차 (예: 2026-W21)")
    parser.add_argument(
        "--scope", default="standard",
        choices=["standard", "deep", "emergency"],
        help="수집 깊이 (standard=sonar / deep·emergency=sonar-pro)",
    )
    parser.add_argument("--output", required=True,
                        help="결과 저장 경로 (디렉토리 또는 단일 JSON 파일)")

    # 쿼리 소스 (단일 도메인일 때만 사용)
    query_grp = parser.add_mutually_exclusive_group()
    query_grp.add_argument(
        "--queries", nargs="+",
        help="직접 입력 쿼리 (--domain 사용 시)",
    )
    query_grp.add_argument(
        "--auto-queries", action="store_true",
        help="도메인별 기본 쿼리 자동 사용",
    )

    parser.add_argument("--parallel", action="store_true",
                        help="--all-domains 시 병렬 실행 (기본: 순차)")
    parser.add_argument("--dry-run",  action="store_true",
                        help="API 실제 호출 없이 구조 검증")

    args = parser.parse_args()

    output_path = Path(args.output)

    # ── 전체 도메인 모드 ────────────────────────────────────────────────────────
    if args.all_domains:
        output_path.mkdir(parents=True, exist_ok=True)
        api_key = get_api_key() if not args.dry_run else "dry-run"

        if args.parallel or args.dry_run:
            all_results = collect_all_domains_parallel(
                args.week, args.scope, api_key, output_path, dry_run=args.dry_run
            )
        else:
            all_results = {}
            for domain in DOMAIN_META:
                print(f"[INFO] 수집 중: {domain}", file=sys.stderr)
                queries = DOMAIN_META[domain]["auto_queries"]
                result  = collect_domain_intel(
                    domain, args.week, args.scope, queries, api_key
                )
                out_file = output_path / f"intel_{domain}.json"
                out_file.write_text(json.dumps(result, ensure_ascii=False, indent=2))
                all_results[domain] = result

        # 통합 인덱스 저장
        index = {
            "week": args.week, "scope": args.scope,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "domains": list(all_results.keys()),
            "summary": {
                d: {"status": r.get("_status"), "confidence": r.get("confidence", 0),
                    "fact_count": len(r.get("key_facts", []))}
                for d, r in all_results.items()
            },
        }
        (output_path / "_index.json").write_text(
            json.dumps(index, ensure_ascii=False, indent=2)
        )
        print_collection_report(all_results)
        print(f"[OK] 전체 수집 완료 → {output_path}/", file=sys.stderr)
        return

    # ── 단일 도메인 모드 ───────────────────────────────────────────────────────
    if args.auto_queries:
        queries = DOMAIN_META[args.domain]["auto_queries"]
    elif args.queries:
        queries = args.queries
    else:
        parser.error("--domain 사용 시 --queries 또는 --auto-queries 중 하나 필수")

    if args.dry_run:
        result = _make_dry_run_result(args.domain, args.week, args.scope, queries)
    else:
        api_key = get_api_key()
        result  = collect_domain_intel(
            args.domain, args.week, args.scope, queries, api_key
        )

    # 출력 경로: 디렉토리면 파일명 자동 생성
    if output_path.suffix == "":
        output_path.mkdir(parents=True, exist_ok=True)
        out_file = output_path / f"intel_{args.domain}.json"
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        out_file = output_path

    out_file.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"[OK] {args.domain} 수집 완료 → {out_file}")
    print(f"     쿼리 수: {result['_query_count']} | 신뢰도: {result['confidence']} "
          f"| 팩트: {len(result['key_facts'])}개")


if __name__ == "__main__":
    main()
