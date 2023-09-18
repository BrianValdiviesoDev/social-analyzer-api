def categoryEntity(category) -> dict:
    return {
        "uuid": category["uuid"],
        "name": category["name"],
        "parent": category["parent"],
        "active": category["active"]
        }


def categoriesEntity(categories) -> list:
    return [categoryEntity(category) for category in categories]