import asyncio
from fastapi import APIRouter, status, HTTPException
from models.youtube import YoutubeStatistics, YoutubeVideoResponse, YoutubeVideosIds

from services.youtube import findYoutubeChannelVideos, findYoutubeStats, findYoutubeVideo, getYoutubeChannelVideos, scrapeYouTubeVideos, scrapeYoutubeChannel


router = APIRouter(prefix="/youtube",
                   tags=["youtube"],
                   responses={404: {"message": "Not found"}})


@router.post("/scrapper/{id}", response_model=str, status_code=status.HTTP_200_OK)
async def scrapeYoutube(id: str):
    asyncio.create_task(scrapeYoutubeChannel(id))
    return 'scrapping...'


@router.post("/scrapper/{id}/videos", response_model=str, status_code=status.HTTP_200_OK)
async def getYoutubeVideos(id: str, ids: YoutubeVideosIds):
    if not ids:
        asyncio.create_task(getYoutubeChannelVideos(id))

    asyncio.create_task(scrapeYouTubeVideos(ids.ids))
    return 'scrapping...'


@router.get("/{platformId}", response_model=YoutubeStatistics, status_code=status.HTTP_200_OK)
async def get(platformId: str):
    stats = await findYoutubeStats(platformId)
    if not stats:
        raise HTTPException(
            status_code=404, detail="YouTube Channel not found")
    return stats


@router.get("/{platformId}/videos", response_model=list[YoutubeVideoResponse], status_code=status.HTTP_200_OK)
async def get(platformId: str):
    videos = await findYoutubeChannelVideos(platformId)
    if not videos:
        raise HTTPException(status_code=404, detail="Videos not found")
    return videos


@router.get("/{platformId}/video/{id}", response_model=YoutubeVideoResponse, status_code=status.HTTP_200_OK)
async def get(platformId: str, id: str):
    video = await findYoutubeVideo(platformId, id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video
