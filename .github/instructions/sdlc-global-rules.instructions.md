---
description: Global SDLC rules that apply to all agents and all sessions in this workspace
applyTo: '**'
---

# Global SDLC Rules

Applies to **ALL agents** and **ALL sessions** automatically.  
No agent needs to repeat these rules individually.

---

## Branch Rule

- Always derive branch name as: `feature/{ISSUE_KEY_LOWERCASE}`
  - SCRUM-6 → `feature/scrum-6`
  - SCRUM-8 → `feature/scrum-8`
- If branch does not exist, create it from main first
- Never commit directly to main
- Never merge directly to main — raise PR only

---

## Folder Rule

- All SDLC docs live under: `.sdlc/{ISSUE_KEY}/`
- Create the folder if it does not exist
- Never read or write SDLC docs to project root
- Source code → `src/{ISSUE_KEY_SAFE}/`
- Tests → `tests/{ISSUE_KEY_SAFE}/`
- Workflows → `.github/workflows/{ISSUE_KEY}/`
- Docs → `docs/{ISSUE_KEY}/`
- PR description → `.sdlc/{ISSUE_KEY}/`
- CHANGELOG.md → repo root

---

## Python Safety Rule

- `{ISSUE_KEY_SAFE}` = hyphens replaced with underscores
  - SCRUM-6 → `SCRUM_6`
  - SCRUM-8 → `SCRUM_8`
- Always use `{ISSUE_KEY_SAFE}` for:
  - `src/` folder names
  - `tests/` folder names
  - Any Python module or package names
- Hyphens **allowed** in:
  - `.sdlc/{ISSUE_KEY}/` folder names
  - `.github/workflows/{ISSUE_KEY}/` folder names
  - Branch names `feature/{ISSUE_KEY_LOWERCASE}`
- Never use hyphens in Python package or module names

---

## Commit Rule

- Always show a preview of generated files to the user
- Always ask for confirmation before committing
- Never commit without explicit user confirmation
- Always push to `feature/{ISSUE_KEY_LOWERCASE}` after committing
- Never push directly to main

---

## File Not Found Rule

- If any required input file is missing, notify the user clearly and stop
- Never proceed with missing dependencies

---

## Code Quality Rule

- Always write clean, well-commented code
- Follow DRY principles — no duplicated logic
- Never hardcode secrets or credentials
- Infer technology stack from `architecture.md` only; never assume a language or framework
- All function names must be self-explanatory

---

## Code Structure Rule

- Never write code to repo root level
- Never mix code from different stories
- Always derive all folder paths from `{ISSUE_KEY}`
- Story-scoped paths are **mandatory**:
  - `src/{ISSUE_KEY_SAFE}/` NOT `src/`
  - `tests/{ISSUE_KEY_SAFE}/` NOT `tests/`
  - `.github/workflows/{ISSUE_KEY}/` NOT `.github/workflows/`

---

## Handoff Rule

- When all steps are complete and committed, output this exact line:  
  `SDLC_NEXT: {ISSUE_KEY}`
- If anything failed, output:  
  `SDLC_ERROR: {ISSUE_KEY} - [reason]`
- This signals the hooks to trigger the next agent
- **Exception:** `sdlc-pr-agent` outputs a completion summary instead — it is the final agent

---

## Security Rule

- Never use PATs, deploy keys, or external secrets
- Use `GITHUB_TOKEN` only for GitHub operations
- Never expose credentials in any generated file
- Never commit `.env` files or secret configs