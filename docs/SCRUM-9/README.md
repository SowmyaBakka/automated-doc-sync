# SCRUM-9 Documentation

This folder contains release-facing documentation for the SCRUM-9 expense tracking API.

## Delivered Scope

- Add expenses through `POST /expenses`
- Read all expenses through `GET /expenses`
- Filter expenses by category through `GET /expenses?category=...`
- Aggregate totals by category through `GET /expenses/summary/categories`
- Persist expenses in a single JSON file configured by `SCRUM_9_STORAGE_PATH`

## Storage Behavior

- Missing storage file is treated as first run and initializes to an empty collection
- Empty file is treated as an empty collection
- Corrupted JSON is surfaced as a sanitized `500` response
- Write failures are surfaced as a sanitized `500` response

## Request Validation Rules

- `amount` is required and must be strictly positive
- `category` is required, trimmed, and must contain non-whitespace content
- `date` is required and must use exact `YYYY-MM-DD` format
- unknown extra fields are rejected

## Response Shapes

Expense item:

```json
{
	"id": 1,
	"amount": "12.50",
	"category": "groceries",
	"date": "2026-06-24"
}
```

Category summary:

```json
{
	"groceries": "12.50",
	"travel": "8.25"
}
```

## Error Responses

Validation failure:

```json
{
	"detail": [
		{
			"loc": ["amount"],
			"msg": "Value error, amount must be greater than 0",
			"type": "value_error"
		}
	]
}
```

Storage corruption:

```json
{
	"detail": "storage data is corrupted"
}
```

Storage read/write failure:

```json
{
	"detail": "storage operation failed"
}
```

## Story Path Guardrails

- Keep all implementation code under `src/SCRUM_9/`
- Keep all tests under `tests/SCRUM_9/`
- Keep all SCRUM-9 docs under `docs/SCRUM-9/`
- Do not add SCRUM-9 implementation files at repository root
