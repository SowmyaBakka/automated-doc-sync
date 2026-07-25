# Implementation Plan: SCRUM-10

## Scope and Approach

Implement a minimal authentication slice with `POST /register` and `POST /login` using FastAPI, a service layer, and an in-memory repository. Keep implementation strictly story-scoped under `src/SCRUM_10/` and `tests/SCRUM_10/`.

## Module and File Breakdown

### Source files (`src/SCRUM_10/`)

- `src/SCRUM_10/__init__.py`: package marker.
- `src/SCRUM_10/main.py`: FastAPI app wiring and router registration.
- `src/SCRUM_10/errors.py`: domain/API exception types and deterministic error mapping helpers.
- `src/SCRUM_10/models/__init__.py`: package marker.
- `src/SCRUM_10/models/user.py`: user entity (`id`, `username`, normalized `email`, `password_hash`, `created_at`).
- `src/SCRUM_10/schemas/__init__.py`: package marker.
- `src/SCRUM_10/schemas/auth.py`: request/response/error Pydantic models and field constraints.
- `src/SCRUM_10/store/__init__.py`: package marker.
- `src/SCRUM_10/store/in_memory_user_repo.py`: in-memory repository contract implementation (`create_user`, `get_by_email`, `exists_by_email`, `clear`).
- `src/SCRUM_10/security/__init__.py`: package marker.
- `src/SCRUM_10/security/password_hasher.py`: bcrypt-backed hash/verify abstraction.
- `src/SCRUM_10/security/token_provider.py`: mock token provider interface and implementation.
- `src/SCRUM_10/services/__init__.py`: package marker.
- `src/SCRUM_10/services/auth_service.py`: registration/login orchestration and business rules.
- `src/SCRUM_10/routes/__init__.py`: package marker.
- `src/SCRUM_10/routes/auth.py`: `/register` and `/login` route handlers and response translation.
- `src/SCRUM_10/requirements.txt`: runtime dependencies.
- `src/SCRUM_10/requirements-dev.txt`: test/dev dependencies.
- `src/SCRUM_10/README.md`: story-local run/test notes.

### Test files (`tests/SCRUM_10/`)

- `tests/SCRUM_10/__init__.py`: package marker.
- `tests/SCRUM_10/conftest.py`: shared fixtures (app client, repository reset, service doubles if needed).
- `tests/SCRUM_10/test_register_api.py`: endpoint tests for register path.
- `tests/SCRUM_10/test_login_api.py`: endpoint tests for login path.
- `tests/SCRUM_10/test_auth_service.py`: service-level business and security behavior.
- `tests/SCRUM_10/test_repository_isolation.py`: in-memory lifecycle/isolation behavior.
- `tests/SCRUM_10/test_error_models.py`: deterministic error envelope tests.

## Dependency-Ordered Task Sequence

### Phase 1: Setup

| Task ID | Title | Description | File paths | Depends on | Blocked | Effort |
|---|---|---|---|---|---|---|
| TASK-01 | Story scaffold and app entrypoint | Create package/test folder structure and wire `main.py` with auth router registration skeleton. | `src/SCRUM_10/__init__.py`, `src/SCRUM_10/main.py`, `src/SCRUM_10/routes/__init__.py`, `tests/SCRUM_10/__init__.py`, `tests/SCRUM_10/conftest.py` | None | No | S |
| TASK-02 | Dependency and local docs setup | Add required runtime/dev dependencies and story-local README commands for run/test. | `src/SCRUM_10/requirements.txt`, `src/SCRUM_10/requirements-dev.txt`, `src/SCRUM_10/README.md` | TASK-01 | No | S |
| TASK-03 | Contract and error model definitions | Define request/response schemas, shared error envelope, and exception primitives for `400/401/409`. | `src/SCRUM_10/schemas/auth.py`, `src/SCRUM_10/errors.py`, `src/SCRUM_10/schemas/__init__.py` | TASK-01 | No | M |

### Phase 2: Core

