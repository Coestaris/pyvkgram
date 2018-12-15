import json

class cfg:
    def __init__(self, appId = '', admins = [], credentials = {}, tg_token = '', 
            timer_tick = 0, time_format = '', timeZone = 0, posts_to_get = 0, 
            between_request_delay = 0, sendFileTimeout=0, dbPrefix = "", dbNames = ""):
        self.appId = appId
        self.admins = admins
        self.credentials = credentials
        self.tg_token = tg_token
        self.time_format = time_format
        self.timer_tick = timer_tick
        self.time_zone = timeZone
        self.posts_to_get = posts_to_get
        self.between_request_delay = between_request_delay
        self.sendFileTimeout = sendFileTimeout
        self.dbPrefix = dbPrefix
        self.dbNames = dbNames

class stat:
    def __init__(self, vkRequests = {}, postAttachments = {}, tgRequests = {}, postSent = 0, forcedRequests = 0, postRecieved = 0):
        self.vkRequests = vkRequests
        self.tgRequests = tgRequests
        self.postAttachments = postAttachments
        self.postSent = postSent
        self.forcedRequests = forcedRequests
        self.postRecieved = postRecieved

    def toDict(self):
        return {
            "vkRequests" : self.vkRequests,
            "tgRequests" : self.tgRequests, 
            "postAttachments" : self.postAttachments,
            "postSent" : self.postSent,
            "forcedRequests" : self.forcedRequests,
            "postRecieved" : self.postRecieved
        }

    @staticmethod
    def parse(dict):
        a = stat(
            dict["vkRequests"],
            dict["postAttachments"],
            dict["tgRequests"],
            dict["postSent"],
            dict["forcedRequests"],
            dict["postRecieved"]
        )
        return a


def loadCfg():
    with open('../cfg.json') as f:
        data = json.load(f)
        return cfg(
            appId=data["appId"],
            admins=data["admins"],
            credentials=data["credentials"],
            tg_token=data["tg_token"],
            timer_tick=data["timer_tick"],
            time_format=data["time_format"],
            timeZone=data["time_zone"],
            posts_to_get=data["posts_per_request"],
            between_request_delay=data["between_requests_delay"],
            sendFileTimeout=data["sendFileTimeout"],
            dbPrefix=data["dbPrefix"],
            dbNames=data["dbNames"])

globalCfg = loadCfg()
globalStat = stat()