# ShotMe — FastAPI URL Shortener Workshop

A hands-on workshop repo for learning FastAPI with a real project. You build a URL shortener called ShotMe.

---

## Folders

### `starter/`

This is where you work. It has one file — `main.py` — with the full structure already in place: imports, Pydantic models, database setup, and five route stubs. Each stub has a comment telling you what to implement. Your job is to fill in the logic.

Run it with:

```
pip install -r requirements.txt
uvicorn main:app --reload
```

### `solution/`

The complete working version. Look at this after you've attempted the starter, or when you get stuck. It's split across multiple files to show what a real project layout looks like:

```
solution/
├── app/
│   ├── main.py        ← creates the app, mounts the router
│   ├── database.py    ← connection and table setup
│   ├── models.py      ← request body shapes
│   ├── schemas.py     ← response shapes
│   └── routes/
│       └── urls.py    ← all five route handlers
├── requirements.txt
└── .gitignore
```

The starter is one file because that's enough to understand FastAPI. The solution is split into modules because that's how you'd structure it if the project kept growing — each file has one clear job and you can find things without reading the whole codebase.

Run it with:

```
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## Routes

| Method | Path | What it does |
|--------|------|--------------|
| POST | `/shorten` | Takes a long URL, returns a short code |
| GET | `/stats/{code}` | Returns click count for a code |
| GET | `/{code}` | Redirects to the original URL |
| PUT | `/url/{code}` | Updates the destination URL for a code |
| DELETE | `/url/{code}` | Removes a code from the database |

---

## Database

Uses SQLite with raw `sqlite3` — no ORM. One table, five columns. The `init_db()` function creates it on startup so you don't have to do anything manually.

---

## Deploying to Render

If you deploy to Render's free tier, note that the SQLite database resets every time the service spins down. This is expected — the free tier uses an ephemeral filesystem. For a persistent database in production you'd switch to Postgres or another hosted database and swap the connection string.
