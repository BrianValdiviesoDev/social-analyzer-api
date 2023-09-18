import uuid
from dtos.youtube import YoutubeVideoStatisticsDto, youtubeVideosDto
from server.mongoClient import db
from pymongo import DESCENDING
from services.youtubeScraper import YouTubeScrapper
socialSourceCollenction = db['socialsources']
youtubeStatsCollection = db['youtubestatistics']
youtubeVideoCollection = db['youtubevideos']
youtubeVideoStatistics = db['youtubevideostatistics']

async def scrapeYoutubeChannel(id: str):
    socialSource = socialSourceCollenction.find_one({'uuid': id})
    if not socialSource:
        raise ValueError("Social source not found")

    scraper = YouTubeScrapper(socialSource["youtube"]["username"])
    statistics = await scraper.getChannelData()
    statistics["platformId"] = socialSource["youtube"]["uuid"]
    youtubeStatsCollection.insert_one(statistics)

    videos = await getYoutubeChannelVideos(id)
    ids = [item['uuid'] for item in videos]
    statistisc = await scrapeYouTubeVideos(ids)

    return


async def getYoutubeChannelVideos(id: str):
    socialSource = socialSourceCollenction.find_one({'uuid': id})
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
    return


async def findYoutubeStats(platformId: str):
    result = youtubeStatsCollection.find_one({'platformId': platformId})
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
    platform = youtubeStatsCollection.find_one({'platformId': platformId})
    if not platform:
        raise ValueError('Platform not found')

    video = youtubeVideoCollection.find_one({'uuid': id})
    stats = youtubeVideoStatistics.find(
        {'videoId': id}, sort=[("timestamp", DESCENDING)])
    video['stats'] = YoutubeVideoStatisticsDto(stats)
    return video
