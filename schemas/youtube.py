from pydantic import BaseModel


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
    views: float | str
    date: str
    comments: float | str
    likes: float | str
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
