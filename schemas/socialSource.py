from pydantic import BaseModel


class SocialSourcePost(BaseModel):
    name: str
    youtube: str | None
    linkedin: str | None
    instagram: str | None
    facebook: str | None
    twitter: str | None
    tiktok: str | None
    web: str | None
    rss: str | None
    email: str | None


class SocialSourceResponse(SocialSourcePost):
    uuid: str
    active: bool
