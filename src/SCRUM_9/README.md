# SCRUM-9 Expense Tracker API

This package contains the SCRUM-9 implementation for expense tracking.

## Runtime Configuration

- `SCRUM_9_STORAGE_PATH`: absolute or relative path to the JSON storage file.
  - Default: `expenses.json`

## Start (development)

From repository root:

```bash
uvicorn src.SCRUM_9.main:app --reload
```
