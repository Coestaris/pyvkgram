class cfg:
    def __init__(self, appId = '', admins = [], login = '', password = '', tg_token = '', timer_tick = 0, time_format = ''):
        self.appId = appId
        self.admins = admins
        self.login = login
        self.password = password
        self.tg_token = tg_token
        self.time_format = time_format
        self.timer_tick = timer_tick

globalCfg = cfg()