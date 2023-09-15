
import asyncio
from fastapi import APIRouter, status
from fastapi import APIRouter, HTTPException
from services.socialSource import findAll, addSocialSource, findSocialSourceById, updateSocialSource, restore, softDelete, scrapeYoutubeChannel, getYoutubeChannelVideos, scrapeYouTubeVideos
from models.socialSource import SocialSource, SocialSourcePost, YoutubeStatistics

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


@router.get("/scrapper/youtube/{id}", response_model=str, status_code=status.HTTP_200_OK)
async def get(id: str):
    asyncio.create_task(scrapeYoutubeChannel(id))
    return 'scrapping...'


@router.get("/scrapper/youtube/videos/{id}", response_model=str, status_code=status.HTTP_200_OK)
async def get(id: str):
    asyncio.create_task(getYoutubeChannelVideos(id))
    return 'scrapping...'
