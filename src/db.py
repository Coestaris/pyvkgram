from tinydb import TinyDB, Query
from tinydb.operations import delete

import dbUser

db = TinyDB('db.json')
User = Query()

def has_user(teleId):
    global db
    return db.contains(User.teleId == teleId)

def store_user(user):
    global db
    db.remove(User.teleId == user.teleId)
    db.insert(user.toDict())

def get_user(teleId):
    global db
    return dbUser.dbUser.parse(db.search(User.teleId == teleId)[0])
