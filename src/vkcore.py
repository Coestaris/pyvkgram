import vk
from posts import post

def init(cfg):
    global api
    
    storage = vk.AuthSession(app_id = cfg.appId, user_login = cfg.login, user_password = cfg.password)
    api = vk.API(storage, v = "5.35")
    pass

def get_group_info(grId):
    global api
    response = api.groups.getById(group_id=grId, fields=['name', 'id'])
    return ( response[0]["name"], response[0]["id"] )

def get_posts(grId, isGroup, count, offset):
    global api
    response = api.wall.get(
        owner_id = (-1 if isGroup else 1) * grId,
        count = count,
        offset = offset
    )

    posts = []
    for x in response["items"]:
        posts.append(post(x))

    print response
    return posts