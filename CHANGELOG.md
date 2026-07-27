# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [SCRUM-10] - 2026-07-25

### Added

- Authentication REST API under `src/SCRUM_10/` with two endpoints:
  - `POST /register`
  - `POST /login`
- In-memory user repository with normalized email uniqueness checks
- Password hashing and verification utilities to prevent plaintext storage
- Deterministic error contract for `400`, `401`, and `409` scenarios
- Mock token provider abstraction for login success responses
- SCRUM-10 test suite under `tests/SCRUM_10/` covering API behavior, service rules, error envelope consistency, and repository isolation
- Full SDLC artifact chain for SCRUM-10 under `.sdlc/SCRUM-10/`

### Changed

- Pipeline stage tracking for SCRUM-10 advanced through requirements, architecture, design review, implementation plan, implementation, code review, and verify

### Fixed

- Enforced deterministic validation and credential failure response shape at API boundary
- Ensured password values are never returned in response payloads

### Known Limitations

- Authentication uses temporary mock tokens (no production JWT signing in this story)
- User data persists only in-memory and resets on restart
- Out-of-scope auth features remain unimplemented (profile, reset, email verification, logout, refresh tokens)

---

## [SCRUM-9] - 2026-06-24

### Added

- Expense tracking REST API under `src/SCRUM_9/` with three endpoints:
  - `POST /expenses`
  - `GET /expenses`
  - `GET /expenses/summary/categories`
- Strict request validation for positive amounts, non-empty trimmed categories, exact `YYYY-MM-DD` dates, and JSON-object request bodies
- Decimal-safe expense service layer with category filtering and stable category summary aggregation
- JSON file persistence with first-run empty initialization, corrupted-data detection, explicit read/write fault contracts, async locking, and atomic mutation support
- Centralized FastAPI error mapping for validation failures and sanitized `500` storage errors
- SCRUM-9 test suite with 27 passing tests covering validation, service logic, happy paths, summary behavior, error handling, fixture isolation, and concurrent-write regression coverage
- Story-scoped GitHub Actions workflow in `.github/workflows/SCRUM-9/scrum-9-ci.yml`
- SCRUM-9 usage and release documentation under `src/SCRUM_9/README.md` and `docs/SCRUM-9/README.md`

### Changed

- Category summary responses now return the direct category-to-total mapping defined by the approved architecture
- Verification evidence for SCRUM-9 is recorded under `.sdlc/SCRUM-9/verify.md`

### Fixed

- Bound `POST /expenses` payloads explicitly from the request body after happy-path integration testing exposed missing body binding
- Normalized validation error details with JSON-safe encoding so `400` responses do not fail during serialization
- Hardened test fixtures so each test client re-injects its own store, preventing cross-test contamination
- Eliminated a concurrent create race by introducing store-level locking and atomic mutation flow

### Known Limitations

- **No Authentication:** Public MVP API by design
- **No Update/Delete:** Create and read only
- **No Date Range Queries:** Category filtering only
- **No Database Backend:** Single JSON file persistence only
- **Test Warning:** One cosmetic Starlette deprecation warning remains in the verification run

---

## [SCRUM-8] - 2026-06-23

### Added

- ✅ REST API for personal to-do items with three endpoints:
  - `POST /todos` — Create new to-do item with title and optional description
  - `GET /todos` — Retrieve all to-do items (returns 204 No Content when empty per FR-4)
  - `GET /todos/{id}` — Retrieve single to-do item by ID
- ✅ Auto-generated timestamp-based IDs (milliseconds since epoch) with collision detection
- ✅ Request validation via Pydantic models (non-empty title requirement, optional description)
- ✅ JSON file-based persistence with async write-on-mutation durability (todos.json)
- ✅ Thread-safe concurrent operations using asyncio.Lock() on all mutations
- ✅ Comprehensive test suite: 17 tests (8 unit + 9 integration)
  - Unit tests for store: empty store, add with correct fields, get_by_id, concurrent adds, persistence, collision handling
  - Integration tests for all endpoints: happy paths, validation errors, 404s, concurrency
- ✅ Complete API documentation in README.md with curl examples
- ✅ Proper HTTP status codes: 201 (create), 200 (retrieve), 204 (empty list), 400 (validation), 404 (not found), 500 (server error)
- ✅ All responses in JSON format (Content-Type: application/json)

### Changed

- Updated .gitignore to exclude runtime data files (todos.json) and Python artifacts

### Fixed

- ✅ FR-4 Compliance: GET /todos now correctly returns 204 No Content when store is empty (per code review)
- ✅ Concurrent write race condition: Added asyncio.Lock() to JsonStore.add() to prevent data loss
- ✅ Timestamp ID collision risk: Implemented auto-increment collision detection in store

### Known Limitations

- **No Authentication:** Single shared to-do list for all clients (design by spec)
- **No Update/Delete:** POST and GET only (out of scope per requirements)
- **No Pagination:** Returns all items in one response
- **No Database Backend:** Uses JSON file only (not production-scale)
- **No Containerization:** Development mode only (localhost)
- **Timestamp Precision:** Millisecond-based IDs; collision handling for edge cases only

---

## [Unreleased]

(No changes yet)
