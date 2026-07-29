---
name: generate-pr-description
description: Generates production-ready PR description with 5 mandatory sections and CHANGELOG.md entry. Use after verify-and-report passes, before raising PR.
applyTo: '**'
---

# generate-pr-description Skill

Generates PR description and changelog from SDLC documents.

**Used by:** `sdlc-pr-agent` (orchestrator that calls this skill)

---

## When to Use

- ✓ After verify.md shows ✅ Verified verdict
- ✓ All code committed to `feature/{ISSUE_KEY_LOWERCASE}`
- ✓ Before raising PR to main

## Input Required

Read these first:
- `.sdlc/{ISSUE_KEY}/requirements.md`
- `.sdlc/{ISSUE_KEY}/verify.md` (test results)
- `.sdlc/{ISSUE_KEY}/code-review.md` (findings)
- `git diff main..feature/{ISSUE_KEY_LOWERCASE} --name-status`
  (to get actual list of changed files)

---

## The 5 Mandatory Sections

### 1. Summary (2-3 sentences)
- What was built
- Reference the JIRA issue {ISSUE_KEY}
- Key value delivered
- Derive entirely from requirements.md user story

Example structure (do not copy — derive from story):
> "This PR delivers [what was built] as specified 
> in {ISSUE_KEY}. All functional requirements are met 
> and all tests pass."

### 2. Changes Made
- Run `git diff main..feature/{ISSUE_KEY_LOWERCASE} 
  --name-status` to get actual changed files
- Group by category: SDLC Docs, Source Code, 
  Tests, Config
- Include reason for each change
- Use table format:

| File | Change | Reason |
|------|--------|--------|
| `src/{ISSUE_KEY_SAFE}/main.py` | Created | [derive from impl-plan.md] |
| `tests/{ISSUE_KEY_SAFE}/test_x.py` | Created | [derive from impl-plan.md] |

### 3. Test Evidence
- Copy full test output from `verify.md`
- Include: passed count, failed count, duration
- Include FR coverage table from `verify.md`
- Include NFR coverage table from `verify.md`

Example structure (populate from verify.md):
============================= test session results =============================

{TEST_COUNT} passed in {DURATION}s
| FR ID | Requirement | Test | Status |
|-------|-------------|------|--------|
| FR-1 | [from requirements.md] | [from verify.md] | ✅/❌ |

### 4. Known Limitations
Derive ALL of these from SDLC documents:
- Out of scope items from requirements.md
- Tasks skipped or blocked from impl-plan.md
- Any ⚠️ warnings from verify.md
- Any ⚠️ warnings from code-review.md
- Open questions from requirements.md

Example structure (derive from documents):
> "- [out of scope item from requirements.md]
> - [skipped task from impl-plan.md]
> - [warning from verify.md]"

### 5. Reviewer Checklist
Derive checklist items from requirements.md FRs:
 Requirements met — all FRs implemented
 All tests pass
 No hardcoded secrets or credentials
 Architecture followed as designed
 Code review findings addressed
 Output document quality verified
 Branch is up to date with main
 PR description is complete
 Changelog entry is present
---

## CHANGELOG.md Format

Save to repo root: `CHANGELOG.md`

```markdown
# Changelog

## [{ISSUE_KEY}] - {TODAY_DATE}

### Added
- [derive from impl-plan.md completed tasks]

### Changed
- [derive from design-review.md agreed decisions]

### Fixed
- [derive from code-review.md fixes applied]

### Known Limitations
- [derive from requirements.md out of scope]
- [derive from verify.md warnings]
```

---

## Output Files

- PR description → `.sdlc/{ISSUE_KEY}/pr-description.md`
- Changelog → `CHANGELOG.md` (repo root)

---

## Quality Checks Before Saving
- ✅ All 5 sections present and filled
- ✅ No placeholder text remaining
- ✅ No hardcoded story-specific content
- ✅ Test evidence matches verify.md exactly
- ✅ Known limitations sourced from documents
- ✅ CHANGELOG entry follows correct format
- ✅ {ISSUE_KEY} used — never hardcoded story name

---

## Rules

- Never skip any of the 5 sections
- Never skip the CHANGELOG entry
- Always extract data from SDLC docs — never fabricate
- Always use {ISSUE_KEY} — never hardcode story names
- Always show preview to user before committing
- Always commit both files together
- Commit message: 
  `"feat: add PR description and changelog for {ISSUE_KEY}"`
- Follow global Instructions for all commit/push operations
- Never raise PR without user confirmation