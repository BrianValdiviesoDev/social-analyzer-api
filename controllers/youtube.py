import asyncio
from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel import Session, select
from server.postgres import get_session
from services.youtube import getYoutubeChannelVideos, scrapeYouTubeVideos, scrapeYoutubeChannel, findYoutubeChannel
from schemas.youtube import YoutubeCompleteStatsResponse
from models.youtube import YouTubeVideo
router = APIRouter(prefix="/youtube",
                   tags=["youtube"],
                   responses={404: {"message": "Not found"}})


@router.post("/scrapper/{channelId}", response_model=str, status_code=status.HTTP_200_OK)
async def scrapeYoutube(channelId: str, session: Session = Depends(get_session)):
    asyncio.create_task(scrapeYoutubeChannel(session, channelId))
    return 'scrapping...'


@router.post("/scrapper/{channelId}/videos", response_model=str, status_code=status.HTTP_200_OK)
async def getYoutubeVideos(channelId: str, ids: list[str], session: Session = Depends(get_session)):
    if not ids:
        ids = session.exec(select(YouTubeVideo.uuid).where(
            YouTubeVideo.youtube_channel == channelId)).all()
    asyncio.create_task(scrapeYouTubeVideos(session, ids))
    return 'scrapping...'


@router.get("/{channelId}", response_model=YoutubeCompleteStatsResponse, status_code=status.HTTP_200_OK)
async def get(channelId: str, session: Session = Depends(get_session)):
    channel = await findYoutubeChannel(session, channelId)
    if not channel:
        raise HTTPException(
            status_code=404, detail="YouTube Channel not found")
    return channel
