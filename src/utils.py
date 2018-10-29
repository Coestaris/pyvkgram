import json
import logging
import random
import re
import threading
from datetime import datetime
from functools import wraps

import telegram
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

import cfg
import db
import dbUser
import language
import vkcore
from posts import attachmentTypes

LIST_OF_ADMINS = []

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
        user = db.get_user(update.message.chat_id)
        if user_id not in LIST_OF_ADMINS:
            update.message.reply_text(language.getLang(user.lang)["err_not_allowed"].format(user_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped

def loadCfg():
    with open('../cfg.json') as f:
        data = json.load(f)
        c = cfg.cfg(
            data["appId"],
            data["admins"],
            data["user_login"],
            data["user_password"],
            data["tg_token"],
            data["timer_tick"],
            data["time_format"])
        return c
