class dbUser:
    def __init__(self, teleid, vkGroups = [], lang = "ru", currListening = 0, getPosts = {}, ignoreMonitoring = False, postFormat = {}, debugName = "-"):
        self.teleId = teleid
        self.vkGroups = vkGroups
        self.lang = lang
        self.currListening = currListening
        self.getPosts = getPosts
        self.debugName = debugName
        self.ignoreMonitoring = ignoreMonitoring
        self.postFormat = postFormat


    def toDict(self):
        a =  {
            "teleId" : self.teleId,
            "vkGroups" : self.vkGroups,
            "lang" : self.lang,
            "listening" : self.currListening,
            "getPosts" : self.getPosts,
            "ignoreMonitoring" : self.ignoreMonitoring,
            "postFormat" : self.postFormat,
            "debugName" : self.debugName
        }
        return a

    @staticmethod
    def parse(dict):
        user = dbUser(
            dict["teleId"],
            dict["vkGroups"],
            dict["lang"],
            dict["listening"],
            dict["getPosts"],
            dict["ignoreMonitoring"],
            dict["postFormat"],
            dict["debugName"] if "debugName" in dict else "-"
        )

        if('show_id' not in user.postFormat):
            user.postFormat = {
                'show_id' : True,
                'show_autor' : True,
                'show_date' : True,
                'show_likes' : True,
                'show_status' : True,
                'show_link' : True
            }
        
        return user