import requests

from bs4 import BeautifulSoup

from posts import post
import vk
import cfg
import db
import utils

def reinit(number):
    utils.incStatVK("auth")

    global api
    storage = vk.AuthSession(
        app_id = cfg.globalCfg.appId, 
        user_login = cfg.globalCfg.credentials[number]["login"], 
        user_password = cfg.globalCfg.credentials[number]["password"], 
        scope = 0x111111)

    api = vk.API(storage, v = "5.35")
    pass

def get_group_info(grId):
    utils.incStatVK("groups.getById")

    global api
    response = api.groups.getById(group_id=grId, fields=['name', 'id'])
    return ( response[0]["name"], response[0]["id"] )

def get_video(owner, vidID, access_key):
    utils.incStatVK("video.get")

    global api
    request = "{}_{}_{}".format(owner, vidID, access_key)
    response = api.video.get(videos =  request, count = 1, offset = 0)
    return response["items"][0]

def get_video_direct_url(player_url):
    page = requests.get(player_url).content
    soup = BeautifulSoup(page, 'html.parser')
    #print soup.prettify()

    return [x.get('src') for x in soup.find_all('source')]


def get_posts(grId, isGroup, count, offset, reinited=0):
    utils.incStatVK("wall.get")

    global api

    try:
        response = api.wall.get(
            owner_id = (-1 if isGroup else 1) * grId,
            count = count,
            offset = offset
        )

    except:
        
        if(reinited == len(cfg.globalCfg.credentials)):
            print("After reiniting nothing fixed =c")
            raise SystemExit

        else:
            cnn = db.manage_ccn()

            print("WARNING!!! Some shit happened! Trying to reinit, to fix it to {}...".format(cnn))
            reinit(cnn)
            return get_posts(grId, isGroup, count, offset, reinited)

    #print response
    posts = []
    for x in response["items"]:
        posts.append(post(x))

    return posts