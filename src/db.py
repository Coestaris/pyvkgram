from tinydb import TinyDB, Query
import dbUser

db = TinyDB('db.json')
User = Query()

def has_user(teleId):
    global db
    return len(db.search(User.teleId == teleId)) != 0

def store_user(user):
    global db
    db.insert(user.toDict())

def get_user(teleId):
    global db
    return dbUser.dbUser.parse(db.search(User.teleId == teleId)[0])
