---
name: verify-and-report
description: Comprehensive verification suite covering 
code tests, FR/NFR coverage mapping, and output document 
quality. Use after code-review-checklist passes and 
before raising PR.
applyTo: '**'
---

## verify-and-report Skill

Final quality gate: runs all tests, maps to requirements,
and validates output document before PR is raised.

### Relationship to sdlc-verify-agent
- `sdlc-verify-agent` — the AGENT that orchestrates
  the full verification session, handles user interaction,
  previews and commits verify.md
- `verify-and-report` — this SKILL contains the detailed
  verification logic that the agent executes
- The agent calls this skill; this skill does the work

### When to Use
- ✓ After code-review-checklist.md exists and passes
- ✓ After all implementation tasks are committed
- ✓ Before raising PR to main
- ✓ Final verification step in SDLC pipeline
- ✗ Do not run if code-review.md shows ❌ Failed

### Input Required
- `.sdlc/{ISSUE_KEY}/requirements.md`
- `.sdlc/{ISSUE_KEY}/architecture.md` (tech stack)
- `.sdlc/{ISSUE_KEY}/code-review.md` (must pass)
- Code: `src/{ISSUE_KEY_SAFE}/`
- Tests: `tests/{ISSUE_KEY_SAFE}/`
- Output document:
  * For doc-sync stories → published markdown files
  * For API stories → API response samples
  * For workflow stories → workflow run logs
  * For UI stories → rendered output or screenshots
  * When unclear → ask user to identify output file

### Pass/Fail Thresholds
- ✅ Pass: 100% of tests pass, all FRs covered
- ⚠️ Warning: up to 10% tests skipped, minor NFR gaps
- ❌ Fail: any test fails, any FR has zero coverage,
  any critical NFR unverified

---

## Workflow — Sequential, Each Part Depends on Previous
Part A (Code) must complete before Part B (Docs)
Part B must complete before Part C (Output)
If Part A fails → fix before running Part B
---

## PART A — Code Verification

### Step 1: Identify and Generate Missing Tests
- Unit tests: one per function/component
- Integration tests: test component interactions
- Happy path: normal expected inputs
- Edge cases:
  * Empty input
  * Missing files
  * Invalid data
  * Unauthorized access
- Each FR must have at least one test
- Generate missing tests before running

### Step 2: Run All Tests
Infer test framework from architecture.md:
- Python → pytest
- Node.js → jest or mocha
- Java → JUnit
- Go → go test
- Other → infer from dependencies

Run and capture:
- Exit code (0 = pass, non-zero = fail)
- Total tests run
- Passed / Failed / Skipped count
- Full error output and stack traces

Apply thresholds:
- 0 failures → ✅ Pass
- Any failure → ❌ Fail — fix before proceeding
- Skipped > 10% → ⚠️ Warning

### Step 3: FR Coverage Table

| FR ID | Requirement | Test Name | Status |
|-------|-------------|-----------|--------|
| FR-1 | ... | test_xx | ✅ Covered |
| FR-2 | ... | — | ❌ Not covered |

### Step 3b: NFR Coverage Table

| NFR ID | Requirement | How Verified | Status |
|--------|-------------|--------------|--------|
| NFR-1 | ... | timed run / scan | ✅ Verified |
| NFR-2 | ... | — | ❌ Not verified |

---

## PART B — Output Document Quality Check

### Step 4: Identify Output Document
Determine output document type from architecture.md:
- Doc-sync → published markdown on gh-pages
- REST API → sample API responses
- Workflow → workflow run summary
- Other → ask user if unclear

### Step 5: Quality Checklist

| Check | Status | Finding | Action |
|-------|--------|---------|--------|
| Content complete, not truncated | | | |
| All required sections present | | | |
| Content accurate vs requirements.md | | | |
| No broken links or references | | | |
| Formatting valid and consistent | | | |
| No placeholder or TODO items remaining | | | |
| Output matches user story specification | | | |
| No sensitive data exposed in output | | | |
| File encoding is UTF-8 | | | |
| Output file size is reasonable (< 10MB) | | | |

Thresholds:
- All ✅ → Part B passes
- Any ⚠️ → document and note in verify.md
- Any ❌ → fix before proceeding to Part C

---

## PART C — Generate verify.md

### Verification Metadata
Include at top of verify.md:
Verified by: sdlc-verify-agent
Date: {TODAY_DATE}
Branch: feature/{ISSUE_KEY_LOWERCASE}
Commit: {LATEST_COMMIT_SHA}
Status: ✅ Verified / ⚠️ Warning / ❌ Failed

### verify.md Structure

## Verification Metadata
- Date, branch, commit, overall status

## Code Verification
- Test Execution Summary
- FR Coverage Table
- NFR Coverage Table
- Issues found and fixed

## Output Document Quality Check
- Quality checklist results
- Issues found and recommended fixes

## Final Verification Verdict
- ✅ Verified — ready for PR
- ⚠️ Verified with warnings — minor issues noted
- ❌ Failed — fix required before PR

### Output Location
Save as: `.sdlc/{ISSUE_KEY}/verify.md`
Follow global commit/push rules from Instructions.

### Next Steps
- ✅ Verified → Output `SDLC_NEXT: {ISSUE_KEY}`
- ⚠️ Warning → Fix or document, then proceed
- ❌ Failed → Output `SDLC_ERROR: {ISSUE_KEY} - [reason]`
  fix and re-verify before proceeding

### Rules
- Always run Part A before Part B
- Always run Part B before Part C
- Never skip any part
- Always generate missing tests before running
- Always map every FR and NFR
- Infer technology from architecture.md only
- Never proceed to PR if verdict is ❌ Failed
- Follow global Instructions for all commit/push operations