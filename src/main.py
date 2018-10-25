import vk
import json
import cfg

def loadCfg():
    with open('../cfg.json') as f:
        data = json.load(f)
        c = cfg.cfg(
            data["appId"],
            data["user_login"],
            data["user_password"],
            data["tg_token"],
            data["timer_tick"],
            data["time_format"])
        return c

cfg = loadCfg()

#session = vk.AuthSession(app_id=6646136, user_login="", user_password="")
#api = vk.API(session)
#print(api._session.access_token)
#print(api.users.get(user_ids=1))