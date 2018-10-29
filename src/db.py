from tinydb import TinyDB, Query
from tinydb.operations import delete

import dbUser

dbFileName = 'db.json'

userTable = TinyDB(dbFileName).table('users')
timeTable = TinyDB(dbFileName).table('time')
User = Query()

def reassign_db():
    global userTable
    global timeTable
    global User

    userTable = TinyDB(dbFileName).table('users')
    timeTable = TinyDB(dbFileName).table('time')
    User = Query()

def has_user(teleId):
    global userTable
    return userTable.contains(User.teleId == teleId)

def store_user(user):
    global userTable
    userTable.remove(User.teleId == user.teleId)
    userTable.insert(user.toDict())

def get_users():
    global userTable
    return [dbUser.dbUser.parse(x) for x in userTable.all()]

def store_time(time):
    global timeTable
    timeTable.purge()
    timeTable.insert({'time' : time })

def get_time():
    global timeTable
    l = timeTable.all()
    if(len(l) == 0):
        return None
    else:
        return l[0]

def get_user(teleId):
    global userTable
    return dbUser.dbUser.parse(userTable.search(User.teleId == teleId)[0])
