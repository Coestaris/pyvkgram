class cfg:
    def __init__(self, appId = '', admins = [], credentials = {}, tg_token = '', 
            timer_tick = 0, time_format = '', timeZone = 0, posts_to_get = 0, between_request_delay = 0):
        self.appId = appId
        self.admins = admins
        self.credentials = credentials
        self.tg_token = tg_token
        self.time_format = time_format
        self.timer_tick = timer_tick
        self.time_zone = timeZone
        self.posts_to_get = posts_to_get
        self.between_request_delay = between_request_delay

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

globalCfg = cfg()
globalStat = stat()