| Task ID | Title | Description | File paths | Depends on | Blocked | Effort |
|---|---|---|---|---|---|---|
| TASK-04 | Domain entity and repository | Implement user entity and in-memory repository with normalized-email indexing and clear/reset support. | `src/SCRUM_10/models/user.py`, `src/SCRUM_10/models/__init__.py`, `src/SCRUM_10/store/in_memory_user_repo.py`, `src/SCRUM_10/store/__init__.py` | TASK-03 | No | M |
| TASK-05 | Security adapters | Implement password hash/verify adapter and mock token provider abstraction. Ensure no plaintext leak in return values/logging paths. | `src/SCRUM_10/security/password_hasher.py`, `src/SCRUM_10/security/token_provider.py`, `src/SCRUM_10/security/__init__.py` | TASK-03 | No | M |
| TASK-06 | Auth service workflows | Implement register/login orchestration: validation handoff, duplicate check, hash persistence, credential verify, token response. | `src/SCRUM_10/services/auth_service.py`, `src/SCRUM_10/services/__init__.py` | TASK-04, TASK-05 | Yes - cannot start until repo and security adapters are complete | L |
| TASK-07 | API routes and response mapping | Implement `POST /register` and `POST /login`, map service/domain errors to deterministic `400/401/409` JSON responses. | `src/SCRUM_10/routes/auth.py`, `src/SCRUM_10/main.py` | TASK-06 | Yes - depends on service completion | M |

### Phase 3: Testing

| Task ID | Title | Description | File paths | Depends on | Blocked | Effort |
|---|---|---|---|---|---|---|
| TASK-08 | Registration API tests | Add positive/negative register tests including duplicate email and malformed input scenarios. | `tests/SCRUM_10/test_register_api.py`, `tests/SCRUM_10/conftest.py` | TASK-07 | Yes - routes must exist | M |
| TASK-09 | Login API tests | Add login success and invalid credential/malformed request cases with deterministic assertions. | `tests/SCRUM_10/test_login_api.py`, `tests/SCRUM_10/conftest.py` | TASK-07 | Yes - routes must exist | M |
| TASK-10 | Service and security tests | Verify password hash behavior, duplicate checks, and login verification logic at service layer. | `tests/SCRUM_10/test_auth_service.py` | TASK-06 | Yes - service implementation required | M |
| TASK-11 | Isolation and error schema tests | Ensure in-memory reset between tests and stable error envelope format for `400/401/409`. | `tests/SCRUM_10/test_repository_isolation.py`, `tests/SCRUM_10/test_error_models.py` | TASK-07 | Yes - endpoint errors must be implemented | M |

### Phase 4: Release

| Task ID | Title | Description | File paths | Depends on | Blocked | Effort |
|---|---|---|---|---|---|---|
| TASK-12 | Final verification and documentation alignment | Run tests, verify scope boundaries, and update story docs with final behavior and known limitations. | `src/SCRUM_10/README.md`, `.sdlc/SCRUM-10/impl-plan.md` | TASK-08, TASK-09, TASK-10, TASK-11 | Yes - requires all test tasks to pass | S |

## FR/NFR Traceability Matrix

| Requirement | Implementing tasks | Primary files | Validation tests |
|---|---|---|---|
| FR-1 `POST /register` | TASK-07 | `src/SCRUM_10/routes/auth.py` | `tests/SCRUM_10/test_register_api.py` |
| FR-2 `POST /login` | TASK-07 | `src/SCRUM_10/routes/auth.py` | `tests/SCRUM_10/test_login_api.py` |
| FR-3 register inputs | TASK-03, TASK-07 | `src/SCRUM_10/schemas/auth.py` | `tests/SCRUM_10/test_register_api.py` |
| FR-4 duplicate email `409` | TASK-04, TASK-06, TASK-07 | `src/SCRUM_10/store/in_memory_user_repo.py`, `src/SCRUM_10/services/auth_service.py` | `tests/SCRUM_10/test_register_api.py`, `tests/SCRUM_10/test_auth_service.py` |
| FR-5 hashed password only | TASK-05, TASK-06 | `src/SCRUM_10/security/password_hasher.py`, `src/SCRUM_10/services/auth_service.py` | `tests/SCRUM_10/test_auth_service.py` |
| FR-6 login credentials | TASK-03, TASK-07 | `src/SCRUM_10/schemas/auth.py`, `src/SCRUM_10/routes/auth.py` | `tests/SCRUM_10/test_login_api.py` |
| FR-7 token on login success | TASK-05, TASK-06, TASK-07 | `src/SCRUM_10/security/token_provider.py` | `tests/SCRUM_10/test_login_api.py` |
| FR-8 invalid login `401` | TASK-06, TASK-07 | `src/SCRUM_10/services/auth_service.py`, `src/SCRUM_10/routes/auth.py` | `tests/SCRUM_10/test_login_api.py` |
| FR-9 in-memory persistence | TASK-04 | `src/SCRUM_10/store/in_memory_user_repo.py` | `tests/SCRUM_10/test_repository_isolation.py` |
| FR-10 required/non-empty input `400` | TASK-03, TASK-07 | `src/SCRUM_10/schemas/auth.py`, `src/SCRUM_10/errors.py` | `tests/SCRUM_10/test_register_api.py`, `tests/SCRUM_10/test_login_api.py`, `tests/SCRUM_10/test_error_models.py` |
| FR-11 mock token strategy | TASK-05, TASK-06 | `src/SCRUM_10/security/token_provider.py` | `tests/SCRUM_10/test_login_api.py` |
| NFR-1 scope boundary | TASK-12 | `src/SCRUM_10/routes/auth.py` | all tests under `tests/SCRUM_10/` |
| NFR-2 excluded features remain out | TASK-12 | `src/SCRUM_10/README.md` | regression check in final review |
| NFR-3 REST JSON style | TASK-03, TASK-07 | `src/SCRUM_10/schemas/auth.py`, `src/SCRUM_10/routes/auth.py` | API tests |
| NFR-4 deterministic errors | TASK-03, TASK-07, TASK-11 | `src/SCRUM_10/errors.py` | `tests/SCRUM_10/test_error_models.py` |
| NFR-5 no plaintext password exposure | TASK-05, TASK-06, TASK-10 | `src/SCRUM_10/security/password_hasher.py` | `tests/SCRUM_10/test_auth_service.py` |
| NFR-6 no committed secrets | TASK-02, TASK-12 | `src/SCRUM_10/README.md` | release checklist verification |

