import uuid
from sqlmodel import Session, select
from schemas.socialSource import SocialSourceResponse, SocialSourcePost
from models.socialSource import SocialSource
from models.youtube import YoutubeChannel


async def addSocialSource(session: Session, socialsource: SocialSourcePost) -> SocialSourceResponse:
    newChannel = YoutubeChannel(
        username=socialsource.youtube, uuid=str(uuid.uuid4()))
    socialsource.youtube = newChannel.uuid
    newSocialSource = SocialSource(
        **socialsource.dict(), uuid=str(uuid.uuid4()))

    session.add(newChannel)
    session.add(newSocialSource)
    session.commit()
    session.refresh(newSocialSource)
    return newSocialSource


async def findSocialSourceById(session: Session, uuid: str) -> SocialSourceResponse:
    query = select(SocialSource).where(SocialSource.uuid == uuid)
    return session.exec(query).first()


async def findAllSocialSources(session: Session) -> list[SocialSourceResponse]:
    query = select(SocialSource)
    result = session.exec(query).all()
    return result
