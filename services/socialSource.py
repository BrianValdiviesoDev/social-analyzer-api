import uuid
from sqlmodel import Session, select
from schemas.socialSource import SocialSourceBase
from models.socialSource import SocialSource


async def addSocialSource(session: Session, socialsource: SocialSourceBase):
    newSocialSource = SocialSource(
        **socialsource.dict(), uuid=str(uuid.uuid4()))
    session.add(newSocialSource)
    session.commit()
    session.refresh(newSocialSource)
    return newSocialSource


async def findSocialSourceById(session: Session, uuid: str):
    query = select(SocialSource).where(SocialSource.uuid == uuid)
    return session.exec(query).first()


async def findAllSocialSources(session: Session):
    query = select(SocialSource)
    result = session.exec(query).all()
    return result
