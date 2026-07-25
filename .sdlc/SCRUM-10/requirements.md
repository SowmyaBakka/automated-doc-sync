# Requirements Document: SCRUM-10

## User Story

**As a** new user,  
**I want** to register and log in via a REST API,  
**So that** I can access personalized features securely.

---

## Functional Requirements

| ID | Requirement | Description |
|----|-------------|-------------|
| FR-1 | Registration Endpoint | The API must expose `POST /register` to create a new user account |
| FR-2 | Login Endpoint | The API must expose `POST /login` to authenticate an existing user |
| FR-3 | Registration Inputs | Registration must accept `username`, `email`, and `password` |
| FR-4 | Duplicate Email Handling | Registration must return `409 Conflict` when the email is already registered |
| FR-5 | Password Storage Safety | Passwords must never be stored in plain text; only hashed passwords are persisted |
| FR-6 | Login Credentials | Login must accept `email` and `password` |
| FR-7 | Login Success Response | On valid credentials, login must return an authentication token in the response payload |
| FR-8 | Invalid Login Handling | Login must return `401 Unauthorized` for invalid credentials |
| FR-9 | Persistence Approach | User data is maintained in-memory for this story and is not persisted across restarts |
| FR-10 | Input Validation Baseline | Endpoints must validate that required inputs are present and non-empty, returning `400 Bad Request` for malformed input |
| FR-11 | Token Strategy (Temporary) | Login currently returns a mock token string as a temporary implementation decision |

---

## Non-Functional Requirements

| ID | Requirement | Description |
|----|-------------|-------------|
| NFR-1 | Scope Boundary | In scope: registration and login only |
| NFR-2 | Excluded Features | Out of scope: profile, password reset, email verification, logout, refresh tokens |
| NFR-3 | API Style | REST API with JSON request/response payloads |
| NFR-4 | Error Consistency | Error responses must be deterministic for key scenarios (`400`, `401`, `409`) |
| NFR-5 | Security Minimum | Plain text passwords are prohibited in storage, logs, and responses |
| NFR-6 | Environment Safety | No secrets or credentials are committed as part of this story |

---

## Out of Scope

- Profile retrieval endpoints
- Password reset flows
- Email verification workflows
- Logout and token revocation
- Refresh token support
- Persistent database or file-backed user storage
- Production-grade JWT signing and key management

---

## Open Questions

- Should temporary in-memory storage and mock token behavior be promoted to production-ready authentication (real JWT with secret from environment) in this story, or tracked as a follow-up story?
