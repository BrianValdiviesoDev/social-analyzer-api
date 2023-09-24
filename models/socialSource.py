
from sqlmodel import Field, SQLModel
from typing import Optional


class SocialSource(SQLModel, table=True):
    __tablename__ = "social_sources"

    uuid: str = Field(default=None, primary_key=True)
    name: str = None
    youtube: Optional[str] = None
    linkedin: Optional[str] = None
    instagram: Optional[str] = None
    facebook: Optional[str] = None
    twitter: Optional[str] = None
    tiktok: Optional[str] = None
    web: Optional[str] = None
    rss: Optional[str] = None
    email: Optional[str] = None
    active: Optional[bool] = True
