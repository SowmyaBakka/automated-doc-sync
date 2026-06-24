# SCRUM-9 Pull Request

## 1. Summary

This PR delivers the SCRUM-9 personal expense tracking REST API for logging and viewing daily expenses through FastAPI endpoints backed by JSON-file persistence. It implements all functional requirements for create, list, category filtering, and category-summary retrieval, along with strict validation, deterministic error handling, and decimal-safe aggregation. Verification is complete: all SCRUM-9 tests pass and the story is ready for review.

## 2. Changes Made

### SDLC Docs

| File | Change | Reason |
|------|--------|--------|
| `.sdlc/SCRUM-9/requirements.md` | Created | Captures the approved user story, FR-1 through FR-5, NFR-1 through NFR-4, and story scope |
| `.sdlc/SCRUM-9/architecture.md` | Created | Defines the FastAPI, service, and JSON-store architecture plus error-handling strategy |
| `.sdlc/SCRUM-9/design-review.md` | Created | Records review findings and the agreed design corrections before implementation |
| `.sdlc/SCRUM-9/impl-plan.md` | Created | Breaks delivery into setup, core, testing, and release tasks |
| `.sdlc/SCRUM-9/code-review.md` | Created | Documents the review findings that were fixed before approval |
| `.sdlc/SCRUM-9/verify.md` | Created | Stores final verification evidence with full test output and FR/NFR coverage |

### Source Code

| File | Change | Reason |
|------|--------|--------|
| `src/SCRUM_9/main.py` | Created | Composes the FastAPI application and centralized exception handling |
| `src/SCRUM_9/models/expense.py` | Created | Defines request validation and normalized expense models |
| `src/SCRUM_9/routes/expenses.py` | Created | Exposes `POST /expenses`, `GET /expenses`, and `GET /expenses/summary/categories` |
| `src/SCRUM_9/services/expense_service.py` | Created | Implements add/list/filter/summary business logic with decimal-safe totals |
| `src/SCRUM_9/store/json_store.py` | Created | Provides JSON-file persistence, first-run initialization, fault contracts, locking, and atomic mutation |
| `src/SCRUM_9/README.md` | Created | Documents local usage, API contracts, and story-scoped implementation details |

### Tests

| File | Change | Reason |
|------|--------|--------|
| `tests/SCRUM_9/conftest.py` | Created | Supplies isolated temp-file fixtures for deterministic test execution |
| `tests/SCRUM_9/test_expenses_api.py` | Created | Covers happy-path create/list/filter API behavior |
| `tests/SCRUM_9/test_validation.py` | Created | Verifies strict validation rules and 400 responses |
| `tests/SCRUM_9/test_summary_and_errors.py` | Created | Covers category summary plus corrupted JSON, write-failure, and auto-init fault paths |
| `tests/SCRUM_9/test_service_summary.py` | Created | Verifies decimal-safe aggregation, exact filtering, and concurrent create regression coverage |
| `tests/SCRUM_9/test_isolation.py` | Created | Confirms fixture isolation and clean storage state between tests |

### Config and Docs

| File | Change | Reason |
|------|--------|--------|
| `.github/workflows/SCRUM-9/scrum-9-ci.yml` | Created | Adds story-scoped CI validation for SCRUM-9 |
| `src/SCRUM_9/requirements.txt` | Created | Declares runtime dependencies for the SCRUM-9 API |
| `src/SCRUM_9/requirements-dev.txt` | Created | Declares development and test dependencies |
| `docs/SCRUM-9/README.md` | Created | Provides user-facing endpoint and usage documentation |

### Branch Scope Note

`git diff main..feature/scrum-9 --name-status` also includes earlier SDLC/bootstrap and SCRUM-8 files relative to `main`. Reviewers should evaluate this PR with that branch scope in mind.

## 3. Test Evidence

### Verification Summary

- Verified by: `sdlc-verify-agent`
- Date: `2026-06-24`
- Branch: `feature/scrum-9`
- Overall status: `✅ Verified`
- Result: `27 passed / 0 failed / 0 skipped`
- Warning: `1 cosmetic Starlette deprecation warning`

### Full Test Output

