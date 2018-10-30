import vk
from posts import post
import requests
from bs4 import BeautifulSoup

def init(cfg):
    global api
    #vk.logger.setLevel('DEBUG')
    storage = vk.AuthSession(app_id = cfg.appId, user_login = cfg.login, user_password = cfg.password, scope = 0x111111)
    api = vk.API(storage, v = "5.35")
    pass

def get_group_info(grId):
    global api
    response = api.groups.getById(group_id=grId, fields=['name', 'id'])
    return ( response[0]["name"], response[0]["id"] )

def get_video(owner, vidID, access_key):
    global api
    request = "{}_{}_{}".format(owner, vidID, access_key)
    response = api.video.get(videos =  request, count = 1, offset = 0)
    return response["items"][0]

def get_video_direct_url(player_url):
    page = requests.get(player_url).content
    soup = BeautifulSoup(page, 'html.parser')
    #print soup.prettify()

    return [x.get('src') for x in soup.find_all('source')]


def get_posts(grId, isGroup, count, offset):
    global api
    #print "Get groups call"

    response = api.wall.get(
        owner_id = (-1 if isGroup else 1) * grId,
        count = count,
        offset = offset
    )

    #print response
    posts = []
    for x in response["items"]:
        posts.append(post(x))

    return posts