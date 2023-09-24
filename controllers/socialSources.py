
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from server.postgres import get_session
from services.socialSource import addSocialSource, findAllSocialSources, findSocialSourceById
from models.socialSource import SocialSource
from schemas.socialSource import SocialSource, SocialSourceBase
router = APIRouter(prefix="/socialsource",
                   tags=["socialsource"],
                   responses={404: {"message": "Not found"}})


@router.post("/",  response_model=SocialSource, status_code=status.HTTP_201_CREATED)
async def post(socialsource: SocialSourceBase, session: Session = Depends(get_session)):
    new_socialsource = await addSocialSource(session, socialsource)
    return new_socialsource


@router.get("/", response_model=list[SocialSource], status_code=status.HTTP_200_OK)
async def get(session: Session = Depends(get_session)):
    ss = await findAllSocialSources(session)
    if not ss:
        raise HTTPException(status_code=404, detail="Resource not found")
    return ss


@router.get("/{uuid}",  response_model=SocialSource, status_code=status.HTTP_200_OK)
async def get(uuid: str, session: Session = Depends(get_session)):
    ss = await findSocialSourceById(session, uuid)
    if not ss:
        raise HTTPException(status_code=404, detail="Resource not found")
    return ss
