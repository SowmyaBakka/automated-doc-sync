# SCRUM-9 Expense Tracker API

This package contains the story-scoped FastAPI implementation for SCRUM-9.

## Scope Rules

- Story code lives only under `src/SCRUM_9/`
- Story tests live only under `tests/SCRUM_9/`
- Story docs live only under `docs/SCRUM-9/`
- Do not place SCRUM-9 implementation code at repository root

## Runtime Configuration

- `SCRUM_9_STORAGE_PATH`: absolute or relative path to the JSON storage file
  - Default: `expenses.json`

## Start (development)

From repository root:

```bash
uvicorn src.SCRUM_9.main:app --reload
```

## Endpoints

### `POST /expenses`

Create a new expense.

Example request:

```json
{
  "amount": "12.50",
  "category": "groceries",
  "date": "2026-06-24"
}
```

Example `201 Created` response:

```json
{
  "id": 1,
  "amount": "12.50",
  "category": "groceries",
  "date": "2026-06-24"
}
```

### `GET /expenses`

Return all persisted expenses.

Optional query parameter:

- `category`: exact category match after trimming request whitespace

Example `200 OK` response:

```json
[
  {
    "id": 1,
    "amount": "12.50",
    "category": "groceries",
    "date": "2026-06-24"
  }
]
```

### `GET /expenses/summary/categories`

Return Decimal-safe aggregated totals by category.

Example `200 OK` response:

```json
{
  "totals": {
    "groceries": "12.50",
    "travel": "8.25"
  }
}
```

## Validation Contract

Invalid or missing request fields return `400 Bad Request`.

Rules:

- `amount` is required and must be greater than `0`
- `category` is required, trimmed, and must not be empty
- `date` is required and must match `YYYY-MM-DD`
- request body must be a JSON object

## Error Contract

- `400 Bad Request`: invalid payload or framework validation failure
- `500 Internal Server Error`: unexpected server failure
- `500` with `{"detail": "storage data is corrupted"}`: unreadable or invalid JSON store
- `500` with `{"detail": "storage operation failed"}`: storage read/write failure

## Testing

Run SCRUM-9 tests from repository root:

```bash
pytest tests/SCRUM_9 -q
```
