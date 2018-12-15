import json
import threading
from functools import wraps

import cfg
import language
import db
import re

LIST_OF_ADMINS = []
linkRegex = re.compile(r"\\\[(.+?)\|(.+?)\]", re.MULTILINE)

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
        text[start_index + end_index:])

def makeVKLinks(input, toAdd=u'https://vk.com/{}'):
    matches = re.finditer(linkRegex, input)
    toReplace = []

    #print(input)
    
    for match in matches:
        start = match.start()
        end = match.end()

        link = match.group(1)
        caption = match.group(2)

        toReplace.append( (start, end, u"[{}]({})".format( caption, toAdd.format(link)) ) )

    if(len(toReplace) != 0):

        #print toReplace

        for tr in reversed(toReplace):
            print tr
            #input = replace_str_index( input, tr[0], tr[1], tr[2] )

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

