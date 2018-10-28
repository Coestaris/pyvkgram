import vk
from posts import post
import requests
from bs4 import BeautifulSoup

def init(cfg):
    global api
    
    storage = vk.AuthSession(app_id = cfg.appId, user_login = cfg.login, user_password = cfg.password, scope = 0x111111)
    api = vk.API(storage, v = "5.35")

    print storage.access_token
    pass

def get_group_info(grId):
    global api
    response = api.groups.getById(group_id=grId, fields=['name', 'id'])
    return ( response[0]["name"], response[0]["id"] )

def get_video(owner, vidID, access_key):
    global api
    request = "{}_{}_{}".format(owner, vidID, access_key)
    response = api.video.get(videos =  request, count = 1, offset = 0)

    #print response["items"][0]

    return response["items"][0]

def get_video_direct_url(player_url):
    page = requests.get(player_url).content
    soup = BeautifulSoup(page, 'html.parser')

    #print soup.prettify()

    return soup.find('source').get('src')


print(get_video_direct_url("https://vk.com/video_ext.php?oid=239202396&id=169933357&hash=c05231377a965a37&__ref=vk.api&api_hash=1540752451106b9df1662c26d224_GE3TINZZGY2TENI%27"))


def get_posts(grId, isGroup, count, offset):
    global api
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