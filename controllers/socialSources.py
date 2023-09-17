
import asyncio
from fastapi import APIRouter, status
from fastapi import APIRouter, HTTPException
from services.socialSource import findAll, addSocialSource, findSocialSourceById, updateSocialSource, restore, softDelete, scrapeYoutubeChannel, getYoutubeChannelVideos, scrapeYouTubeVideos, findYoutubeStats, findYoutubeChannelVideos, findYoutubeVideo
from models.socialSource import SocialSource, SocialSourcePost, YoutubeStatistics, YoutubeVideo, YoutubeVideoResponse, YoutubeVideosIds

router = APIRouter(prefix="/socialsource",
                   tags=["socialsource"],
                   responses={404: {"message": "Not found"}})


@router.get("/", response_model=list[SocialSource], status_code=status.HTTP_200_OK)
async def getAll():
    list = await findAll()
    if not list:
        raise HTTPException(
            status_code=404, detail="There is any social source yet")
    return list


@router.post("/", response_model=SocialSourcePost, status_code=status.HTTP_201_CREATED)
async def post(socialsource: SocialSourcePost):
    new_socialsource = await addSocialSource(socialsource)
    return new_socialsource


@router.get("/{id}", response_model=SocialSource, status_code=status.HTTP_200_OK)
async def get(id: str):
    socialsource = await findSocialSourceById(id)
    if not socialsource:
        raise HTTPException(status_code=404, detail="SocialSource not found")
    return socialsource


@router.put("/{id}", response_model=SocialSource, status_code=status.HTTP_200_OK)
async def update(id: str, socialsource: SocialSourcePost):
    updated = await updateSocialSource(id, socialsource)
    return updated


@router.put("/{id}/delete", response_model=SocialSource, status_code=status.HTTP_200_OK)
async def update(id: str):
    updated = await softDelete(id)
    return updated


@router.put("/{id}/restore", response_model=SocialSourcePost, status_code=status.HTTP_200_OK)
async def update(id: str):
    updated = await restore(id)
    return updated


@router.post("/scrapper/youtube/{id}", response_model=str, status_code=status.HTTP_200_OK)
async def scrapeYoutube(id: str):
    asyncio.create_task(scrapeYoutubeChannel(id))
    return 'scrapping...'


@router.post("/scrapper/youtube/{id}/channel", response_model=str, status_code=status.HTTP_200_OK)
async def getYoutubeVideos(id: str):
    asyncio.create_task(getYoutubeChannelVideos(id))
    return 'scrapping...'


@router.post("/scrapper/youtube/{id}/videos", response_model=str, status_code=status.HTTP_200_OK)
async def getYoutubeVideos(id: str, ids: YoutubeVideosIds):
    if not ids:
        asyncio.create_task(getYoutubeChannelVideos(id))

    asyncio.create_task(scrapeYouTubeVideos(ids.ids))
    return 'scrapping...'


@router.get("/youtube/{platformId}", response_model=YoutubeStatistics, status_code=status.HTTP_200_OK)
async def get(platformId: str):
    stats = await findYoutubeStats(platformId)
    if not stats:
        raise HTTPException(
            status_code=404, detail="YouTube Channel not found")
    return stats


@router.get("/youtube/{platformId}/videos", response_model=list[YoutubeVideoResponse], status_code=status.HTTP_200_OK)
async def get(platformId: str):
    videos = await findYoutubeChannelVideos(platformId)
    if not videos:
        raise HTTPException(status_code=404, detail="Videos not found")
    return videos


@router.get("/youtube/{platformId}/video/{id}", response_model=YoutubeVideoResponse, status_code=status.HTTP_200_OK)
async def get(platformId: str, id: str):
    video = await findYoutubeVideo(platformId, id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video
