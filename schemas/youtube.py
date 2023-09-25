import datetime
from pydantic import BaseModel
from typing import List


class YoutubeChannelPost(BaseModel):
    username: str


class YoutubeChannelResponse(YoutubeChannelPost):
    uuid: str


class YoutubeStatsPost(BaseModel):
    timestamp: datetime.datetime | None
    subs: float | None
    videos: float | None
    views: float | None
    startAt: datetime.date | None


class YoutubeStatsResponse(YoutubeStatsPost):
    uuid: str
    youtube_channel: str


class YoutubeVideoPost(BaseModel):
    url: str
    title: str | None
    thumbnail: str | None
    description: str | None


class YoutubeVideoResponse(YoutubeVideoPost):
    uuid: str
    youtube_channel: str


class YoutubeVideoStatsPost(BaseModel):
    date: datetime.date | None
    views: float | None
    likes: float | None
    comments: float | None
    timestamp: datetime.datetime


class YoutubeVideoStatsResponse(YoutubeVideoStatsPost):
    uuid: str
    youtube_video: str


class YoutubeCompleteStatsResponse(BaseModel):
    uuid: str
    videos: List[YoutubeVideoResponse] = []
    stats: List[YoutubeStatsResponse] = []
