import json
import threading
from functools import wraps

import cfg
import language
import db

LIST_OF_ADMINS = []

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)

def escape_string(input):
    return input.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("]", "\\]").replace("`", "\\`")

def display_time(seconds, granularity=2):
    
    intervals = (
        ('weeks', 604800),  # 60 * 60 * 24 * 7
        ('days', 86400),    # 60 * 60 * 24
        ('hours', 3600),    # 60 * 60
        ('minutes', 60),
        ('seconds', 1),
    )
    
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{0:.0f} {1}".format(value, name))
    return ', '.join(result[:granularity])

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def send_action(action):
    def decorator(func):
        @wraps(func)
        def command_func(*args, **kwargs):
            bot, update = args
            bot.send_chat_action(chat_id=update.message.chat_id, action=action)
            func(bot, update, **kwargs)
        return command_func
    
    return decorator

def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            update.message.reply_text(language.getLang("ru")["err_not_allowed"].format(user_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped

def loadCfg():
    with open('../cfg.json') as f:
        data = json.load(f)
        c = cfg.cfg(
            appId=data["appId"],
            admins=data["admins"],
            login=data["user_login"],
            password=data["user_password"],
            tg_token=data["tg_token"],
            timer_tick=data["timer_tick"],
            time_format=data["time_format"],
            timeZone=data["time_zone"],
            posts_to_get=data["posts_per_request"],
            between_request_delay=data["between_requests_delay"])
        return c
