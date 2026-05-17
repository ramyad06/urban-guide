from pydantic import BaseModel


class URLResponse(BaseModel):
    code: str
    long_url: str


class StatsResponse(BaseModel):
    code: str
    long_url: str
    click_count: int
