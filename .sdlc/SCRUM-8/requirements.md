# Requirements: SCRUM-8 — Add and View Personal To-Do Items via a REST API

## Original User Story
> As a **user**, I want to create and view my to-do items through a REST API, so that I can manage my daily tasks programmatically from any client.

---

## Functional Requirements

| ID | Requirement |
|----|-------------|
| FR-1 | The API must expose a `POST /todos` endpoint that accepts a JSON body with a `title` (required) and `description` (optional). |
| FR-2 | `POST /todos` must return the created to-do item with an auto-generated timestamp-based `id` (milliseconds since epoch) and a `201 Created` status. |
| FR-3 | The API must expose a `GET /todos` endpoint that returns all to-do items as a JSON array with `200 OK`. |
| FR-4 | `GET /todos` must return `204 No Content` when no items exist. |
| FR-5 | The API must expose a `GET /todos/:id` endpoint that returns a single to-do item by its `id` with `200 OK`. |
| FR-6 | `GET /todos/:id` must return `404 Not Found` if no item with the given `id` exists. |
| FR-7 | Each to-do item must contain the fields: `id`, `title`, `description`, `done` (boolean, default `false`), `createdAt` (ISO timestamp). |
| FR-8 | `POST /todos` must return `400 Bad Request` with a descriptive error message if `title` is missing or empty. |
| FR-9 | All API responses must use `Content-Type: application/json`. |
| FR-10 | To-do items must be persisted to a local JSON file on disk so data survives server restarts. |

---

## Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NFR-1 | The API must be built using **Python with FastAPI**. |
| NFR-2 | The JSON file store must be read at startup and written on every mutation to ensure durability. |
| NFR-3 | The API must respond to all requests within 500ms under normal load. |
| NFR-4 | The codebase must include a `requirements.txt` listing all Python dependencies. |

---

## Out of Scope

- User authentication and authorization (all to-dos are in a single shared list).
- Update (`PUT`/`PATCH`) and delete (`DELETE`) endpoints.
- Pagination or filtering of the `GET /todos` list.
- A database backend (PostgreSQL, MongoDB, SQLite, etc.).
- Deployment / containerization.

---

## Open Questions

- Should `done` be settable at creation time, or only via a future update endpoint?
- Is there a maximum length constraint on `title` or `description`?
- Should the JSON file path be configurable (e.g., via an environment variable)?
