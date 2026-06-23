# Design Review: SCRUM-9

## Executive Summary

The proposed architecture for SCRUM-9 is a solid MVP design for a file-backed expense tracking API and aligns with the stated story scope. Review identified a few moderate-risk gaps around explicit requirement traceability, persistence error handling, and monetary precision policy. These have now been incorporated into architecture documentation, and the design is suitable to proceed with implementation.

## Risks and Gaps Found

| Category | Gap / Risk | Impact | Resolution |
|---|---|---|---|
| Functional Traceability | FR-to-component coverage was implicit, not explicitly documented. | Moderate: implementation may drift from requirements without a direct coverage map. | Added a dedicated Functional Requirements Traceability matrix mapping FR-1..FR-5 to architecture components. |
| Error Handling Completeness | Missing explicit behavior for missing storage file, corrupted JSON, and write failures. | High: inconsistent runtime behavior or unclear client contract under fault conditions. | Added an Error Handling Strategy section defining 400/500 behavior, initialization semantics, and sanitized server errors. |
| Data Integrity / Numeric Precision | Monetary arithmetic precision policy was not explicit. | Moderate: floating-point drift can produce incorrect category totals. | Added decimal-safe amount handling guidance in service/performance sections. |
| Validation Specificity | Validation listed required fields but did not define domain constraints and date format contract. | Moderate: inconsistent validation across handlers and tests. | Added explicit constraints: positive amount, non-empty category, ISO date format. |

## Agreed Design Decisions

- Preserve lightweight MVP architecture using FastAPI + JSON file storage.
- Keep endpoints public (no authentication) per NFR-1 and out-of-scope constraints.
- Maintain a service layer between routes and storage for clean separation and testability.
- Require explicit validation and deterministic error mapping for all request and persistence failure paths.
- Use decimal-safe arithmetic for amount aggregation correctness.

## Required Changes to architecture.md

All required changes were applied:

- Added Functional Requirements Traceability section with FR-1 to FR-5 mapping.
- Expanded validation responsibilities with positive amount, non-empty category, and ISO date format.
- Added explicit Error Handling Strategy section.
- Added decimal-safe arithmetic guidance under service/performance considerations.

## Final Assessment

**Approved with changes ⚠️**

The design is now approved for implementation, contingent on implementation and tests honoring the documented validation, error handling, and numeric precision policies.
