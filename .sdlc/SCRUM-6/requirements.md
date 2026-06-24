# Requirements for SCRUM-6

## Original User Story
As a backend developer on a growing team, I want all markdown documentation files to automatically publish to GitHub Pages whenever I merge a PR to main, so that my team always reads up-to-date docs without anyone manually copying files.

## Functional Requirements

| ID | Requirement |
| --- | --- |
| FR-1 | The workflow shall trigger on every push to the `main` branch. |
| FR-2 | The workflow shall process only markdown files under `docs/` (`docs/**/*.md`). |
| FR-3 | The workflow shall exclude `.sdlc/`, `node_modules/`, `.github/`, and `venv/` from all sync operations. |
| FR-4 | The publish target shall be the `gh-pages` branch. |
| FR-5 | The published output shall mirror the source `docs/` folder structure exactly on `gh-pages`. |
| FR-6 | The workflow shall process incremental changes only (added, modified, renamed, deleted) and shall not perform full rebuild publishing. |
| FR-7 | For transient per-file sync failures, the workflow shall retry up to 3 times with a 5-second wait between retries. |
| FR-8 | The workflow shall attempt all eligible files even if some files fail after retries. |
| FR-9 | The workflow summary shall include full lists of successful files, failed files, and deleted files. |
| FR-10 | The workflow shall fail at the end of the run if any eligible file failed after retries. |
| FR-11 | When a source in-scope file is deleted, the corresponding file on `gh-pages` shall be deleted. |
| FR-12 | Authentication for publishing shall use only GitHub Actions `GITHUB_TOKEN`. |

## Non-Functional Requirements

| ID | Requirement |
| --- | --- |
| NFR-1 | No PATs, deploy keys, or external secrets shall be used. |
| NFR-2 | The solution shall prioritize reliability by combining bounded retries with end-of-run aggregate error reporting. |
| NFR-3 | The workflow output shall be auditable and clear enough to identify file-level outcomes in one run. |
| NFR-4 | The implementation shall be maintainable as repository-as-code in GitHub Actions. |
| NFR-5 | The sync logic shall remain incremental and efficient by operating only on detected deltas. |

## Out of Scope
- Publishing files outside `docs/`.
- Publishing any non-markdown file type.
- Publishing `.sdlc` artifacts or any content under excluded folders.
- Using external deployment services or non-GitHub secret stores.
- Full-site republish when only a subset of files changed.
