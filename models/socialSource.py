from pydantic import BaseModel
from typing import Optional


class SocialSource(BaseModel):
    uuid: str
    name: str
    youtube: Optional[str]
    linkedin: Optional[str]
    instagram: Optional[str]
    facebook: Optional[str]
    twitter: Optional[str]
    tiktok: Optional[str]
    web: Optional[str]
    rss: Optional[str]
    email: Optional[str]
    active: bool = True

class SocialSourceUpdate(BaseModel):
    name: str | None
    youtube: str | None
    linkedin: str | None
    instagram: str | None
    facebook: str | None
    twitter: str | None
    tiktok: str | None
    web: str | None
    rss: str | None
    email: str | None