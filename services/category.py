import uuid
from models.category import Category, CategoryUpdate
from dtos.category import categoriesEntity, categoryEntity
from server.mongoClient import db

collection = db['categories']


async def findAllCategories():
    return categoriesEntity(collection.find())


async def addCategory(category: Category):
    new_category = dict(category)
    new_category['uuid'] = str(uuid.uuid4())
    new_category['active'] = True
    collection.insert_one(new_category)
    created = collection.find_one({"uuid": new_category['uuid']})
    return categoryEntity(created)


async def findCategoryById(id: str):
    return categoryEntity(collection.find_one({'uuid': id}))


async def updateCategory(id: str, category: CategoryUpdate):
    update_data = dict(category)
    collection.find_one_and_update({'uuid': id}, {"$set": update_data})
    updated = collection.find_one({"uuid": id})
    return categoryEntity(updated)


async def restoreCategory(id: str):
    collection.find_one_and_update({'uuid': id}, {"$set": {'active': True}})
    updated = collection.find_one({"uuid": id})
    return categoryEntity(updated)


async def softDeleteCategory(id: str):
    collection.find_one_and_update({'uuid': id}, {"$set": {'active': False}})
    updated = collection.find_one({"uuid": id})
    return categoryEntity(updated)
