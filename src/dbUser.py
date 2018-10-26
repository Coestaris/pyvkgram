class dbUser:
    def __init__(self, teleid, vkGroups = [], lang = "ru", currListening = 0, getPosts = {}):
        self.teleId = teleid
        self.vkGroups = vkGroups
        self.lang = lang
        
        self.currListening = currListening
        self.getPosts = getPosts

    def toDict(self):
        a =  {
            "teleId" : self.teleId,
            "vkGroups" : self.vkGroups,
            "lang" : self.lang,
            "listening" : self.currListening,
            "getPosts" : self.getPosts
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
        )