def socialSourceEntity(data) -> dict:
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


def socialSourcesEntity(data) -> list:
    return [socialSourceEntity(ss) for ss in data]


def socialPlatfform(data) -> dict:
    return {
        "uuid": data["uuid"],
        "username": data["username"],
    }


def youtubeVideo(data) -> dict:
    return {
        "url": data["url"],
        "statistics": data["statistics"],
        "platfformId": data["platfformId"],
        "description": data["description"],
    }


def YoutubeVideoStatistics(data) -> dict:
    return {
        "title": data["title"],
        "visualizations": data["visualizations"],
        "published": data["published"],
        "comments": data["comments"],
        "likes": data["likes"],
        "timestamp": data["timestamp"],
    }


def YoutubeStatistics(data) -> dict:
    return {
        "channelName": data["channelName"],
        "subs": data["subs"],
        "videos": data["videos"],
        "visualizations": data["visualizations"],
        "startAt": data["startAt"],
        "timestamp": data["timestamp"],
    }
