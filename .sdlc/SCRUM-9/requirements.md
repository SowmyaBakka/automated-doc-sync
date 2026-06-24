# Requirements Document: SCRUM-9

## User Story

**As a** personal finance user,  
**I want** to log and view my daily expenses via a REST API,  
**So that** I can track where my money is going each month.

---

## Functional Requirements

| ID | Requirement | Description |
|----|-------------|-------------|
| FR-1 | Add Expense | Users can add an expense via POST endpoint with amount, category, and date |
| FR-2 | List All Expenses | Users can retrieve all expenses via GET endpoint |
| FR-3 | Filter by Category | Users can filter expenses by category via query parameter |
| FR-4 | Category Summary | Users can retrieve total spend per category via dedicated endpoint |
| FR-5 | Data Persistence | Expenses persist between sessions in JSON file storage |

---

## Non-Functional Requirements

| ID | Requirement | Description |
|----|-------------|-------------|
| NFR-1 | No Authentication | API endpoints are public; no auth required for MVP |
| NFR-2 | JSON Storage | Data stored in single JSON file (e.g., expenses.json) |
| NFR-3 | Validation | Invalid/missing required fields return 400 Bad Request |
| NFR-4 | Minimal Fields | Each expense contains: id, amount, category, date |

---

## Out of Scope

- User authentication and multi-user isolation
- Database integration (SQL/NoSQL)
- Expense update/delete endpoints
- Date range filtering
- Advanced analytics or reporting
- Frontend UI

---

## Open Questions

None — all clarifications collected.
