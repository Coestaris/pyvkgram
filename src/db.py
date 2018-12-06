from tinydb import TinyDB, Query
from tinydb.operations import delete

import dbUser
import cfg

dbFileName = 'db.json'

userTable = TinyDB(dbFileName).table('users')
timeTable = TinyDB(dbFileName).table('time')
cnnTable = TinyDB(dbFileName).table('cnn')
statTable = TinyDB(dbFileName).table('stat')
User = Query()

def reassign_db():
    cfg.globalStat = cfg.stat()

    global userTable
    global timeTable
    global User

    userTable = TinyDB(dbFileName).table('users')
    timeTable = TinyDB(dbFileName).table('time')
    statTable = TinyDB(dbFileName).table('stat')
    cnnTable = TinyDB(dbFileName).table('cnn')

    timeTable.insert({ "time" : 0, })
    statTable.insert(cfg.globalStat.toDict())

    User = Query()

def has_user(teleId):
    global userTable
    return userTable.contains(User.teleId == teleId)

def store_user(user):
    global userTable
    userTable.remove(User.teleId == user.teleId)
    userTable.insert(user.toDict())

def store_stat(stat):
    global statTable
    statTable.purge()
    statTable.insert(stat.toDict())

def get_stat():
    global statTable
    l = statTable.all()
    if(len(l) == 0):
        return None
    else:
        return cfg.stat.parse(l[0])

def get_users():
    global userTable
    return [dbUser.dbUser.parse(x) for x in userTable.all()]

def store_time(time):
    global timeTable
    timeTable.purge()
    timeTable.insert({'time': time})

def get_time():
    global timeTable
    l = timeTable.all()
    if(len(l) == 0):
        return None
    else:
        return l[0]["time"]

def get_user(teleId):
    global userTable
    return dbUser.dbUser.parse(userTable.search(User.teleId == teleId)[0])

def store_ccn(ccn):
    global cnnTable
    cnnTable.purge()
    cnnTable.insert( {'cnn': ccn} ) 

#cycleCredentialNumber
def get_ccn():
    global cnnTable
    l = statTable.all()
    if(len(l) == 0):
        return None
    else:
        return l[0]["ccn"]

def manage_ccn():
    ccn = get_ccn()
    if(ccn >= len(cfg.globalCfg.credentials)): ccn = 0
    else: ccn += 1

    store_ccn(ccn)
    return ccn
