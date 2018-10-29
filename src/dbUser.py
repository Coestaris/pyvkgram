class dbUser:
    def __init__(self, teleid, vkGroups = [], lang = "ru", currListening = 0, getPosts = {}, ignoreMonitoring = False, postFormat = 0):
        self.teleId = teleid
        self.vkGroups = vkGroups
        self.lang = lang
        self.currListening = currListening
        self.getPosts = getPosts

        self.ignoreMonitoring = ignoreMonitoring
        self.postFormat = postFormat
        # 0 - default
        # 1 - minimal

    def toDict(self):
        a =  {
            "teleId" : self.teleId,
            "vkGroups" : self.vkGroups,
            "lang" : self.lang,
            "listening" : self.currListening,
            "getPosts" : self.getPosts,
            "ignoreMonitoring" : self.ignoreMonitoring,
            "postFormat" : self.postFormat
        }
        return a

    @staticmethod
    def parse(dict):
        return dbUser(
            dict["teleId"],
            dict["vkGroups"],
            dict["lang"],
            dict["listening"],
            dict["getPosts"],
            dict["ignoreMonitoring"],
            dict["postFormat"]
        )