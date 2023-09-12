from pydantic import BaseModel
from typing import Optional


class Category(BaseModel):
    uuid: str
    name: str
    parent: Optional[str]
    active: bool = True

class CategoryUpdate(BaseModel):
    name: str | None
    parent: str | None