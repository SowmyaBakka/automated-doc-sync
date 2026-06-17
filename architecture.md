# Architecture for SCRUM-6

## Overview
This architecture implements incremental markdown sync from `main` to `gh-pages` on GitHub-hosted Actions (`ubuntu-latest`) using only `GITHUB_TOKEN`. It is optimized for repositories up to 1 GB and up to 500 markdown files, with a target workflow runtime under 5 minutes.

The initial implementation supports `gh-pages` publishing, while defining extension points for future destinations.

## High-Level Component Diagram
```mermaid
flowchart LR
    A[Push to main] --> B[GitHub Actions Workflow Trigger]
    B --> C[Checkout main]
    B --> D[Checkout gh-pages worktree]
    C --> E[Change Detector]
    E -->|added/modified/renamed/deleted markdown set| F[Scope Filter]
    F --> G[Sync Planner]
    G --> H[Destination Adapter: gh-pages]
    H --> I[File Copier and Deleter]
    I --> J[Commit and Push gh-pages]
    J --> K[Workflow Summary Generator]
    K --> L[Job Result: success/failure]

    M[Future Adapter Interface] -.-> H
```

## Technology Choices and Justification
- Runtime: GitHub Actions on `ubuntu-latest`.
- Workflow orchestration: GitHub Actions YAML.
- Sync engine: Python 3 script.
- Git operations: native `git` commands.
- Authentication: built-in `GITHUB_TOKEN` only.

Justification:
- Python provides robust path handling and deterministic filtering logic for incremental sync.
- Native git diffing is the fastest and most reliable way to detect changed/deleted files without full scans.
- `ubuntu-latest` provides predictable execution, fast startup, and standard tooling.
- `GITHUB_TOKEN` satisfies security constraints while enabling branch updates.

## Data Flow: Push to Published GitHub Pages
1. A push event on `main` starts the workflow.
2. The workflow checks out `main` and fetches `gh-pages`.
3. Change Detector computes file deltas from git history (added, modified, renamed, deleted).
4. Scope Filter keeps only markdown files that match:
- root-level `*.md`
- any `*.md` under `docs/`
- excludes `node_modules/`, `.github/`, `venv/`
5. Sync Planner builds operation lists:
- copy/update operations for added/modified/renamed targets
- delete operations for removed source files
6. Destination Adapter (`gh-pages`) maps source paths to mirrored target paths.
7. File executor performs all operations, collecting per-file result status.
8. Branch publisher commits and pushes `gh-pages` updates when there are changes.
9. Summary generator writes a run summary (successes, failures, deletions).
10. Workflow exits with failure if any operation failed, after all operations were attempted.

## Key Components and Responsibilities
- Workflow Trigger
- Starts on push to `main`.

- Checkout Manager
- Retrieves `main` and `gh-pages` content for comparison and publishing.

- Change Detector
- Uses git diff to detect incremental markdown changes only.

- Scope Filter
- Enforces inclusion and exclusion rules for eligible files.

- Sync Planner
- Produces deterministic operation plan for copy/update/delete.

- Destination Adapter Interface
- Defines methods like `map_path()`, `apply_copy()`, `apply_delete()`, `publish()`.
- Current implementation: `GhPagesAdapter`.
- Future implementations can target S3/artifacts/other branches without rewriting core logic.

- Operation Executor
- Executes planned operations and records per-file outcomes.

- Summary Reporter
- Produces a workflow summary table for successful syncs, failures, and deletions.

- Failure Controller
- Marks overall job failed if any file operation fails, but only after all operations complete.

## GitHub Actions Workflow Structure
- Job: `sync-docs-to-gh-pages`
- Runner: `ubuntu-latest`
- Permissions:
- `contents: write` (required for `gh-pages` push)

Steps:
1. `actions/checkout` for `main` with sufficient fetch depth for diff.
2. Setup Python runtime.
3. Fetch `gh-pages` branch and prepare publish worktree.
4. Run Python sync script:
- collect changed/deleted files
- filter to in-scope markdown
- mirror structure to destination
- apply deletes
- record per-file status
5. Commit/push `gh-pages` if changed.
6. Emit summary to workflow summary output.
7. Exit non-zero if any file operation failed.

## Performance and Scalability Design
- Incremental-by-default: no full rebuild path in normal operation.
- Single-pass filtering and planning over changed set.
- Bounded file operations aligned to changed set size, not total repository size.
- Supports repos up to 1 GB and up to 500 markdown files under a 5-minute runtime target by minimizing checkout and copy scope.
- Avoids unnecessary commits when no effective content changes are detected.

## Reliability and Failure Model
- Best-effort per-file processing across the full operation set.
- End-of-run aggregated status controls final job state.
- Failures include file-level errors and git publish errors.
- Summary remains available even on failure for fast troubleshooting.

## Security and Compliance
- Uses only `GITHUB_TOKEN`.
- No PATs, deploy keys, or external secrets.
- No external sync services.
