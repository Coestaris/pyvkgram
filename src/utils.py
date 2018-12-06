import json
import threading
from functools import wraps

import cfg
import language
import db
import re

LIST_OF_ADMINS = []
linkRegex = re.compile(r"\\\[(.+)\|(.+)\]")

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)

def replace_str_index(text, start_index=0, end_index=0, replacement=''):
    return '%s%s%s'%(text[:start_index], replacement, text[start_index + end_index+1:])

def makeVKLinks(input, toAdd='https://vk.com/{}'):
    matches = re.finditer(linkRegex, input)
    toReplace = []

    print(input)
    
    for match in enumerate(matches):
        start = match.start()
        end = match.end()

        link = input[match.start(0) : match.end(0) - match.start(0)]
        caption = input[match.start(1) : match.end(1) - match.start(1)]

        toReplace.append( (start, end, "({}{})[{}]".format(toAdd, link, caption)) )
    
    if(len(toReplace) != 0):
        for toReplace in range(len(toReplace) - 1, 0, step=-1):
            input = replace_str_index( input, toReplace[0], toReplace[1], toReplace[2] )

    return input

def escape_string(input, isBold=False, isItalic=False):
    input = u"{}".format(input)
    
    if(isBold): return input.replace("*", "\\*")
    elif(isItalic): return input.replace("_", "\\_")
    else: return input.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")

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
            credentials=data["credentials"],
            tg_token=data["tg_token"],
            timer_tick=data["timer_tick"],
            time_format=data["time_format"],
            timeZone=data["time_zone"],
            posts_to_get=data["posts_per_request"],
            between_request_delay=data["between_requests_delay"],
            sendFileTimeout=data["sendFileTimeout"])
        return c

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

