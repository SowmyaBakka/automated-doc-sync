# SDLC State-Based Orchestration

This repository now uses state-based chaining for SDLC agents.

## What Triggers Next Agent

The post-commit hook runs `.github/hooks/run-sdlc-hook.ps1`.

The runner does not parse commit messages. It only advances when:

1. `.sdlc/{ISSUE_KEY}/pipeline-state.json` was part of the latest commit.
2. `status` is `completed` and `approved` is `true`.
3. The stage completion artifact exists.

If all checks pass, the runner invokes the next stage agent from `.github/hooks/sdlc-pipeline.json`.

## Start a New Story

Run:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File ".github/hooks/start-sdlc-story.ps1" -IssueKey SCRUM-10
```

This command now does all startup setup in one step:

1. Ensures branch `feature/scrum-10` exists.
2. Creates it from `main` (or `origin/main`) when missing.
3. Switches to that branch.
4. Initializes `.sdlc/SCRUM-10/pipeline-state.json` at `requirements`.
5. Starts `sdlc-requirements-agent`.

## Direct Agent Start (Issue Key Only)

You can start by invoking only the requirements agent with an issue key.

Example:

```text
@sdlc-requirements-agent SCRUM-10
```

The requirements agent preflight now bootstraps branch and state automatically:

1. Ensures `feature/{ISSUE_KEY_LOWERCASE}` exists and switches to it.
2. Initializes `.sdlc/{ISSUE_KEY}/pipeline-state.json` when missing.
3. Proceeds with requirement generation and normal commit/approval flow.

After the requirements commit, post-commit hook chaining continues automatically.

## Resume an Existing Story

1. Open `.sdlc/{ISSUE_KEY}/pipeline-state.json`.
2. Set `currentStage`, `status`, `approved`, and `artifacts` to the current truth.
3. Commit that state update with the stage artifact.

After commit, the hook will evaluate state and launch the next agent if ready.

## Stage IDs

- `requirements`
- `architecture`
- `design-review`
- `impl-plan`
- `implementation`
- `code-review`
- `verify`
- `pr`

## Notes

- `implementation` normally advances after `implementation-summary.md` exists and state is marked complete; if the summary is missing, the hook accepts `implementation-source` plus `implementation-tests` as fallback evidence for backward compatibility.
- `pr` is terminal (`nextStage` is null).
- Keep all SDLC documents in `.sdlc/{ISSUE_KEY}/`.