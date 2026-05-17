import sqlite3 #database
import secrets #generating short urls

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import uvicorn #ASGI - asynchronous server gateway interface

app = FastAPI() #function

DB = "shotme.db"
# --- Pydantic models ---

class URLInput(BaseModel): # url input from the user
    long_url: str #input should always be string


class URLUpdate(BaseModel):
    long_url: str


# --- Database setup ---

def init_db():
    conn = sqlite3.connect(DB) #connect to the db created.
    cursor = conn.cursor() #execute sql commands
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

@app.post("/shorten") #post request
def shorten_url(url:URLInput): #taking the url from the user via URLInput
    code = secrets.token_urlsafe(6)
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO urls (long_url, code) VALUES (?, ?)", (url.long_url, code))
    conn.commit()
    conn.close()

    return {"shorturl" : code} #returning the short url

@app.get("/{code}")
def redirect_url(code: str):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT long_url FROM urls WHERE code = ?", (code,))

    result = cursor.fetchone()
    conn.close()

    if result is None:
        raise HTTPException(status_code = 404, detail = "code not found" )
    
    return RedirectResponse(url = result[0])
    pass


@app.put("/url/{code}")
def update_url(code: str, url: URLUpdate):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM urls WHERE code = ?", (code ,))
    result = cursor.fetchone()

    if result is None:
        raise HTTPException(status_code = 404, detail = "Code not found")

    cursor.execute("UPDATE urls SET long_url = ? WHERE code = ? ",
    (url.long_url,code))

    conn.commit()
    conn.close()

    return{"message": "url updated successfully", "code": code, "new_url": url.long_url}


@app.delete("/url/{code}")
def delete_url(code: str):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM urls WHERE code = ?", (code,))
    result = cursor.fetchone()

    if result is None:
        raise HTTPException(status_code = 404, detail = "code not found")

    cursor.execute("DELETE FROM urls WHERE code = ?", (code,))
    conn.commit()
    conn.close()

    return {"message" : "deleted successfully", "code" : code}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)