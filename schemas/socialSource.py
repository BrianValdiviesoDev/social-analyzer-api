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