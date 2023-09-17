from pydantic import BaseModel
from typing import Optional
from typing_extensions import TypedDict


class YoutubeStatistics(BaseModel):
    platformId: str
    channelName: str
    subs: float
    videos: float
    visualizations: float
    startAt: str
    timestamp: str


class YoutubeVideoStatistics(BaseModel):
    description: str
    views: float
    date: str
    comments: float
    likes: float
    timestamp: str
    videoId: str


class YoutubeVideo(BaseModel):
    uuid: str
    platformId: str
    url: str
    title: str
    thumbnail: str


class YoutubeVideoResponse(BaseModel):
    uuid: str
    platformId: str
    url: str
    title: str
    thumbnail: str
    stats: list[YoutubeVideoStatistics]


class YoutubeVideosIds(BaseModel):
    ids: list


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
