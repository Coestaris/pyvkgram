import os

from tinydb import TinyDB, Query
from tinydb.operations import delete

import dbUser
import cfg

postsDBFileName = u'{}/{}'.format(cfg.globalCfg.dbPrefix, cfg.globalCfg.dbNames["posts"])
mainDBFileName = u'{}/{}'.format(cfg.globalCfg.dbPrefix, cfg.globalCfg.dbNames["main"])

timeTable = TinyDB(mainDBFileName).table('time')
cnnTable = TinyDB(mainDBFileName).table('cnn')
statTable = TinyDB(mainDBFileName).table('stat')
postsTable = TinyDB(postsDBFileName)

userTable = TinyDB(mainDBFileName).table('users')
User = Query()

def reassign_db():
    cfg.globalStat = cfg.stat()

    #Tables
    global cnnTable
    global userTable
    global timeTable
    global postsTable

    global User

    userTable = TinyDB(mainDBFileName).table('users')
    timeTable = TinyDB(mainDBFileName).table('time')
    statTable = TinyDB(mainDBFileName).table('stat')
    cnnTable = TinyDB(mainDBFileName).table('cnn')

    timeTable.insert({ "time" : 0, })
    statTable.insert(cfg.globalStat.toDict())

    User = Query()

class userHandle:

    @staticmethod
    def drop(teleId = None) :
        global mainDBFileName
        
        os.remove(mainDBFileName)
        reassign_db()
        if(teleId != None):
            userHandle.store_user(dbUser.dbUser(teleId))

    @staticmethod        
    def has_user(teleId):
        global userTable
        return userTable.contains(User.teleId == teleId)

    @staticmethod
    def store_user(user):
        global userTable
        userTable.remove(User.teleId == user.teleId)
        userTable.insert(user.toDict())

    @staticmethod
    def get_users():
        global userTable
        return [dbUser.dbUser.parse(x) for x in userTable.all()]

    @staticmethod
    def get_user(teleId):
        global userTable
        return dbUser.dbUser.parse(userTable.search(User.teleId == teleId)[0])

class statTimeHandle:

    @staticmethod      
    def store_stat(stat):
        global statTable
        statTable.purge()
        statTable.insert(stat.toDict())

    @staticmethod
    def get_stat():
        global statTable
        l = statTable.all()
        if(len(l) == 0):
            return None
        else:
            return cfg.stat.parse(l[0])

    @staticmethod
    def store_time(time):
        global timeTable
        timeTable.purge()
        timeTable.insert({'time': time})

    @staticmethod
    def get_time():
        global timeTable
        l = timeTable.all()
        if(len(l) == 0):
            return None
        else:
            return l[0]["time"]

def is_post_sent(user, id):
    pass

def store_ccn(ccn):
    global cnnTable
    cnnTable.purge()
    cnnTable.insert( {'cnn': ccn} ) 

#cycleCredentialNumber
def get_ccn():
    
    return 0
    
    #global cnnTable
    #l = cnnTable.all()
    #if(len(l) == 0):
    #    return None
    #else:
    #    return l[0]["ccn"]

def manage_ccn():
    ccn = get_ccn()
    if(ccn >= len(cfg.globalCfg.credentials)): ccn = 0
    else: ccn += 1

    store_ccn(ccn)
    return ccn

