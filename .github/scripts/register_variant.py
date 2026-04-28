#!/usr/bin/env python3
"""
register_variant.py — Variant 자동 등록 스크립트 v2.1
Usage:
  python register_variant.py --mode validate  --rule PE-1 --files "file1.md file2.md" --output out.json
  python register_variant.py --mode register  --files "file1.md" --index VARIANT_INDEX.json --output result.json
  python register_variant.py --mode changelog --result result.json --changelog CHANGELOG.md
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


# ─────────────────────────────────────────────
# 유틸리티
# ─────────────────────────────────────────────
def utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def parse_files(files_str: str) -> list[Path]:
    """공백·줄바꿈 구분 파일 목록 파싱"""
    paths = []
    for p in re.split(r'[\s\n]+', files_str.strip()):
        p = p.strip()
        if p and Path(p).exists():
            paths.append(Path(p))
    return paths


def extract_frontmatter(text: str) -> dict:
    """YAML frontmatter 추출 (--- 블록)"""
    m = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not m:
        return {}
    try:
        import yaml
        return yaml.safe_load(m.group(1)) or {}
    except Exception:
        return {}


def infer_domain(path: Path) -> str:
    """파일 경로에서 도메인 추론"""
    p = str(path).lower()
    if 'jv' in p or 'joint' in p:
        return 'JV-Fund'
    if 'bstar' in p or 'eco2' in p or 'sco2' in p:
        return 'B-Star-eCO2'
    if 'fu' in p or 'thermal' in p or 'hbm' in p:
        return 'FU-Thermal'
    if 'ai' in p or 'infra' in p or 'dc' in p:
        return 'AI-Infra'
    if 'semiconductor' in p:
        return 'Semiconductor'
    return 'General'


# ─────────────────────────────────────────────
# PE-1 검증: 출처·수치·연도 명시
# ─────────────────────────────────────────────
PE1_CHECKS = [
    (r'\[출처|source|ref\]|\(https?://', 'source_citation',
     '출처 미명시 — [출처] 또는 URL 링크 필요'),
    (r'\d{4}년|\b20\d{2}\b', 'year_reference',
     '연도 미명시 — 수치 데이터에 연도 기재 필요'),
    (r'\(est\.\)|추정|estimated', 'estimation_tag',
     '추정값 태그 없음 — 추정 데이터에 (est.) 표기 권장'),
]


def validate_pe1(content: str, path: Path) -> dict:
    results = {'rule': 'PE-1', 'file': str(path), 'passed': True, 'issues': [], 'checks': {}}
    for pattern, key, msg in PE1_CHECKS:
        found = bool(re.search(pattern, content, re.IGNORECASE))
        results['checks'][key] = found
        if not found:
            results['issues'].append({'code': f'PE1-{key.upper()}', 'message': msg, 'severity': 'warning'})
    # PE-1은 source_citation 미존재 시 FAIL
    if not results['checks'].get('source_citation'):
        results['passed'] = False
        results['issues'][-1 if results['issues'] else 0]['severity'] = 'error'
    return results


# ─────────────────────────────────────────────
# PE-3 검증: 반대 시나리오 포함
# ─────────────────────────────────────────────
PE3_PATTERNS = [
    r'반대.*시나리오|opposite.*scenario|counter.*scenario',
    r'리스크.*매트릭스|risk.*matrix',
    r'단점|downside|challenge|limitation|위험|우려',
    r'대안|alternative|반론|counterargument',
]


def validate_pe3(content: str, path: Path) -> dict:
    results = {'rule': 'PE-3', 'file': str(path), 'passed': False, 'issues': [], 'checks': {}}
    for i, pattern in enumerate(PE3_PATTERNS):
        found = bool(re.search(pattern, content, re.IGNORECASE))
        results['checks'][f'pattern_{i}'] = found
        if found:
            results['passed'] = True
            break
    if not results['passed']:
        results['issues'].append({
            'code': 'PE3-NO-COUNTER',
            'message': '반대 시나리오/리스크 섹션 없음 — 반론·단점·리스크 매트릭스 추가 필요',
            'severity': 'error',
        })
    return results


# ─────────────────────────────────────────────
# Variant 메타데이터 추출
# ─────────────────────────────────────────────
def extract_variant_meta(path: Path) -> dict:
    content = path.read_text(encoding='utf-8')
    fm = extract_frontmatter(content)
    # ID: frontmatter > 파일명 기반
    variant_id = fm.get('id') or fm.get('variant_id') or path.stem.upper().replace('-', '_')
    return {
        'id':          variant_id,
        'file':        str(path),
        'domain':      fm.get('domain') or infer_domain(path),
        'version':     fm.get('version') or '1.0',
        'title':       fm.get('title') or path.stem.replace('_', ' ').replace('-', ' ').title(),
        'description': fm.get('description') or '',
        'tags':        fm.get('tags') or [],
        'registered_at': utcnow(),
        'status':      'active',
        'pe1_passed':  None,
        'pe3_passed':  None,
    }


# ─────────────────────────────────────────────
# MODE: validate
# ─────────────────────────────────────────────
def mode_validate(args) -> int:
    files = parse_files(args.files)
    if not files:
        print(f'[WARN] 유효한 파일 없음: {args.files}')
        json.dump({'rule': args.rule, 'total': 0, 'passed': 0, 'results': []}, open(args.output, 'w'))
        return 0

    results = []
    validator = validate_pe1 if args.rule == 'PE-1' else validate_pe3
    passed_count = 0

    for path in files:
        content = path.read_text(encoding='utf-8')
        r = validator(content, path)
        results.append(r)
        status = '✅ PASS' if r['passed'] else '⚠️  FAIL'
        print(f'  [{args.rule}] {status} — {path}')
        for issue in r.get('issues', []):
            print(f'          {issue["severity"].upper()}: {issue["message"]}')
        if r['passed']:
            passed_count += 1

    summary = {
        'rule':    args.rule,
        'total':   len(files),
        'passed':  passed_count,
        'failed':  len(files) - passed_count,
        'results': results,
        'run_at':  utcnow(),
    }
    json.dump(summary, open(args.output, 'w'), ensure_ascii=False, indent=2)
    print(f'\n[{args.rule}] 결과: {passed_count}/{len(files)} 통과')
    # PE-3 실패는 warning 처리 (non-blocking)
    return 0


# ─────────────────────────────────────────────
# MODE: register
# ─────────────────────────────────────────────
def mode_register(args) -> int:
    files = parse_files(args.files)
    index_path = Path(args.index)

    # 기존 인덱스 로드
    if index_path.exists():
        index = json.loads(index_path.read_text(encoding='utf-8'))
    else:
        index = {'schema_version': '2.1', 'updated_at': utcnow(), 'variants': []}

    existing_ids = {v['id'] for v in index.get('variants', [])}
    registered = []
    updated    = []

    for path in files:
        meta = extract_variant_meta(path)
        # PE 검증 결과 반영
        content = path.read_text(encoding='utf-8')
        meta['pe1_passed'] = validate_pe1(content, path)['passed']
        meta['pe3_passed'] = validate_pe3(content, path)['passed']

        if meta['id'] in existing_ids:
            # 기존 항목 업데이트
            for i, v in enumerate(index['variants']):
                if v['id'] == meta['id']:
                    index['variants'][i] = {**v, **meta, 'updated_at': utcnow()}
                    break
            updated.append(meta)
            print(f'  [UPDATE] {meta["id"]} — {path}')
        else:
            index['variants'].append(meta)
            registered.append(meta)
            print(f'  [REGISTER] {meta["id"]} — {path}')

    index['updated_at'] = utcnow()
    index['total'] = len(index['variants'])
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')

    result = {
        'registered': len(registered),
        'updated':    len(updated),
        'variants':   registered + updated,
        'index_path': str(index_path),
        'run_at':     utcnow(),
    }
    json.dump(result, open(args.output, 'w'), ensure_ascii=False, indent=2)
    print(f'\n등록: {len(registered)}개 / 갱신: {len(updated)}개')
    return 0


# ─────────────────────────────────────────────
# MODE: changelog
# ─────────────────────────────────────────────
def mode_changelog(args) -> int:
    result_path = Path(args.result)
    changelog_path = Path(args.changelog)

    if not result_path.exists():
        print('[WARN] registration_result.json 없음 — CHANGELOG 갱신 스킵')
        return 0

    result = json.loads(result_path.read_text(encoding='utf-8'))
    registered = result.get('registered', 0)
    variants   = result.get('variants', [])
    run_at     = result.get('run_at', utcnow())

    entry_lines = [
        f'## [Auto] Variant 자동 등록 — {today()}',
        '',
        f'- **워크플로우**: register_variant.yml v2.1',
        f'- **등록/갱신 Variant**: {registered}개',
        f'- **실행 시각**: {run_at}',
        '',
    ]
    for v in variants:
        entry_lines.append(f'  - `{v["id"]}` ({v["domain"]} / v{v["version"]}) — PE-1:{"✅" if v.get("pe1_passed") else "⚠"} PE-3:{"✅" if v.get("pe3_passed") else "⚠"}')
    entry_lines.append('')
    entry = '\n'.join(entry_lines)

    if changelog_path.exists():
        existing = changelog_path.read_text(encoding='utf-8')
        # 최상단에 삽입
        new_content = entry + '\n' + existing
    else:
        new_content = f'# CHANGELOG\n\n{entry}\n'

    changelog_path.write_text(new_content, encoding='utf-8')
    print(f'CHANGELOG.md 갱신 완료 ({registered}개 Variant)')
    return 0


# ─────────────────────────────────────────────
# main
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description='Variant Auto-Registration Script v2.1')
    parser.add_argument('--mode', choices=['validate', 'register', 'changelog'], required=True)
    parser.add_argument('--rule',      default='PE-1', help='검증 규칙 (PE-1 | PE-3)')
    parser.add_argument('--files',     default='',     help='대상 파일 목록 (공백 구분)')
    parser.add_argument('--index',     default='prompts/jv_fund/VARIANT_INDEX.json')
    parser.add_argument('--output',    default='output.json')
    parser.add_argument('--result',    default='registration_result.json')
    parser.add_argument('--changelog', default='CHANGELOG.md')
    args = parser.parse_args()

    mode_map = {'validate': mode_validate, 'register': mode_register, 'changelog': mode_changelog}
    sys.exit(mode_map[args.mode](args))


if __name__ == '__main__':
    main()
