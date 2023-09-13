import uuid
from models.socialSource import SocialSource, SocialSourceUpdate
from schemas.socialSource import socialSourceEntity, socialSourcesEntity
from server.mongoClient import db

collection = db['socialsources']
async def findAll():
    return socialSourcesEntity(collection.find())

async def addSocialSource(socialsource: SocialSource):
    new_socialsource = dict(socialsource)
    new_socialsource['uuid'] = str(uuid.uuid4())
    new_socialsource['active'] = True
    collection.insert_one(new_socialsource)
    created = collection.find_one({"uuid": new_socialsource['uuid']})
    return socialSourceEntity(created)

async def findSocialSourceById(id:str):
    return socialSourceEntity(collection.find_one({'uuid': id}))

async def updateSocialSource(id:str, socialsource:SocialSourceUpdate):
    update_data = dict(socialsource)
    collection.find_one_and_update({'uuid': id}, {"$set": update_data})
    updated = collection.find_one({"uuid": id})
    return socialSourceEntity(updated)

async def restore(id:str):
    collection.find_one_and_update({'uuid': id}, {"$set": {'active':True}})
    updated = collection.find_one({"uuid": id})
    return socialSourceEntity(updated)

async def softDelete(id:str):
    collection.find_one_and_update({'uuid': id}, {"$set": {'active':False}})
    updated = collection.find_one({"uuid": id})
    return socialSourceEntity(updated)