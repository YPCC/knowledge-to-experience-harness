---
name: open-code-review
description: "Performs AI-powered code review on any Git repository using the ocr CLI from alibaba/open-code-review. Use when the user asks to review code, review a pull request, review changes, review a commit, scan a codebase, or check quality/security issues in a repo."
type: workflow
lifecycle: active
---

# Open Code Review Skill

Invoke [alibaba/open-code-review](https://github.com/alibaba/open-code-review) (`ocr` CLI) to review any Git repository. Produces structured, line-level comments with severity and category. Works on the knowledge-to-experience-harness repo, cms-policy-as-code, or any other public/private repo.

## Prerequisites

- Git >= 2.41
- Node.js >= 18 (for npm install)
- `ocr` CLI: `npm install -g @alibaba-group/open-code-review`
- LLM configured: `ocr config provider` then `ocr config model` (OpenAI-compatible, Anthropic, Bedrock, etc.), or use Delegation Mode.

If `ocr` is missing, install it and continue. Do not probe existence first.

## Core Workflow

1. **Gather context**  
   Identify the target (current workspace, branch range, specific commit, or full scan). Extract a short business/requirement background from the user request or repo README.

2. **Run review**  
   Always use `--audience agent` and prefer `--format json` or `--output /tmp/ocr_review.json` for full results.  
   Pass background: `--background "concise context"`.

   | Goal | Command |
   |------|---------|
   | Working tree changes | `ocr review --audience agent --background "context" --format json --output /tmp/ocr_review.json` |
   | Branch vs main | `ocr review --audience agent --background "context" --from main --to <branch> --format json --output /tmp/ocr_review.json` |
   | Single commit | `ocr review --audience agent --background "context" --commit <sha> --format json --output /tmp/ocr_review.json` |
   | Full codebase / directory (no diff) | `ocr scan --path . --audience agent --format json --output /tmp/ocr_scan.json` |
   | Preview only | `ocr review --preview` |

3. **Parse & report**  
   Read the JSON output. Group findings by severity (critical / high / medium). Discard low severity. Present with file:line, category, and recommendation. Include token/time summary if available.

4. **Optional fix**  
   Only apply fixes if the user explicitly asks. Focus on critical/high/medium. Verify before committing.

## Custom Rules

Place project rules in `<repo>/.opencodereview/rule.json` or pass `--rule path/to/rule.json`.

Example rule.json:
```json
{
  "rules": [
    {
      "path": "**/*.{py,ts,tsx,js}",
      "rule": "Check for security issues, null handling, and clear error paths. Prefer provenance and modular design matching the harness principles.",
      "merge_system_rule": true
    }
  ]
}
```

## Output Template

```markdown
## Code Review Results

**Files reviewed**: N  
**Issues found**: X critical, Y high, Z medium

### Critical
- **`path/to/file.py:42`** [security] — Description  
  > Recommendation: ...

### High
...

### Medium
...
```

If none: "Review complete — no critical, high, or medium issues found."

## Notes for Harness / Any Repo

- Review the harness itself, the React platform, scripts, or external sources like cms-policy-as-code.
- For generated video code or platform code, emphasize clarity, provenance, and modularity.
- Combine with the evaluation-framework.md for post-review checks.
- Results can feed into generation-log.md or platform metadata.

See official docs: https://github.com/alibaba/open-code-review and https://open-codereview.ai
