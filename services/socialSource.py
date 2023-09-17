import uuid
import asyncio
import time

from pymongo import DESCENDING
from models.socialSource import SocialSourcePost
from schemas.socialSource import YoutubeVideoStatisticsDto, socialSourceDto, socialSourcesDto, youtubeVideosDto
from server.mongoClient import db
from .youtubeScraper import YouTubeScrapper
collection = db['socialsources']
youtubeCollection = db['youtubestatistics']
youtubeVideoCollection = db['youtubevideos']
youtubeVideoStatistics = db['youtubevideostatistics']


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


async def scrapeYoutubeChannel(id: str):
    socialSource = collection.find_one({'uuid': id})
    if not socialSource:
        raise ValueError("Social source not found")

    scraper = YouTubeScrapper(socialSource["youtube"]["username"])
    statistics = await scraper.getChannelData()
    statistics["platformId"] = socialSource["youtube"]["uuid"]
    youtubeCollection.insert_one(statistics)

    videos = await getYoutubeChannelVideos(id)
    ids = [item['uuid'] for item in videos]
    statistisc = await scrapeYouTubeVideos(ids)

    return


async def getYoutubeChannelVideos(id: str):
    socialSource = collection.find_one({'uuid': id})
    if not socialSource:
        raise ValueError("Social source not found")
    scraper = YouTubeScrapper(socialSource["youtube"]["username"])
    videos = await scraper.getChannelVideos()
    for video in videos:
        video["uuid"] = str(uuid.uuid4())
        video["platformId"] = socialSource["youtube"]["uuid"]

    youtubeVideoCollection.insert_many(videos)
    inserted = youtubeVideoCollection.find(
        {'platformId': socialSource["youtube"]["uuid"]})
    return inserted


async def scrapeYouTubeVideos(ids: list):
    for id in ids:
        video = youtubeVideoCollection.find_one({'uuid': id})
        print(f"Scraping {video}")
        scraper = YouTubeScrapper()
        info = await scraper.getVideoStatistics(video['url'])
        info['videoId'] = video['uuid']
        youtubeVideoStatistics.insert_one(info)
        print(info)
    return


async def findYoutubeStats(platformId: str):
    result = youtubeCollection.find_one({'platformId': platformId})
    return result


async def findYoutubeChannelVideos(platformId: str):
    videos = youtubeVideoCollection.find({'platformId': platformId})
    response = []
    for video in videos:
        lastStat = youtubeVideoStatistics.find_one(
            {'videoId': video['uuid']}, sort=[("timestamp", DESCENDING)])
        try:
            video['stats'] = YoutubeVideoStatisticsDto([lastStat])
        except:
            video['stats'] = []
        response.append(video)
    return youtubeVideosDto(response)


async def findYoutubeVideo(platformId: str, id: str):
    platform = youtubeCollection.find_one({'platformId': platformId})
    if not platform:
        raise ValueError('Platform not found')

    video = youtubeVideoCollection.find_one({'uuid': id})
    stats = youtubeVideoStatistics.find(
        {'videoId': id}, sort=[("timestamp", DESCENDING)])
    video['stats'] = YoutubeVideoStatisticsDto(stats)
    return video
