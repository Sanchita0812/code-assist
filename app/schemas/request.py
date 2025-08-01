# app/schemas/request.py

from pydantic import BaseModel, HttpUrl

class CodeRequest(BaseModel):
    repoUrl: HttpUrl
    prompt: str
