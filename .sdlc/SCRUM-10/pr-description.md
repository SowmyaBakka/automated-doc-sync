# PR Description: SCRUM-10

## 1. Summary
This PR delivers SCRUM-10 by implementing a minimal authentication REST API that supports user registration and login for secure access onboarding. The story fulfills the defined contract for `POST /register` and `POST /login`, including deterministic error behavior and safe password handling. Verification and code review completed with approval, and the story is ready for merge review.

## 2. Changes Made
Branch comparison to `main` includes baseline repository setup and prior story files; the table below scopes to SCRUM-10 story artifacts and implementation.

| File | Change | Reason |
|------|--------|--------|
| `.sdlc/SCRUM-10/requirements.md` | Created | Captures SCRUM-10 story requirements and scope boundaries |
| `.sdlc/SCRUM-10/architecture.md` | Created | Defines auth architecture, contracts, and sequence flows |
| `.sdlc/SCRUM-10/design-review.md` | Created | Records design validation and residual non-blocking risks |
| `.sdlc/SCRUM-10/impl-plan.md` | Created | Provides task sequencing and FR/NFR traceability |
| `.sdlc/SCRUM-10/code-review.md` | Created | Documents approval and minor residual test gaps |
| `.sdlc/SCRUM-10/verify.md` | Created | Stores verification evidence and final test verdict |
| `.sdlc/SCRUM-10/pipeline-state.json` | Updated | Tracks stage progression through verify and PR readiness |
| `src/SCRUM_10/main.py` | Created | FastAPI app wiring and global validation/error handlers |
| `src/SCRUM_10/routes/auth.py` | Created | Implements `POST /register` and `POST /login` endpoint behavior |
| `src/SCRUM_10/services/auth_service.py` | Created | Encapsulates register/login business logic and rules |
| `src/SCRUM_10/store/in_memory_user_repo.py` | Created | In-memory user persistence per story scope |
| `src/SCRUM_10/security/password_hasher.py` | Created | Password hash/verify utility for non-plaintext storage |
| `src/SCRUM_10/security/token_provider.py` | Created | Temporary mock token generation abstraction |
| `src/SCRUM_10/schemas/auth.py` | Created | Request/response validation and schema contracts |
| `src/SCRUM_10/errors.py` | Created | Deterministic API error envelope mapping |
| `src/SCRUM_10/README.md` | Created | Story-local run/test guidance and scope notes |
| `src/SCRUM_10/requirements.txt` | Created | Runtime dependencies for SCRUM-10 service |
| `src/SCRUM_10/requirements-dev.txt` | Created | Test/development dependencies |
| `tests/SCRUM_10/conftest.py` | Created | Shared fixtures and state reset for test isolation |
| `tests/SCRUM_10/test_register_api.py` | Created | Register endpoint success/error contract coverage |
| `tests/SCRUM_10/test_login_api.py` | Created | Login endpoint success/error contract coverage |
| `tests/SCRUM_10/test_auth_service.py` | Created | Service-level hashing and credential checks |
| `tests/SCRUM_10/test_repository_isolation.py` | Created | In-memory reset/isolation behavior checks |
| `tests/SCRUM_10/test_error_models.py` | Created | Shared deterministic error envelope assertions |

## 3. Test Evidence
Verification command:

```text
pytest tests/SCRUM_10 -q
```

Result summary:

```text
16 passed
```

FR coverage:

| FR ID | Requirement | Validation Evidence | Status |
|-------|-------------|---------------------|--------|
| FR-1 | Registration endpoint | `tests/SCRUM_10/test_register_api.py` | Pass |
| FR-2 | Login endpoint | `tests/SCRUM_10/test_login_api.py` | Pass |
| FR-3 | Registration inputs | `tests/SCRUM_10/test_register_api.py` | Pass |
| FR-4 | Duplicate email returns 409 | `tests/SCRUM_10/test_register_api.py` | Pass |
| FR-5 | Password hashed only | `tests/SCRUM_10/test_auth_service.py` | Pass |
| FR-6 | Login credentials accepted | `tests/SCRUM_10/test_login_api.py` | Pass |
| FR-7 | Token on login success | `tests/SCRUM_10/test_login_api.py` | Pass |
| FR-8 | Invalid login returns 401 | `tests/SCRUM_10/test_login_api.py` | Pass |
| FR-9 | In-memory persistence | `tests/SCRUM_10/test_repository_isolation.py` | Pass |
| FR-10 | Missing/non-empty input validation 400 | `tests/SCRUM_10/test_register_api.py`, `tests/SCRUM_10/test_login_api.py` | Pass |
| FR-11 | Mock token strategy | `tests/SCRUM_10/test_login_api.py` | Pass |

NFR coverage:

| NFR ID | Requirement | Validation Evidence | Status |
|--------|-------------|---------------------|--------|
| NFR-1 | Scope boundary (auth only) | Route surface limited to register/login | Pass |
| NFR-2 | Excluded features remain out | No profile/reset/refresh/logout endpoints added | Pass |
| NFR-3 | REST JSON style | FastAPI JSON handlers and schema models | Pass |
| NFR-4 | Deterministic 400/401/409 errors | `tests/SCRUM_10/test_error_models.py` | Pass |
| NFR-5 | No plaintext password exposure | `tests/SCRUM_10/test_auth_service.py` | Pass |
| NFR-6 | No committed secrets | No env secrets introduced in SCRUM-10 files | Pass |

## 4. Known Limitations
- Out of scope by requirements: profile retrieval, password reset, email verification, logout/revocation, refresh tokens, persistent DB/file auth backend, and production-grade JWT signing/key management.
- Token behavior remains intentionally temporary (mock token) for this story scope.
- User persistence is in-memory only and resets on process restart.
- Residual review gaps noted: no explicit endpoint test for malformed non-object body and no explicit login uppercase-email endpoint test.
- Open question remains whether to promote auth to production JWT and durable storage in a follow-up story.

## 5. Reviewer Checklist
- [x] Requirements met for FR-1 through FR-11
- [x] Verification tests pass for SCRUM-10 (`16 passed`)
- [x] No hardcoded secrets or credentials added
- [x] Architecture and implementation plan were followed
- [x] Code review completed and approved
- [x] Branch includes story-scoped source under `src/SCRUM_10/`
- [x] Branch includes story-scoped tests under `tests/SCRUM_10/`
- [x] Changelog entry added for SCRUM-10

Branch: `feature/scrum-10`
Verification commit: `b68d4d3`
