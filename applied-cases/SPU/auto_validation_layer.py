"""
SPU v3.0 Auto-Validation Layer
Red Team 연동 + E-0N 검증 8주기
SSoT: https://www.notion.so/34e55ed436f08122b7a3f2c632e69a12
"""

import re
from typing import Dict, List, Tuple
from datetime import datetime


# --- E-0N 검증 주기 ---
E0N_CHECKS = {
    'E-01': 'SHA/목록 불일치',
    'E-02': '상태값 누락 (설명없는 TODO)',
    'E-03': '버전 역행 (낮은 번호로 덮어쓰기)',
    'E-04': '구조 불일치 (섹션 누락/중복)',
    'E-05': 'SSOT 맴크 불일치',
    'E-06': '슬레이브 충돌 (병렬 통합 실패)',
    'E-07': '필수 필드 누락',
    'E-08': '앞득 없는 데이터 삽입'
}


class AUTO_VALIDATION_LAYER:
    """SPU v3.0 자동 검증 계층 - E-0N + Red Team 연동"""

    def __init__(self, mode: str = 'full'):
        self.mode = mode  # 'full', 'blue_only', 'red_only'
        self.results: Dict[str, List] = {'blue': [], 'red': [], 'pass': [], 'fail': []}
        self.timestamp = datetime.now().isoformat()

    def blue_team_validate(self, document: dict) -> List[Tuple[str, bool, str]]:
        """Blue Team: 표준 검증 실행"""
        checks = []

        # E-07: 섹션 완성도 (SPU 문서 10개 섹션)
        required_sections = ['§1', '§2', '§3', '§4', '§5', '§6', '§7', '§8', '§9', '§10']
        content = document.get('content', '')
        missing = [s for s in required_sections if s not in content]
        checks.append(('E-07', len(missing) == 0, f'Missing sections: {missing}' if missing else 'ALL CLEAR'))

        # E-03: 버전 순서 검증
        version_pattern = r'v(\d+\.\d+)'
        versions = [float(v) for v in re.findall(version_pattern, content)]
        is_monotonic = all(versions[i] <= versions[i+1] for i in range(len(versions)-1)) if len(versions) > 1 else True
        checks.append(('E-03', is_monotonic, 'Version order valid' if is_monotonic else 'VERSION REGRESSION DETECTED'))

        # E-07: KPI 필드 존재
        has_kpi = 'KPI' in content or 'kpi' in content.lower()
        checks.append(('E-07b', has_kpi, 'KPI field present' if has_kpi else 'KPI MISSING - AUTO-INSERT TEMPLATE'))

        # E-05: SSOT 맵 포함
        has_ssot = 'notion.so' in content or 'SSOT' in content
        checks.append(('E-05', has_ssot, 'SSOT link present' if has_ssot else 'SSOT LINK MISSING'))

        self.results['blue'] = checks
        return checks

    def red_team_validate(self, document: dict) -> List[Tuple[str, bool, str]]:
        """Red Team: 가정 공격 및 구조적 시나리오 탐색"""
        checks = []
        content = document.get('content', '')

        # RT-01: DPU 충돌 검증
        has_dpu_comparison = 'DPU' in content
        checks.append(('RT-01', has_dpu_comparison,
                        'DPU comparison present' if has_dpu_comparison else 'WARNING: DPU 충돌 분석 누락'))

        # RT-02: NVIDIA 대응 시나리오
        has_nvidia = 'NVIDIA' in content
        checks.append(('RT-02', has_nvidia,
                        'NVIDIA scenario present' if has_nvidia else 'WARNING: NVIDIA 대응 시나리오 누락'))

        # RT-03: 리스크 항목
        has_risk = '리스크' in content or 'risk' in content.lower() or 'E-0N' in content
        checks.append(('RT-03', has_risk,
                        'Risk section present' if has_risk else 'CRITICAL: 리스크 항목 누락'))

        # RT-04: 단가 근거 존재
        has_price = '$' in content or '단가' in content
        checks.append(('RT-04', has_price,
                        'Price basis present' if has_price else 'WARNING: 단가 근거 누락'))

        self.results['red'] = checks
        return checks

    def run_full_validation(self, document: dict) -> dict:
        """Blue + Red Team 연속 실행 → 통합 리포트"""
        blue_results = self.blue_team_validate(document)
        red_results = self.red_team_validate(document)

        all_checks = blue_results + red_results
        passed = sum(1 for _, ok, _ in all_checks if ok)
        failed = sum(1 for _, ok, _ in all_checks if not ok)

        e0n_status = '파랑' if failed == 0 else ('주황' if failed <= 2 else '빨강')

        report = {
            'timestamp': self.timestamp,
            'e0n_status': e0n_status,
            'total_checks': len(all_checks),
            'passed': passed,
            'failed': failed,
            'blue_team': blue_results,
            'red_team': red_results,
            'recommendation': self._generate_recommendation(all_checks)
        }
        return report

    def _generate_recommendation(self, checks: List[Tuple]) -> str:
        failures = [(check_id, msg) for check_id, ok, msg in checks if not ok]
        if not failures:
            return '✅ E-0N ALL CLEAR - 맨다 시노드로 진행 가능'
        recs = [f'[{cid}] {msg}' for cid, msg in failures]
        return '\n'.join(['⚠️ 다음 항목들을 수정하세요:'] + recs)


# --- 실행 예시 ---
if __name__ == '__main__':
    validator = AUTO_VALIDATION_LAYER(mode='full')
    test_doc = {
        'content': '§1 SPU 개념 §2 버전 §3 고객 §4 NVIDIA §5 전략 §6 조직 §7 M&A §8 연계 §9 E-0N 리스크 §10 KPI $1k~$3k SSOT notion.so DPU NVIDIA'
    }
    report = validator.run_full_validation(test_doc)
    print(f'E-0N Status: {report["e0n_status"]} | {report["passed"]}/{report["total_checks"]} PASS')
