"""API request and response schemas."""

from typing import List

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str
    service: str
    supported_languages: List[str]
    active_tools_count: int
    llm_provider: str


class LanguageInfo(BaseModel):
    code: str
    name: str
    native_name: str
    region: str


class LanguagesResponse(BaseModel):
    languages: List[LanguageInfo]
