import secrets

from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from app.database import get_conn
from app.models import URLInput, URLUpdate
from app.schemas import URLResponse, StatsResponse

router = APIRouter()


# IMPORTANT: /stats/{code} is registered before /{code}
# so FastAPI doesn't swallow "stats" as a short code.

@router.post("/shorten", response_model=URLResponse)
def shorten_url(url: URLInput):
    code = secrets.token_urlsafe(6)
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO urls (long_url, code) VALUES (?, ?)",
        (url.long_url, code),
    )
    conn.commit()
    conn.close()
    return {"code": code, "long_url": url.long_url}


@router.get("/stats/{code}", response_model=StatsResponse)
def get_stats(code: str):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM urls WHERE code = ?", (code,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Code not found")
    return {"code": row["code"], "long_url": row["long_url"], "click_count": row["click_count"]}


@router.get("/{code}")
def redirect_url(code: str):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM urls WHERE code = ?", (code,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Code not found")
    cursor.execute("UPDATE urls SET click_count = click_count + 1 WHERE code = ?", (code,))
    conn.commit()
    conn.close()
    return RedirectResponse(url=row["long_url"])


@router.put("/url/{code}", response_model=URLResponse)
def update_url(code: str, url: URLUpdate):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM urls WHERE code = ?", (code,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Code not found")
    cursor.execute("UPDATE urls SET long_url = ? WHERE code = ?", (url.long_url, code))
    conn.commit()
    conn.close()
    return {"code": code, "long_url": url.long_url}


@router.delete("/url/{code}")
def delete_url(code: str):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM urls WHERE code = ?", (code,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Code not found")
    cursor.execute("DELETE FROM urls WHERE code = ?", (code,))
    conn.commit()
    conn.close()
    return {"message": f"Deleted {code}"}
