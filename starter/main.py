import sqlite3
import secrets

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI()

DB = "shotme.db"


# --- Pydantic models ---

class URLInput(BaseModel):
    long_url: str


class URLUpdate(BaseModel):
    long_url: str


# --- Database setup ---

def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            long_url TEXT NOT NULL,
            code TEXT UNIQUE NOT NULL,
            click_count INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


init_db()


# --- Routes ---

# IMPORTANT: /stats/{code} must be registered BEFORE /{code}
# so FastAPI doesn't treat the word "stats" as a short code.

@app.post("/shorten")
def shorten_url(url: URLInput):
    # Generate a short code, save long_url + code to the database, return the code.
    pass


@app.get("/stats/{code}")
def get_stats(code: str):
    # Look up the code in the database and return its click_count.
    # Return a 404 if the code doesn't exist.
    pass


@app.get("/{code}")
def redirect_url(code: str):
    # Look up the code in the database.
    # If it doesn't exist, return a 404.
    # Increment click_count by 1, then redirect the user to the long_url.
    pass


@app.put("/url/{code}")
def update_url(code: str, url: URLUpdate):
    # Check that the code exists. Return a 404 if it doesn't.
    # Update long_url for that code (leave code and click_count alone).
    pass


@app.delete("/url/{code}")
def delete_url(code: str):
    # Check that the code exists. Return a 404 if it doesn't.
    # Delete the record from the database and return a confirmation message.
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
