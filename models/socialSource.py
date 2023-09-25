
from sqlmodel import Field, SQLModel
from typing import Optional
import uuid


class SocialSource(SQLModel, table=True):
    __tablename__ = "social_sources"

    uuid: str = Field(default=str(uuid.uuid4()), primary_key=True)
    name: str = None
    youtube: Optional[str] = Field(
        default=None, foreign_key="youtube_channels.uuid")
    linkedin: Optional[str] = None
    instagram: Optional[str] = None
    facebook: Optional[str] = None
    twitter: Optional[str] = None
    tiktok: Optional[str] = None
    web: Optional[str] = None
    rss: Optional[str] = None
    email: Optional[str] = None
    active: Optional[bool] = True
