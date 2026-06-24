# Design Review: SCRUM-8 — Add and View Personal To-Do Items via a REST API

**Date:** 2026-06-23
**Reviewer:** Senior Architect (AI)
**Status:** ⚠️ Approved with changes

---

## Executive Summary

The architecture is well-structured and maps cleanly to the technology choices required by the story. However, two correctness issues must be resolved before implementation: a direct contradiction between FR-4 (204 No Content) and FR-9 (all responses JSON), and an unaddressed concurrent write race condition in the JSON file store that could result in data loss under normal FastAPI concurrency.

---

## Risks and Gaps

### GAP-1 — FR-4 vs FR-9 Contradiction (High Impact)
| Field | Detail |
|-------|--------|
| **Category** | Functional Requirements Conflict |
| **Impact** | High — HTTP 204 must not include a response body (RFC 7230 §3.3). FR-9 requires all responses to be `application/json`. These two requirements are mutually exclusive for the empty-list case. Any implementation that follows both will violate one of them. |
| **Resolution** | Change FR-4 and the architecture's API table: `GET /todos` returns `200 OK` with `[]` (empty JSON array) when no items exist. An empty array is the idiomatic REST response for an empty collection and satisfies FR-9 fully. |

---

### GAP-2 — Concurrent Write Race Condition in JSON Store (Medium Impact)
| Field | Detail |
|-------|--------|
| **Category** | Component Design Gap |
| **Impact** | Medium — FastAPI with Uvicorn handles concurrent async requests. If two `POST /todos` requests arrive simultaneously, both can read the same in-memory list before either writes to disk, causing one item to be silently lost. |
| **Resolution** | Add an `asyncio.Lock()` in `json_store.py` that wraps all read-modify-write operations. |

---

### GAP-3 — Timestamp ID Collision Risk (Low Impact)
| Field | Detail |
|-------|--------|
| **Category** | Data Design Gap |
| **Impact** | Low — Two requests within the same millisecond produce identical IDs, breaking the uniqueness guarantee of `GET /todos/:id`. |
| **Resolution** | In `json_store.py`'s `add()` method, after generating the timestamp ID, check if it already exists in the in-memory list; if so, increment by 1 until unique. |

---

### GAP-4 — Error Response Schema Not Defined (Low Impact)
| Field | Detail |
|-------|--------|
| **Category** | API Design Gap |
| **Impact** | Low — FR-8 requires a "clear error message" on `400`, and FR-6 implies a `404` with a body. Without a defined schema, implementations may return inconsistent formats across endpoints. |
| **Resolution** | Adopt FastAPI's default error shape: `{"detail": "<message>"}`. Document this as the standard error response schema in the API Design section. |

---

### GAP-5 — `done` Field Writability Unresolved (Low Impact)
| Field | Detail |
|-------|--------|
| **Category** | Functional Requirements Traceability |
| **Impact** | Low — The open question "Should `done` be settable at creation time?" is not resolved in the architecture. The architecture notes it is "always false at creation" but does not state where this is enforced. |
| **Resolution** | `done` is excluded from `TodoCreate` (the request body model) and is hardcoded to `False` in the store's `add()` method. Stated explicitly in the Pydantic Models component description. |

---

## Agreed Design Decisions

| Decision | Rationale |
|----------|-----------|
| FastAPI + Uvicorn as runtime | Mandated by NFR-1; provides automatic OpenAPI docs and Pydantic validation out of the box. |
| Pydantic v2 for validation | Handles FR-8 (400 on empty title) and FR-9 (JSON serialisation) automatically. |
| JSON file as persistence layer | Mandated by requirements; no infrastructure dependencies for this MVP. |
| Timestamp-based IDs (ms epoch) with collision guard | Agreed during requirements elicitation; uniqueness enforced by incrementing on collision. |
| No authentication layer | Explicitly out of scope; API must be restricted to localhost/intranet. |
| `done=False` enforced at model level | `TodoCreate` excludes `done`; store hardcodes `False`. Out-of-scope for this story. |
| `GET /todos` empty list → `200 OK` with `[]` | Resolves FR-4/FR-9 conflict; idiomatic REST for empty collections. |

---

## FR Traceability Matrix

| FR | Architecture Component | Status |
|----|----------------------|--------|
| FR-1 | `routes/todos.py` — POST /todos | ✅ Covered |
| FR-2 | `routes/todos.py` + `json_store.py` — 201 + timestamp ID | ✅ Covered |
| FR-3 | `routes/todos.py` — GET /todos 200 OK | ✅ Covered |
| FR-4 | `routes/todos.py` — empty list returns `200 OK` with `[]` | ⚠️ Changed (see GAP-1) |
| FR-5 | `routes/todos.py` — GET /todos/:id 200 OK | ✅ Covered |
| FR-6 | `routes/todos.py` — 404 on unknown id | ✅ Covered |
| FR-7 | `models/todo.py` — TodoItem schema | ✅ Covered |
| FR-8 | `routes/todos.py` + Pydantic — 400 on empty title | ✅ Covered |
| FR-9 | FastAPI default — Content-Type: application/json | ✅ Covered |
| FR-10 | `store/json_store.py` + `todos.json` | ✅ Covered |

---

## Final Assessment

**⚠️ Approved with changes**

The architecture is solid and well-aligned with requirements. The changes required are targeted and low-risk: one requirement conflict resolved (FR-4/FR-9), one concurrency guard added, one minor ID collision safeguard, and two documentation clarifications. No structural rework is needed.
