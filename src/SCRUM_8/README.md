# To-Do REST API

A lightweight REST API for managing personal to-do items, built with Python and FastAPI.

## Features

- **Create to-do items** with title and optional description
- **Retrieve all to-do items** as a JSON array
- **Retrieve a single item** by ID
- **Persistent storage** using a local JSON file
- **Auto-generated timestamps** for each item (milliseconds since epoch)
- **Validation** to ensure titles are non-empty

## Installation

1. Clone the repository and navigate to `src/SCRUM_8/`:

```bash
cd src/SCRUM_8/
```

2. Install runtime dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Install development/testing dependencies:

```bash
pip install -r requirements-dev.txt
```

## Running the Server

From the `src/SCRUM_8/` directory, start the development server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000/`

### Interactive API Documentation

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## API Endpoints

### 1. Create a To-Do Item

```bash
curl -X POST "http://127.0.0.1:8000/todos" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
```

**Response (201 Created):**
```json
{
  "id": 1750000000000,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "done": false,
  "createdAt": "2026-06-23T10:00:00Z"
}
```

**Error (400 Bad Request):**
```bash
curl -X POST "http://127.0.0.1:8000/todos" \
  -H "Content-Type: application/json" \
  -d '{"title": "", "description": "Empty title"}'
```

### 2. Get All To-Do Items

```bash
curl -X GET "http://127.0.0.1:8000/todos"
```

**Response (200 OK):**
```json
[
  {
    "id": 1750000000000,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "done": false,
    "createdAt": "2026-06-23T10:00:00Z"
  },
  {
    "id": 1750000000001,
    "title": "Write report",
    "description": null,
    "done": false,
    "createdAt": "2026-06-23T10:01:00Z"
  }
]
```

Empty store returns:
```json
[]
```

### 3. Get a Single To-Do Item by ID

```bash
curl -X GET "http://127.0.0.1:8000/todos/1750000000000"
```

**Response (200 OK):**
```json
{
  "id": 1750000000000,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "done": false,
  "createdAt": "2026-06-23T10:00:00Z"
}
```

**Error (404 Not Found):**
```bash
curl -X GET "http://127.0.0.1:8000/todos/999999999"
```

## Data Persistence

All to-do items are persisted to a local JSON file (`todos.json`) in the `src/SCRUM_8/` directory.

- The file is **read on application startup** to load existing items into memory
- The file is **written after every mutation** (when a new item is created) to ensure durability
- Data survives server restarts

### File Format

`todos.json` is a simple JSON array:

```json
[
  {
    "id": 1750000000000,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "done": false,
    "createdAt": "2026-06-23T10:00:00Z"
  }
]
```

## Development

### Running Tests

From the repository root, run all tests:

```bash
pytest tests/SCRUM_8/ -v
```

Run specific test file:

```bash
pytest tests/SCRUM_8/test_store.py -v
pytest tests/SCRUM_8/test_post_todos.py -v
pytest tests/SCRUM_8/test_get_todos.py -v
pytest tests/SCRUM_8/test_get_todo_by_id.py -v
```

### Test Coverage

- **Unit tests:** JSON store operations (load, add, get_all, get_by_id), concurrency, persistence, collision handling
- **Integration tests:** POST /todos validation, GET /todos list retrieval, GET /todos/{id} single item retrieval

## Architecture

```
src/SCRUM_8/
├── main.py                 # FastAPI app entry point
├── models/
│   ├── __init__.py
│   └── todo.py            # Pydantic models (TodoCreate, TodoItem)
├── routes/
│   ├── __init__.py
│   └── todos.py           # Router with /todos endpoints
├── store/
│   ├── __init__.py
│   └── json_store.py      # JsonStore class for persistence
├── todos.json             # Persistent data file
├── requirements.txt       # Runtime dependencies
└── requirements-dev.txt   # Development dependencies
```

## Limitations & Notes

⚠️ **Important:** This is a **localhost-only MVP**. Do **NOT** expose this API to the public internet.

- No user authentication or authorization — all clients share a single global to-do list
- No update (`PUT`/`PATCH`) or delete (`DELETE`) endpoints (out of scope)
- No pagination or filtering (out of scope)
- No database backend — local JSON file only
- Concurrent writes are protected by an `asyncio.Lock` to prevent data loss

## Future Enhancements

- Add `PUT /todos/{id}` and `DELETE /todos/{id}` endpoints for updates and deletions
- Implement user authentication (OAuth2/JWT)
- Migrate to a database backend (PostgreSQL, MongoDB, SQLite)
- Add pagination and filtering to `GET /todos`
- Support for todo categories or tags
- Environment-based configuration (database URL, port, etc.)

## Requirements

- Python 3.11+
- FastAPI >= 0.111
- Uvicorn[standard] >= 0.29

## License

[Specify your license here]

## Support

For issues or questions, please open an issue in the repository.
