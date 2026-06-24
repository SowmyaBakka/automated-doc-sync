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
- `git diff main..feature/{ISSUE_KEY_LOWERCASE} --name-status` (changed files)

---

## The 5 Mandatory Sections

### 1. Summary (2-3 sentences)
- What was built
- Reference the JIRA issue (SCRUM-N)
- Key value delivered

Example:
> "This PR delivers a complete REST API for personal to-do items with 3 endpoints, thread-safe JSON persistence, and 17 passing tests. All 10 functional requirements from SCRUM-8 are met."

### 2. Changes Made
- Group by category: SDLC Docs, Source Code, Tests, Config
- Include reason for each change
- Use table format

Example:
| File | Change | Reason |
|------|--------|--------|
| `main.py` | Created | FastAPI entry point with lifespan |
| `routes/todos.py` | Created | 3 REST endpoints (POST, GET, GET/{id}) |
| `test_store.py` | Created | 8 unit tests for JsonStore |

### 3. Test Evidence
- Copy full test output from `verify.md`
- Include: passed count, failed count, duration
- Include FR coverage table from `verify.md`

Example:
```
============================= test session starts =============================
17 passed in 0.47s
```

| FR ID | Requirement | Test | Status |
|-------|-------------|------|--------|
| FR-1 | POST /todos accepts title | test_post_todos_valid_body_returns_201 | ✅ |

### 4. Known Limitations
- Out of scope items (from requirements.md)
- Implementation constraints
- Performance/scale limits

Example:
> "- No authentication (design by spec)
> - JSON file only (not production-scale)
> - Millisecond-precision IDs with collision handling"

### 5. Reviewer Checklist
- 8-10 verification items
- Format: `[ ] Item`

Example:
```
- [ ] Requirements met — all 10 FRs implemented
- [ ] All tests pass (17/17)
- [ ] No hardcoded secrets
- [ ] Architecture followed as designed
- [ ] Code review findings addressed
- [ ] Output documentation complete
```

---

## CHANGELOG.md Format

Save to repo root: `CHANGELOG.md`

```markdown
# Changelog

## [SCRUM-8] - 2026-06-23

### Added
- REST API with 3 endpoints (POST, GET, GET/{id})
- Thread-safe JSON file persistence
- 17 comprehensive tests

### Changed
- Updated .gitignore to exclude runtime data

### Fixed
- FR-4 compliance: 204 No Content on empty list

### Known Limitations
- No authentication (single shared list)
- JSON file only (not production-scale)
```

---

## Output Files

**PR Description:** `.sdlc/{ISSUE_KEY}/pr-description.md`  
**Changelog:** `CHANGELOG.md` (repo root)

---

## Rules

- Never skip any of the 5 sections
- Always extract data from SDLC docs, never synthesize
- Always show preview to user before committing
- Always commit both files together
- Commit message: `"feat: add PR description and changelog for {ISSUE_KEY}"`