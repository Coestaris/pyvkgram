from tinydb import TinyDB, Query
from tinydb.operations import delete

import dbUser
import cfg

dbFileName = 'db.json'

userTable = TinyDB(dbFileName).table('users')
utilsTable = TinyDB(dbFileName).table('time')
User = Query()

def reassign_db():
    global userTable
    global utilsTable
    global User

    userTable = TinyDB(dbFileName).table('users')
    utilsTable = TinyDB(dbFileName).table('time')
    User = Query()

def has_user(teleId):
    global userTable
    return userTable.contains(User.teleId == teleId)

def store_user(user):
    global userTable
    userTable.remove(User.teleId == user.teleId)
    userTable.insert(user.toDict())

def store_stat(stat):
    global utilsTable
    userTable.update(stat.toDict())

def get_stat():
    global utilsTable
    l = utilsTable.all()
    if(len(l) == 0):
        return None
    else:
        return cfg.stat(l[0])

def get_users():
    global userTable
    return [dbUser.dbUser.parse(x) for x in userTable.all()]

def store_time(time):
    global utilsTable
    utilsTable.update({'time': time})

def get_time():
    global utilsTable
    l = utilsTable.all()
    if(len(l) == 0):
        return None
    else:
        return l[0]["time"]

def get_user(teleId):
    global userTable
    return dbUser.dbUser.parse(userTable.search(User.teleId == teleId)[0])

def store_ccn(ccn):
    global utilsTable
    utilsTable.update( {'cnn': ccn} ) 

#cycleCredentialNumber
def get_ccn():
    global utilsTable
    l = utilsTable.all()
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
