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
        "videoId": data["videoId"]
    }


def YoutubeVideoStatisticsDto(data) -> list:
    return [YoutubeVideoStatisticDto(v) for v in data]


def YoutubeStatisticsDto(data) -> dict:
    return {
        "channelName": data["channelName"],
        "subs": data["subs"],
        "videos": data["videos"],
        "visualizations": data["visualizations"],
        "startAt": data["startAt"],
        "timestamp": data["timestamp"],
    }
