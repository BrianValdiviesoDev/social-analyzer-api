import uuid
import asyncio
import time

from pymongo import DESCENDING
from models.socialSource import SocialSourcePost
from dtos.socialSource import socialSourceDto, socialSourcesDto
from server.mongoClient import db
collection = db['socialsources']


async def findAll():
    return socialSourcesDto(collection.find())


async def addSocialSource(socialsource: SocialSourcePost):

    new_socialsource = dict(socialsource)
    new_socialsource['uuid'] = str(uuid.uuid4())
    new_socialsource['active'] = True

    if 'youtube' in new_socialsource:
        platform = dict(new_socialsource["youtube"])
        platform['uuid'] = str(uuid.uuid4())
        new_socialsource["youtube"] = platform

    if 'linkedin' in new_socialsource:
        platform = dict(new_socialsource["linkedin"])
        platform['uuid'] = str(uuid.uuid4())
        new_socialsource["linkedin"] = platform

    if 'instagram' in new_socialsource:
        platform = dict(new_socialsource["instagram"])
        platform['uuid'] = str(uuid.uuid4())
        new_socialsource["instagram"] = platform

    if 'facebook' in new_socialsource:
        platform = dict(new_socialsource["facebook"])
        platform['uuid'] = str(uuid.uuid4())
        new_socialsource["facebook"] = platform

    if 'twitter' in new_socialsource:
        platform = dict(new_socialsource["twitter"])
        platform['uuid'] = str(uuid.uuid4())
        new_socialsource["twitter"] = platform

    if 'tiktok' in new_socialsource:
        platform = dict(new_socialsource["tiktok"])
        platform['uuid'] = str(uuid.uuid4())
        new_socialsource["tiktok"] = platform

    collection.insert_one(new_socialsource)
    created = collection.find_one({"uuid": new_socialsource['uuid']})
    return socialSourceDto(created)


async def findSocialSourceById(id: str):
    return socialSourceDto(collection.find_one({'uuid': id}))


async def updateSocialSource(id: str, socialsource: SocialSourcePost):
    update_data = dict(socialsource)
    collection.find_one_and_update({'uuid': id}, {"$set": update_data})
    updated = collection.find_one({"uuid": id})
    return socialSourceDto(updated)


async def restore(id: str):
    collection.find_one_and_update({'uuid': id}, {"$set": {'active': True}})
    updated = collection.find_one({"uuid": id})
    return socialSourceDto(updated)


async def softDelete(id: str):
    collection.find_one_and_update({'uuid': id}, {"$set": {'active': False}})
    updated = collection.find_one({"uuid": id})
    return socialSourceDto(updated)
