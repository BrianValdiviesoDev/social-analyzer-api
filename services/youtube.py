import datetime
import uuid
from sqlmodel import Session, select
from pymongo import DESCENDING
from services.youtubeScraper import YouTubeScrapper
from models.youtube import YoutubeChannel, YouTubeStats, YouTubeVideo, YouTubeVideoStats
from schemas.youtube import YoutubeStatsResponse, YoutubeCompleteStatsResponse


async def scrapeYoutubeChannel(session: Session, channelId: str):
    await getYoutubeChannelStats(session, channelId)
    ids = await getYoutubeChannelVideos(session, channelId)
    await scrapeYouTubeVideos(session, ids)
    return


async def getYoutubeChannelStats(session: Session, channelId: str) -> YoutubeStatsResponse:
    query = select(YoutubeChannel).where(YoutubeChannel.uuid == channelId)
    channel = session.exec(query).first()
    if not channel:
        raise ValueError("Channel not found")
    scraper = YouTubeScrapper(channel.username)
    statistics = await scraper.getChannelData()
    newStat = YouTubeStats(
        **statistics.dict(), youtube_channel=channelId)
    session.add(newStat)
    session.commit()
    session.refresh(newStat)
    return newStat


async def getYoutubeChannelVideos(session: Session, channelId: str) -> list:
    query = select(YoutubeChannel).where(YoutubeChannel.uuid == channelId)
    channel = session.exec(query).first()
    if not channel:
        raise ValueError("Channel not found")
    scraper = YouTubeScrapper(channel.username)
    videos = await scraper.getChannelVideos()
    insertedIds = []

    for video in videos:
        exists = session.exec(select(YouTubeVideo).where(
            YouTubeVideo.url == video.url)).first()

        if not exists:
            insert = YouTubeVideo(
                **video.dict(), youtube_channel=channelId, uuid=str(uuid.uuid4()))
            session.add(insert)
            session.commit()
            session.refresh(insert)
            insertedIds.append(insert.uuid)

        else:
            exists.title = video.title
            exists.thumbnail = video.thumbnail
            exists.youtube_channel = channelId
            exists.description = video.description
            insertedIds.append(exists.uuid)

    return insertedIds


async def scrapeYouTubeVideos(session: Session, ids: list[str]):
    for id in ids:
        video = session.exec(select(YouTubeVideo).where(
            YouTubeVideo.uuid == id)).first()
        scraper = YouTubeScrapper()
        info = await scraper.getVideoStatistics(video.url)

        newStat = YouTubeVideoStats(
            **info.dict(), video=id, uuid=str(uuid.uuid4()))
        session.add(newStat)
        session.commit()
        session.refresh(newStat)


async def findYoutubeChannel(session: Session, channelId: str) -> YoutubeCompleteStatsResponse:
    stats = session.exec(select(YouTubeStats).where(
        YouTubeStats.youtube_channel == channelId)).all()
    videos = session.exec(select(YouTubeVideo).where(
        YouTubeVideo.youtube_channel == channelId)).all()
    return YoutubeCompleteStatsResponse(uuid=channelId, stats=stats, videos=videos)