## Concrete Test Cases

| Test Case ID | Scenario | Expected result |
|---|---|---|
| TC-01 | Register with valid `username/email/password` | `201` with `id`, `username`, `email`, success message; no password fields returned |
| TC-02 | Register with duplicate email (case-insensitive) | `409` with `EMAIL_ALREADY_EXISTS` deterministic envelope |
| TC-03 | Register missing `email` | `400` with `VALIDATION_ERROR` and field details for `email` |
| TC-04 | Register empty password or too-short password | `400` deterministic validation error |
| TC-05 | Login with valid credentials | `200` with non-empty `token` and `token_type=Bearer` |
| TC-06 | Login unknown email | `401` with `INVALID_CREDENTIALS` |
| TC-07 | Login wrong password | `401` with `INVALID_CREDENTIALS` |
| TC-08 | Login malformed body (missing password) | `400` with deterministic error schema |
| TC-09 | Password storage verification after register | persisted value is hash, not plaintext, and verify succeeds |
| TC-10 | Repository reset/isolation between tests | user store does not leak state across tests |
| TC-11 | Error schema consistency snapshot | `400/401/409` payloads match agreed envelope and code mapping |
| TC-12 | No sensitive fields in API responses | password/password_hash never appear in response payloads |

## Risks and Mitigations

| Risk | Impact | Mitigation | Owner task |
|---|---|---|---|
| In-memory data loss on restart | accounts vanish between process lifecycles | Document as accepted scope (FR-9) and keep repo abstraction for future persistence swap | TASK-04, TASK-12 |
| Mock token not production-safe | cannot enforce secure downstream auth | Isolate token provider interface and document JWT migration path | TASK-05, TASK-12 |
| Credential leakage through logs/responses | security and compliance failure | centralize response models and avoid logging sensitive payload fields | TASK-03, TASK-05, TASK-07 |
| Non-deterministic validation behavior | flaky clients/tests | enforce shared error mapper and explicit schema assertions | TASK-03, TASK-11 |

## Definition of Done

- All source implementation for SCRUM-10 is under `src/SCRUM_10/` only.
- All tests for SCRUM-10 are under `tests/SCRUM_10/` only.
- `POST /register` and `POST /login` implemented and manually verified via tests.
- Required error responses (`400`, `401`, `409`) are deterministic and schema-consistent.
- Passwords are hashed before persistence and never exposed in responses/logs.
- Mock token behavior is implemented via token provider abstraction.
- Test suite for SCRUM-10 passes locally (API + service + isolation + error-model checks).
- Story-local documentation reflects runtime behavior, scope boundaries, and known non-goals.

## Execution Notes

- Dependency order is strict: TASK-06 cannot start before TASK-04 and TASK-05; TASK-07 cannot start before TASK-06; testing tasks cannot start before their dependent core tasks.
- Any deviation from story-scoped paths (`src/SCRUM_10/`, `tests/SCRUM_10/`) is considered a plan violation.
