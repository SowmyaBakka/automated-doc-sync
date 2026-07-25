# SCRUM-10 Auth API

Minimal authentication API that supports registration and login with in-memory user storage.

## Endpoints

- `POST /register`
- `POST /login`

## Run

```powershell
pip install -r src/SCRUM_10/requirements.txt
uvicorn src.SCRUM_10.main:app --reload
```

## Test

```powershell
pip install -r src/SCRUM_10/requirements-dev.txt
pytest tests/SCRUM_10 -q
```

## Notes

- Passwords are stored only as salted hashes.
- Login returns a temporary mock token by design for this story.
- Data is kept in memory and resets on process restart.
