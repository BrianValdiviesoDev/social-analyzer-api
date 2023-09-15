from pydantic import BaseModel
from typing import Optional
import datetime
from typing_extensions import TypedDict


class YoutubeStatistics(BaseModel):
    platfformId: str
    channelName: str
    subs: float
    videos: float
    visualizations: float
    startAt: str
    timestamp: str


class YoutubeVideoStatistics(BaseModel):
    title: str
    visualizations: str
    published: datetime.date
    comments: float
    likes: float
    timestamp: datetime.datetime


class YoutubeVideo(BaseModel):
    uuid: str
    plattformId: str
    url: str
    title: str
    thumbnail: str


class SocialPlatfform(TypedDict, total=False):
    username: str
    uuid: str


class SocialPlatfformPost(TypedDict, total=False):
    username: Optional[str]


class SocialSource(BaseModel):
    uuid: str
    name: str
    youtube: SocialPlatfform | None
    linkedin: SocialPlatfform | None
    instagram: SocialPlatfform | None
    facebook: SocialPlatfform | None
    twitter: SocialPlatfform | None
    tiktok: SocialPlatfform | None
    web: str | None
    rss: str | None
    email: str | None
    active: bool = True


class SocialSourcePost(BaseModel):
    name: str | None
    youtube: SocialPlatfformPost | None
    linkedin: SocialPlatfformPost | None
    instagram: SocialPlatfformPost | None
    facebook: SocialPlatfformPost | None
    twitter: SocialPlatfformPost | None
    tiktok: SocialPlatfformPost | None
    web: str | None
    rss: str | None
    email: str | None
