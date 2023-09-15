import uuid
import asyncio
import time
from models.socialSource import SocialSourcePost
from schemas.socialSource import socialSourceEntity, socialSourcesEntity
from server.mongoClient import db
from .youtubeScraper import YouTubeScrapper
collection = db['socialsources']
youtubeCollection = db['youtubestatistics']
youtubeVideoCollection = db['youtubevideos']
youtubeVideoStatistics = db['youtubevideostatistics']


async def findAll():
    return socialSourcesEntity(collection.find())


async def addSocialSource(socialsource: SocialSourcePost):

    new_socialsource = dict(socialsource)
    new_socialsource['uuid'] = str(uuid.uuid4())
    new_socialsource['active'] = True

    if 'youtube' in new_socialsource:
        platfform = dict(new_socialsource["youtube"])
        platfform['uuid'] = str(uuid.uuid4())
        new_socialsource["youtube"] = platfform

    if 'linkedin' in new_socialsource:
        platfform = dict(new_socialsource["linkedin"])
        platfform['uuid'] = str(uuid.uuid4())
        new_socialsource["linkedin"] = platfform

    if 'instagram' in new_socialsource:
        platfform = dict(new_socialsource["instagram"])
        platfform['uuid'] = str(uuid.uuid4())
        new_socialsource["instagram"] = platfform

    if 'facebook' in new_socialsource:
        platfform = dict(new_socialsource["facebook"])
        platfform['uuid'] = str(uuid.uuid4())
        new_socialsource["facebook"] = platfform

    if 'twitter' in new_socialsource:
        platfform = dict(new_socialsource["twitter"])
        platfform['uuid'] = str(uuid.uuid4())
        new_socialsource["twitter"] = platfform

    if 'tiktok' in new_socialsource:
        platfform = dict(new_socialsource["tiktok"])
        platfform['uuid'] = str(uuid.uuid4())
        new_socialsource["tiktok"] = platfform

    collection.insert_one(new_socialsource)
    created = collection.find_one({"uuid": new_socialsource['uuid']})
    return socialSourceEntity(created)


async def findSocialSourceById(id: str):
    return socialSourceEntity(collection.find_one({'uuid': id}))


async def updateSocialSource(id: str, socialsource: SocialSourcePost):
    update_data = dict(socialsource)
    collection.find_one_and_update({'uuid': id}, {"$set": update_data})
    updated = collection.find_one({"uuid": id})
    return socialSourceEntity(updated)


async def restore(id: str):
    collection.find_one_and_update({'uuid': id}, {"$set": {'active': True}})
    updated = collection.find_one({"uuid": id})
    return socialSourceEntity(updated)


async def softDelete(id: str):
    collection.find_one_and_update({'uuid': id}, {"$set": {'active': False}})
    updated = collection.find_one({"uuid": id})
    return socialSourceEntity(updated)


async def scrapeYoutubeChannel(id: str):
    socialSource = collection.find_one({'uuid': id})
    if not socialSource:
        raise ValueError("Social source not found")

    scraper = YouTubeScrapper(socialSource["youtube"]["username"])
    statistics = await scraper.getChannelData()
    statistics["platfformId"] = socialSource["youtube"]["uuid"]
    youtubeCollection.insert_one(statistics)

    videos = await getYoutubeChannelVideos(id)

    statistisc = await scrapeYouTubeVideos(videos)

    return


async def getYoutubeChannelVideos(id: str):
    socialSource = collection.find_one({'uuid': id})
    if not socialSource:
        raise ValueError("Social source not found")
    scraper = YouTubeScrapper(socialSource["youtube"]["username"])
    videos = await scraper.getChannelVideos()
    for video in videos:
        video["uuid"] = str(uuid.uuid4())
        video["platfformId"] = socialSource["youtube"]["uuid"]

    youtubeVideoCollection.insert_many(videos)
    inserted = youtubeVideoCollection.find(
        {'platfformId': socialSource["youtube"]["uuid"]})
    return inserted


async def scrapeYouTubeVideos(videos: list):
    for video in videos:
        print(f"Scraping {video}")
        scraper = YouTubeScrapper()
        info = await scraper.getVideoStatistics(video['url'])
        info['videoId'] = video['uuid']
        youtubeVideoStatistics.insert_one(info)
        print(info)
    return
