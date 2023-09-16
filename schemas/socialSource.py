def socialSourceDto(data) -> dict:
    return {
        "uuid": data["uuid"],
        "name": data["name"],
        "youtube": data["youtube"],
        "linkedin": data["linkedin"],
        "instagram": data["instagram"],
        "facebook": data["facebook"],
        "twitter": data["twitter"],
        "tiktok": data["tiktok"],
        "web": data["web"],
        "rss": data["rss"],
        "email": data["email"],
        "active": data["active"]
    }


def socialSourcesDto(data) -> list:
    return [socialSourceDto(ss) for ss in data]


def socialPlatfformDto(data) -> dict:
    return {
        "uuid": data["uuid"],
        "username": data["username"],
    }


def youtubeVideoDto(data) -> dict:
    return {
        "uuid": data["uuid"],
        "url": data["url"],
        "platformId": data["platformId"],
        "title": data["title"],
        "thumbnail": data["thumbnail"],
        "stats": data['stats']
    }


def youtubeVideosDto(data) -> list:
    return [youtubeVideoDto(v) for v in data]


def YoutubeVideoStatisticDto(data) -> dict:
    return {
        "description": data["description"],
        "views": data["views"],
        "date": data["date"],
        "comments": data["comments"],
        "likes": data["likes"],
        "timestamp": data["timestamp"],
    }


def YoutubeVideoStatisticsDto(data) -> list:
    return [YoutubeVideoStatisticsDto(v) for v in data]


def YoutubeStatisticsDto(data) -> dict:
    return {
        "channelName": data["channelName"],
        "subs": data["subs"],
        "videos": data["videos"],
        "visualizations": data["visualizations"],
        "startAt": data["startAt"],
        "timestamp": data["timestamp"],
    }
