# Requirements for SCRUM-6

## Original User Story
As a backend developer on a growing team, I want all markdown documentation files to automatically publish to GitHub Pages whenever I merge a PR to main, so that my team always reads up-to-date docs without anyone manually copying files.

## Functional Requirements

| ID | Requirement |
| --- | --- |
| FR-1 | The system shall trigger the documentation sync workflow on every push to the `main` branch. |
| FR-2 | The system shall include in scope all `*.md` files located at the repository root. |
| FR-3 | The system shall include in scope all `*.md` files located anywhere under the `/docs` directory. |
| FR-4 | The system shall exclude any files under `node_modules/`, `.github/`, and `venv/` from sync processing. |
| FR-5 | The system shall detect and process only markdown files that were added, modified, renamed, or deleted since the previous publish state, rather than rebuilding or republishing the entire documentation set. |
| FR-6 | The system shall publish synced content to the `gh-pages` branch. |
| FR-7 | The system shall mirror the same repository-relative folder structure for published markdown files on the `gh-pages` branch. |
| FR-8 | The system shall remove published files from the `gh-pages` branch when the corresponding in-scope source markdown files are deleted from `main`. |
| FR-9 | The system shall attempt processing for all eligible file changes in a workflow run before determining overall workflow success or failure. |
| FR-10 | The system shall produce a workflow summary showing, at minimum, which files were successfully synced, which files failed to sync, and which files were deleted from the published site. |
| FR-11 | The system shall mark the workflow run as failed if one or more file sync operations fail, after all eligible file operations have been attempted. |
| FR-12 | The system shall use only the default GitHub Actions `GITHUB_TOKEN` for authentication to update the `gh-pages` branch. |

## Non-Functional Requirements

| ID | Requirement |
| --- | --- |
| NFR-1 | The solution shall require no personal access tokens, deploy keys, or external secrets beyond the default GitHub Actions `GITHUB_TOKEN`. |
| NFR-2 | The solution shall provide clear failure visibility by surfacing an end-of-run summary of successes and failures in the workflow output. |
| NFR-3 | The workflow shall be idempotent for unchanged in-scope files, avoiding unnecessary republishes when no relevant markdown changes are detected. |
| NFR-4 | The implementation shall minimize publish work by operating incrementally on changed and deleted files only. |
| NFR-5 | The workflow configuration shall be maintainable within the repository as code and compatible with GitHub Actions and GitHub Pages branch-based publishing. |

## Out of Scope
- Syncing non-markdown file types such as images, PDFs, HTML, or generated assets.
- Syncing markdown files outside the repository root and `/docs` directory.
- Processing files inside `node_modules/`, `.github/`, or `venv/`.
- Using external deployment services, third-party sync platforms, or additional secret stores.
- Publishing to destinations other than the `gh-pages` branch.
- Rebuilding the entire documentation site on every run when only a subset of files changed.
