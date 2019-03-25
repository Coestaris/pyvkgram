import json
import threading
from functools import wraps

import cfg
import language
import db

ef_default = 0
ef_bold = 1
ef_italic = 2
ef_link = 3

def formatLink(url, label):
    return u"[{}]({})".format(escape_string(label, ef_link), url)

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)

def replace_str_index(text, start_index=0, end_index=0, replacement=''):
    return u"{}{}{}".format(
        text[:start_index], 
        replacement, 
        text[end_index:])

def escape_string(input, format = ef_default):
    input = u"{}".format(input)
    
    if(format == ef_bold): return input.replace("*", "\\*")
    elif(format == ef_italic): return input.replace("_", "\\_")
    elif(format == ef_link): return input.replace("[", "\\[").replace("]", "\\]")
    else: return input.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")

def display_time_minimal(seconds):
    if(seconds < 3600):
        return "{}:{}".format(seconds // 60, seconds % 60)
    else:
        return "{}:{}:{}".format(seconds // 3600, seconds // 60, seconds % 60)

def display_time(seconds, granularity=2):
    
    intervals = (
        ('months', 2419200), # 60 * 60 * 24 * 7 * 4
        ('weeks', 604800),   # 60 * 60 * 24 * 7
        ('days', 86400),     # 60 * 60 * 24
        ('hours', 3600),     # 60 * 60
        ('minutes', 60),     # 60
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
        if user_id not in cfg.globalCfg.admins:
            update.message.reply_text(language.getLang("ru")["err_not_allowed"].format(user_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped

def incStat(key, array, c):
    if(key in array):
        value = array[key]
        array[key] = int(value) + c

    else: array[key] = c

def incStatVK(key):
    incStat(key, cfg.globalStat.vkRequests, 1)

def incStatTG(key):
    incStat(key, cfg.globalStat.tgRequests, 1)

def incAttachments(key, c):
    incStat(key, cfg.globalStat.postAttachments, c)

