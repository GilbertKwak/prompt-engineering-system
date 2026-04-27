# 💻 Usage Commands — JV Fund Prompt System

> **Version**: 1.0 | **Updated**: 2026-04-27 | **Author**: Gilbert Kwak

---

## 🔷 1. 기본 검증 명령어

```bash
# Master Prompt v5 검증 (전체 룰)
python automation/auto_validate_jv.py \
  --file prompts/jv_fund/master_prompt_v5.md \
  --rules PE-1,PE-3,PE-5 \
  --verbose

# 특정 룰만 검증
python automation/auto_validate_jv.py \
  --file prompts/jv_fund/master_prompt_v5.md \
  --rules PE-1 \
  --output results/pe1_check.json

# 전체 jv_fund 디렉터리 일괄 검증
for f in prompts/jv_fund/*.md; do
  python automation/auto_validate_jv.py --file "$f" --rules PE-1,PE-3,PE-5 --verbose
done
```

---

## 🔷 2. Git 워크플로우 명령어

```bash
# 신규 분석 브랜치 생성
git checkout -b feat/jv-analysis-$(date +%Y%m%d)

# 변경사항 커밋
git add prompts/jv_fund/
git commit -m "feat(jv-fund): Update [DOMAIN] analysis [STAGE] — $(date +%Y-%m-%d)"

# 검증 후 push
python automation/auto_validate_jv.py --file prompts/jv_fund/master_prompt_v5.md --rules PE-1,PE-3,PE-5
git push origin feat/jv-analysis-$(date +%Y%m%d)

# PR 생성
gh pr create \
  --title "[JV] [DOMAIN] Analysis Update — $(date +%Y-%m-%d)" \
  --body "## 변경 내용\n\n- Domain: [입력]\n- Stage: [입력]\n- Validation: PE-1 ✅ PE-3 ✅ PE-5 ✅\n\n## Notion 링크\nhttps://www.notion.so/34f55ed436f081c08fececa8dd7577f9" \
  --label "jv-analysis"
```

---

## 🔷 3. GitHub Issue 생성 명령어

```bash
# JV 분석 신규 이슈
gh issue create \
  --title "[JV Analysis] [DOMAIN] Screening — $(date +%Y-%m-%d)" \
  --label "jv-analysis,screening" \
  --body "## JV 분석 요청\n\n- **Domain**: HBM / sCO2 / Thermal / AI-DC\n- **Stage**: Screening\n- **Target Partner**: \n- **Budget Range**: \n- **FU Reference**: FU-XXX\n\n## 사용 프롬프트\n\`prompts/jv_fund/master_prompt_v5.md\`\n\n## 체크리스트\n- [ ] PE-1 검증 완료\n- [ ] PE-3 시나리오 포함\n- [ ] Notion 업데이트"

# 월간 리뷰 이슈 수동 생성
gh issue create \
  --title "[Monthly Review] JV Prompt — $(date +%Y-%m)" \
  --label "monthly-review,jv-analysis" \
  --body "## 월간 JV 프롬프트 리뷰\n\n- [ ] PE-1 준수율\n- [ ] PE-3 최신성\n- [ ] PE-5 커버리지\n- [ ] Notion 동기화"
```

---

## 🔷 4. GitHub Actions 수동 트리거

```bash
# 워크플로우 수동 실행
gh workflow run jv_prompt_validate.yml \
  --field target_file=prompts/jv_fund/master_prompt_v5.md \
  --field rules=PE-1,PE-3,PE-5

# 워크플로우 상태 확인
gh run list --workflow=jv_prompt_validate.yml --limit 5

# 최근 실행 결과 다운로드
gh run download $(gh run list --workflow=jv_prompt_validate.yml --limit 1 --json databaseId -q '.[0].databaseId')
```

---

## 🔷 5. Shell Alias 등록 (권장)

```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
alias jv-validate='python ~/workspace/prompt-engineering-system/automation/auto_validate_jv.py --rules PE-1,PE-3,PE-5'
alias jv-validate-v='python ~/workspace/prompt-engineering-system/automation/auto_validate_jv.py --rules PE-1,PE-3,PE-5 --verbose'
alias jv-issue='gh issue create --label "jv-analysis" --title'
alias jv-review='gh issue create --title "[Monthly Review] JV Prompt $(date +%Y-%m)" --label monthly-review,jv-analysis'
alias jv-run='gh workflow run jv_prompt_validate.yml'
alias jv-status='gh run list --workflow=jv_prompt_validate.yml --limit 5'

# 적용
source ~/.bashrc  # 또는 source ~/.zshrc
```

---

## 🔷 6. 빠른 참조 테이블

| 작업 | 명령어 |
|------|--------|
| 빠른 검증 | `jv-validate --file <path>` |
| 상세 검증 | `jv-validate-v --file <path>` |
| 이슈 생성 | `jv-issue "[제목]"` |
| 월간 리뷰 | `jv-review` |
| 워크플로우 실행 | `jv-run` |
| 워크플로우 상태 | `jv-status` |
| Notion 허브 | https://www.notion.so/34f55ed436f081c08fececa8dd7577f9 |

---

## 🔗 SSOT Links

- **GitHub**: https://github.com/GilbertKwak/prompt-engineering-system/tree/main/prompts/jv_fund
- **Notion Hub**: https://www.notion.so/34f55ed436f081c08fececa8dd7577f9
- **PE Lab**: https://www.notion.so/33955ed436f081cc9f0bd014d631aa7b
