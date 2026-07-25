# Design Review: SCRUM-10

## Executive Summary

The proposed architecture for SCRUM-10 is well-aligned with the story scope and provides complete coverage for registration and login workflows using a clean route-service-repository split. Functional requirements are traceable to explicit components and contracts, with strong baseline security controls for password handling and error semantics. Approval is granted with minor design hardening recommendations that can be handled as follow-up implementation tasks.

## Requirements Traceability (Pass/Fail)

### Functional Requirements

| Requirement | Architecture Coverage | Status |
|---|---|---|
| FR-1 Registration Endpoint (`POST /register`) | Defined in API contracts and Auth Routes responsibilities | PASS |
| FR-2 Login Endpoint (`POST /login`) | Defined in API contracts and Auth Routes responsibilities | PASS |
| FR-3 Registration Inputs (`username`, `email`, `password`) | Request model `RegisterRequest` and validation rules define all fields | PASS |
| FR-4 Duplicate Email Handling (`409`) | `exists_by_email` check + error mapping `EMAIL_ALREADY_EXISTS` | PASS |
| FR-5 Password Storage Safety (hashed only) | Password Hasher + explicit no-plaintext storage/response policy | PASS |
| FR-6 Login Credentials (`email`, `password`) | Request model `LoginRequest` and login validation rules | PASS |
| FR-7 Login Success Response includes token | `LoginResponse` includes `token` and `token_type` | PASS |
| FR-8 Invalid Login Handling (`401`) | Invalid credentials mapped to `401 INVALID_CREDENTIALS` | PASS |
| FR-9 In-memory persistence only | InMemory User Repository and process-memory notes | PASS |
| FR-10 Required, non-empty input validation with `400` | Validation section + deterministic `400 VALIDATION_ERROR` model | PASS |
| FR-11 Temporary mock token strategy | Token provider explicitly returns mock token with upgrade seam | PASS |

### Non-Functional Requirements

| Requirement | Architecture Coverage | Status |
|---|---|---|
| NFR-1 Scope boundary (register/login only) | Goals/scope and out-of-scope sections enforce narrow scope | PASS |
| NFR-2 Excluded features remain out of scope | Explicitly listed under out-of-scope and non-goals | PASS |
| NFR-3 REST + JSON style | API contracts define JSON request/response payloads | PASS |
| NFR-4 Deterministic errors (`400`, `401`, `409`) | Shared error model + stable code mapping | PASS |
| NFR-5 No plaintext passwords in storage/logs/responses | Security and hashing strategy explicitly prohibits plaintext handling | PASS |
| NFR-6 No committed secrets/credentials | Mock token approach avoids real secrets; follow-up env secret plan documented | PASS |

## Risks and Gaps

| Category | Risk/Gap | Impact | Resolution |
|---|---|---|---|
| Security | No brute-force/rate-limit control on login path in current design | Increased risk of credential stuffing attempts in non-dev environments | Add route-level rate limiting and account/IP backoff as a follow-up story before production exposure |
| Security | Temporary mock token is non-verifiable and not revocable | Token cannot support secure authorization in downstream services | Keep current mock token for this story, but create next-story commitment for JWT issuance/verification with env-managed signing keys |
| Reliability | In-memory user state is process-local and volatile | User records are lost on restart and cannot scale across instances | Accepted for FR-9; track migration plan to persistent repository behind existing interface |
| Observability | No explicit structured audit events for auth outcomes | Harder incident analysis and abuse monitoring | Add safe, structured auth event logging (without passwords/password hashes) |

## Agreed Design Decisions

- Keep route -> validation -> service -> repository layering as proposed.
- Keep in-memory repository for this story only, with explicit volatility accepted.
- Keep mock token provider for this story, but preserve provider interface seam for JWT migration.
- Preserve deterministic shared error envelope and status code mapping (`400`, `401`, `409`).
- Enforce password hashing via bcrypt-backed hasher and never expose sensitive credential material.

## Story-Scoped Path and Security Compliance Check

- Story-scoped Python-safe naming (`SCRUM_10`) is correctly used in the implementation-ready plan under `src/` and `tests/`.
- Proposed source paths are compliant with story-scoped placement expectations.
- Security constraints are satisfied at design level:
  - No plaintext password storage.
  - No plaintext password logging/response inclusion.
  - No committed secrets required for current mock-token scope.

## Required Changes to architecture.md

No mandatory architecture changes are required for SCRUM-10 approval.

Optional clarity improvements for a future revision:
- Add a short subsection under Security notes documenting intended rate-limit policy for `/login`.
- Add a short subsection under Token approach listing acceptance criteria for JWT migration story.

## Final Assessment

Approved with changes ⚠️

Rationale: all requirements are covered and the design is implementation-ready for the current scope, with non-blocking hardening actions recommended for production-readiness in follow-up work.