```text
tests/SCRUM_9/test_expenses_api.py::test_post_expenses_returns_201_and_persists         PASSED
tests/SCRUM_9/test_expenses_api.py::test_get_expenses_returns_all_created_records        PASSED
tests/SCRUM_9/test_expenses_api.py::test_get_expenses_filters_by_category               PASSED
tests/SCRUM_9/test_isolation.py::test_client_factory_creates_isolated_storage_files     PASSED
tests/SCRUM_9/test_isolation.py::test_repeated_client_fixture_usage_starts_from_empty_state PASSED
tests/SCRUM_9/test_service_summary.py::test_summary_uses_decimal_safe_aggregation       PASSED
tests/SCRUM_9/test_service_summary.py::test_list_expenses_applies_exact_category_filter PASSED
tests/SCRUM_9/test_service_summary.py::test_concurrent_add_expense_calls_do_not_lose_items PASSED
tests/SCRUM_9/test_summary_and_errors.py::test_get_category_summary_returns_decimal_safe_totals PASSED
tests/SCRUM_9/test_summary_and_errors.py::test_post_expenses_invalid_payload_returns_400 PASSED
tests/SCRUM_9/test_summary_and_errors.py::test_corrupted_json_returns_sanitized_500     PASSED
tests/SCRUM_9/test_summary_and_errors.py::test_write_failure_returns_sanitized_500      PASSED
tests/SCRUM_9/test_summary_and_errors.py::test_missing_storage_file_auto_initializes_and_persists PASSED
tests/SCRUM_9/test_validation.py::test_expense_create_accepts_valid_payload              PASSED
tests/SCRUM_9/test_validation.py::test_expense_create_rejects_missing_required_fields[payload0-amount] PASSED
tests/SCRUM_9/test_validation.py::test_expense_create_rejects_missing_required_fields[payload1-category] PASSED
tests/SCRUM_9/test_validation.py::test_expense_create_rejects_missing_required_fields[payload2-date] PASSED
tests/SCRUM_9/test_validation.py::test_expense_create_rejects_non_positive_amount[0]    PASSED
tests/SCRUM_9/test_validation.py::test_expense_create_rejects_non_positive_amount[-1]   PASSED
tests/SCRUM_9/test_validation.py::test_expense_create_rejects_non_positive_amount[-0.0001] PASSED
tests/SCRUM_9/test_validation.py::test_expense_create_rejects_empty_category[]          PASSED
tests/SCRUM_9/test_validation.py::test_expense_create_rejects_empty_category[   ]       PASSED
tests/SCRUM_9/test_validation.py::test_expense_create_rejects_empty_category[\t]        PASSED
tests/SCRUM_9/test_validation.py::test_expense_create_rejects_invalid_date_format[23-06-2026] PASSED
tests/SCRUM_9/test_validation.py::test_expense_create_rejects_invalid_date_format[2026/06/23] PASSED
tests/SCRUM_9/test_validation.py::test_expense_create_rejects_invalid_date_format[2026-6-3]  PASSED
tests/SCRUM_9/test_validation.py::test_expense_create_rejects_invalid_date_format[2026-02-30] PASSED

27 passed, 1 warning in 0.20s
```

### FR Coverage

| FR ID | Requirement | Covering Tests | Status |
|-------|-------------|----------------|--------|
| FR-1 | Add Expense | `test_post_expenses_returns_201_and_persists`, `test_expense_create_accepts_valid_payload`, validation rejection tests | ✅ Covered |
| FR-2 | List All Expenses | `test_get_expenses_returns_all_created_records` | ✅ Covered |
| FR-3 | Filter by Category | `test_get_expenses_filters_by_category`, `test_list_expenses_applies_exact_category_filter` | ✅ Covered |
| FR-4 | Category Summary | `test_get_category_summary_returns_decimal_safe_totals`, `test_summary_uses_decimal_safe_aggregation` | ✅ Covered |
| FR-5 | Data Persistence | `test_post_expenses_returns_201_and_persists`, `test_missing_storage_file_auto_initializes_and_persists` | ✅ Covered |

### NFR Coverage

| NFR ID | Requirement | How Verified | Status |
|--------|-------------|--------------|--------|
| NFR-1 | No Authentication | All endpoints are exercised without auth headers | ✅ Verified |
| NFR-2 | JSON Storage | JSON persistence is asserted directly in API tests | ✅ Verified |
| NFR-3 | Validation | Invalid payloads consistently return 400 in API and model tests | ✅ Verified |
| NFR-4 | Minimal Fields | Response assertions validate `id`, `amount`, `category`, and `date` only | ✅ Verified |

## 4. Known Limitations

- No authentication or multi-user isolation is implemented for this MVP.
- Database integration is out of scope; persistence is a single JSON file only.
- Expense update and delete endpoints are not included.
- Date-range filtering is not included.
- Advanced analytics/reporting and a frontend UI are out of scope.
- The verification run reported one cosmetic Starlette deprecation warning with no behavioral impact.

## 5. Reviewer Checklist

- Requirements for FR-1 through FR-5 are implemented.
- All SCRUM-9 tests pass.
- No hardcoded secrets or credentials are introduced.
- The implementation follows the approved architecture and design-review decisions.
- Code review findings were addressed before approval.
- Validation, persistence fault handling, and decimal-safe summary behavior are covered by tests.
- Verify the broader branch diff against `main`, since it includes SDLC/bootstrap and SCRUM-8 files in addition to SCRUM-9.
- Changelog entry is present and consistent with the implementation.