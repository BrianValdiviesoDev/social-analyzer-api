import datetime
from sqlalchemy import Column, String
from sqlmodel import Field, SQLModel
from typing import Optional
import uuid


class YoutubeChannel(SQLModel, table=True):
    __tablename__ = "youtube_channels"

    uuid: str = Field(default=str(uuid.uuid4()), primary_key=True)
    username: str


class YouTubeStats(SQLModel, table=True):
    __tablename__ = "youtube_stats"

    uuid: str = Field(default=str(uuid.uuid4()), primary_key=True)
    timestamp: datetime.datetime = Field(default=datetime.datetime.utcnow)
    subs: float = None
    videos: float = None
    views: float = None
    youtube_channel: str = Field(foreign_key="youtube_channels.uuid")
    startAt: Optional[datetime.date] = None


class YouTubeVideo(SQLModel, table=True):
    __tablename__ = "youtube_videos"

    uuid: str = Field(default=str(uuid.uuid4()), primary_key=True)
    url: str = Field(sa_column=Column("url", String))
    title: str = None
    thumbnail: str = None
    description: str = None
    youtube_channel: str = Field(foreign_key="youtube_channels.uuid")


class YouTubeVideoStats(SQLModel, table=True):
    __tablename__ = "youtube_video_stats"

    uuid: str = Field(default=str(uuid.uuid4()), primary_key=True)
    video: str = Field(foreign_key="youtube_videos.uuid")
    date: datetime.date = None
    views: float = None
    likes: float = None
    comments: float = None
    timestamp: datetime.datetime = Field(default=datetime.datetime.utcnow)
