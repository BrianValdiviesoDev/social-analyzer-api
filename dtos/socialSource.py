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
