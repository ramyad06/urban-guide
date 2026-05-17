from pydantic import BaseModel


class URLInput(BaseModel):
    long_url: str


class URLUpdate(BaseModel):
    long_url: str
