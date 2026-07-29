---
name: code-review-checklist
description: Performs structured code review across 7 areas (correctness, security, error handling, test coverage, clarity, DRY, dependencies). Use when implementing stories before PR approval.
applyTo: '**'
---

## code-review-checklist Skill

Evaluates code against requirements.md and architecture.md across 7 mandatory review areas.

### When to Use
- After implementation complete and tests pass
- Before raising PR to main
- As quality gatekeeper per SDLC rules

### Input Required
- `.sdlc/{ISSUE_KEY}/requirements.md` (read first)
- `.sdlc/{ISSUE_KEY}/architecture.md` (design context)
- Code files: `src/{ISSUE_KEY_SAFE}/`
- Test files: `tests/{ISSUE_KEY_SAFE}/`

[rest of your content...]

### Output Location
Save as: `.sdlc/{ISSUE_KEY}/code-review.md`

### Status Criteria
- **✅ Pass:** All criteria met; no issues
- **⚠️ Warning:** Minor fixable issues (e.g., one FR untested)
- **❌ Fail:** Critical blockers (e.g., hardcoded secrets, missing FR implementation)

### Next Steps
- ✅ Pass → Proceed to PR
- ⚠️ Warning → Fix issues or document decision
- ❌ Fail → Output `SDLC_ERROR: {ISSUE_KEY} - [reason]`; fix and re-review