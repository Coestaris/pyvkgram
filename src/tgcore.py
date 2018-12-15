#coding:utf-8

import time
import psutil
import re
import telegram
import random
import json
from datetime import datetime
import traceback
import os

import postSender
import menuHandler
import dbUser
import vkcore
import posts
import db
import utils
import cfg
import language

startTime = time.time()

urlRePublicFull = re.compile(r"((?<=^https:\/\/vk\.com\/club)\d{4,})|((?<=^https:\/\/vk\.com\/public)\d{4,})$", re.MULTILINE)
urlRePublic = re.compile(r"(?<=^https:\/\/vk\.com\/)(.+)$", re.MULTILINE)
urlRePublicId = re.compile(r"^\d{4,}$", re.MULTILINE)
groupRe = re.compile(r"^\d{4,} - .+$")
bot = None

send_typing_action = utils.send_action(telegram.ChatAction.TYPING)
send_upload_video_action = utils.send_action(telegram.ChatAction.UPLOAD_VIDEO)
send_upload_photo_action = utils.send_action(telegram.ChatAction.UPLOAD_PHOTO)

@send_typing_action
def start(bot, update):
    utils.incStatTG("start")

    currentDataPackage = {
        "action" : "start",
        "chat_id" : update.message.chat_id,
    }

    try:
        if(not db.userHandle.has_user(update.message.chat_id)):
            db.userHandle.store_user(dbUser.dbUser(teleid=update.message.chat_id, debugName=update.message.from_user.first_name))

        user = db.userHandle.get_user(update.message.chat_id)
        update.message.reply_text(language.getLang(user.lang)["help"], reply_markup = { "remove_keyboard" : True })
    
    except Exception as ex:
        postSender.notify_admin(ex, currentDataPackage)

@send_typing_action
def help(bot, update):
    utils.incStatTG("help")

    currentDataPackage = {
        "action" : "help",
        "chat_id" : update.message.chat_id,
    }

    try:
        user = db.userHandle.get_user(update.message.chat_id)
        update.message.reply_text(language.getLang(user.lang)["help"], reply_markup = { "remove_keyboard" : True })

    except Exception as ex:
        postSender.notify_admin(ex, currentDataPackage)

@send_typing_action
def settings(bot, update):
    utils.incStatTG("settings")
    
    currentDataPackage = {
        "action" : "settings",
        "chat_id" : update.message.chat_id,
    }

    try:
        user = db.userHandle.get_user(update.message.chat_id)
        bot.send_message(chat_id=user.teleId, text="Выбирите кнопку из списка", reply_markup=menuHandler.get_main_menu(user, bot))
    
    except Exception as ex:
        postSender.notify_admin(ex, currentDataPackage)

def callback_inline(bot, update):
    utils.incStatTG("_inline_callbacks")
    
    currentDataPackage = {
        "action" : "_inline_callbacks",
        "chat_id" : update.callback_query.message.chat_id,
        "act" : update.callback_query.data
    }

    try:
        query = update.callback_query

        user = db.userHandle.get_user(query.message.chat_id)
        act = query.data

        markup = menuHandler.get_menu(act, user, bot)
        if(not isinstance(markup, telegram.InlineKeyboardMarkup)):
            bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        else:
            bot.edit_message_reply_markup(chat_id=query.message.chat_id, reply_markup = markup, message_id=query.message.message_id)

    except Exception as ex:
        postSender.notify_admin(ex, currentDataPackage)

def errorHandler(bot, update, error):
    utils.incStatTG("_error")

    try:
        postSender.notify_admin(error)
        #postSender.notify_admin_message(error)
        if(update != None):
            user = db.userHandle.get_user(update.message.chat_id)
            update.message.reply_text(language.getLang(user.lang)["server_error"], reply_markup = { "remove_keyboard" : True })

    except Exception as ex:
        postSender.notify_admin(ex) #No sense to put dataPackage here...

@send_typing_action
def unsubscribe(bot, update):
    utils.incStatTG("unsubscribe")

    currentDataPackage = {
        "action" : "unsubscribe",
        "chat_id" : update.message.chat_id,
    }

    try:
        user = db.userHandle.get_user(update.message.chat_id)
        if(len(user.vkGroups) == 0):
            update.message.reply_text(language.getLang(user.lang)["group_list_is_empty"], reply_markup = { "remove_keyboard" : True })
            return
        
        custom_keyboard = []
        for group in user.vkGroups:
            custom_keyboard.append([telegram.KeyboardButton(text=u"{} - {}".format(group["id"], group["name"]))])

        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
        update.message.reply_text(language.getLang(user.lang)["select_group"], reply_markup=reply_markup)
        user.currListening = 1
        db.userHandle.store_user(user)
    
    except Exception as ex:
        postSender.notify_admin(ex, currentDataPackage)

@send_typing_action
def getPosts(bot, update):
    utils.incStatTG("getPosts")

    currentDataPackage = {
        "action" : "getPosts",
        "chat_id" : update.message.chat_id,
        "message_text" : update.message.text
    }

    try:
        user = db.userHandle.get_user(update.message.chat_id)
        if(len(user.vkGroups) == 0):
            update.message.reply_text(language.getLang(user.lang)["group_list_is_empty"], reply_markup = { "remove_keyboard" : True })
            return

        parts = [x for x in update.message.text.lower().replace("/getposts", "").strip().split(' ') if x != '']
        count = 5
        offset = 0

        if(len(parts) >= 2):
            count = int(parts[0])
            offset = int(parts[1])
        else:
            if(len(parts) == 1):
                count = int(parts[0])

        custom_keyboard = []
        for group in user.vkGroups:
            custom_keyboard.append([telegram.KeyboardButton(text=u"{} - {}".format(group["id"], group["name"]))])

        user.getPosts = { "count" : count, "offset" : offset }
        user.currListening = 2

        db.userHandle.store_user(user)

        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
        update.message.reply_text(language.getLang(user.lang)["get_posts"].format(count), reply_markup=reply_markup)

    except Exception as ex:
        postSender.notify_admin(ex, currentDataPackage)

@send_typing_action
def textInputHandler(bot, update):
    utils.incStatTG("_textInput")

    currentDataPackage = {
        "action" : "_textInput",
        "chat_id" : update.message.chat_id,
        "message_text" : update.message.text
    }

    try:
        user = db.userHandle.get_user(update.message.chat_id)
        if(groupRe.search(update.message.text)):

            id = int(update.message.text.split('-')[0].strip())
            name = update.message.text.split('-')[1].strip()
            
            if(any(x["id"] == id for x in user.vkGroups)):
                
                if(user.currListening == 1):
                    
                    user.vkGroups = [x for x in user.vkGroups if x["id"] != id]
                    db.userHandle.store_user(user)
                    bot.send_message(
                        chat_id = update.message.chat_id, 
                        text = language.getLang(user.lang)["succ_removed_url"].format(name, id), 
                        parse_mode = telegram.ParseMode.MARKDOWN,
                        reply_markup = { "remove_keyboard" : True })
                
                elif(user.currListening == 2):
                    
                    bot.send_message(chat_id = update.message.chat_id, text = language.getLang(user.lang)["getting_posts"].format(user.getPosts["count"], name, id), 
                        parse_mode = telegram.ParseMode.MARKDOWN,
                        reply_markup = { "remove_keyboard" : True })

                    posts = vkcore.get_posts(id, True, user.getPosts["count"], user.getPosts["offset"])
                    cfg.globalStat.postSent += len(posts) 
                    cfg.globalStat.postRecieved += len(posts)

                    for post in posts:
                        postSender.send_post(bot, name, id, post, user)
                else:
                    update.message.reply_text(random.choice(language.getLang(user.lang)["group_text_reply"]), reply_markup = { "remove_keyboard" : True })

            else:
                update.message.reply_text(language.getLang(user.lang)["err_unknown_id"], reply_markup = { "remove_keyboard" : True })
                return

            user.currListening = 0
            db.userHandle.store_user(user)

        else:
            update.message.reply_text(random.choice(language.getLang(user.lang)["text_reply"]), reply_markup = { "remove_keyboard" : True })
            return
    
    except Exception as ex:
        postSender.notify_admin(ex, currentDataPackage)

@send_typing_action
def getGroups(bot, update):
    utils.incStatTG("getGroups")

    currentDataPackage = {
        "action" : "getGroups",
        "chat_id" : update.message.chat_id,
    }

    try:

        #sraise TypeError()

        user = db.userHandle.get_user(update.message.chat_id)
        if(len(user.vkGroups) == 0):
            update.message.reply_text(language.getLang(user.lang)["group_list_is_empty"], reply_markup = { "remove_keyboard" : True })
        else:
            text = language.getLang(user.lang)["group_list"] + '\n'
            for group in user.vkGroups:
                text += language.getLang(user.lang)["get_groups"].format(
                    utils.escape_string(group["name"], True), group["id"])
            
            bot.send_message(
                chat_id = update.message.chat_id, 
                text = text, 
                parse_mode = telegram.ParseMode.MARKDOWN,
                reply_markup = { "remove_keyboard" : True })  

    except Exception as ex:
        postSender.notify_admin(ex, currentDataPackage)
        
@send_typing_action
def subscribe(bot, update):
    utils.incStatTG("subscribe")

    currentDataPackage = {
        "action" : "subscribe",
        "chat_id" : update.message.chat_id,
        "message_text" : update.message.text,
    }

    try:
        user = db.userHandle.get_user(update.message.chat_id)
        url = update.message.text.replace("/subscribe", "").strip()
        id = ""

        if(url == ""):
            update.message.reply_text(language.getLang(user.lang)["err_empty_public_url"], reply_markup = { "remove_keyboard" : True })
            return
        else:
            if(urlRePublicFull.search(url)):
                id = urlRePublicFull.search(url).group()

            elif(urlRePublic.search(url)):
                id = urlRePublic.search(url).group()

            elif(urlRePublicId.search(url)):
                id = urlRePublicId.search(url).group()

            else:
                update.message.reply_text(language.getLang(user.lang)["err_wrong_public_url"], reply_markup = { "remove_keyboard" : True })
                return
        
        info = vkcore.get_group_info(id)

        if(info[0] == ''):
            update.message.reply_text(language.getLang(user.lang)["err_cant_find_url"], reply_markup = { "remove_keyboard" : True })
            return
        
        if(any(x["id"] == info[1] for x in user.vkGroups)):
            update.message.reply_text(language.getLang(user.lang)["err_already_exists_url"], reply_markup = { "remove_keyboard" : True })
            return

        user.vkGroups.append( { "name" : info[0], "id" : info[1] } )
        db.userHandle.store_user(user)
        
        bot.send_message(
            chat_id = update.message.chat_id, 
            text = language.getLang(user.lang)["succ_added_new_url"].format(info[0], info[1]), 
            parse_mode = telegram.ParseMode.MARKDOWN,
            reply_markup = { "remove_keyboard" : True })

    except Exception as ex:
        postSender.notify_admin(ex, currentDataPackage)

@send_typing_action
@utils.restricted
def adm_stat(bot, update):
    utils.incStatTG("adm_stat")

    currentDataPackage = {
        "action" : "adm_stat",
        "chat_id" : update.message.chat_id,
    }

    try:
        pid = os.getpid()
        py = psutil.Process(pid)
        mem = psutil.virtual_memory()

        bot.send_message(
            chat_id = update.message.chat_id, 
            text = (u"*CPU*: {}_%_\n\n*Mem*:\n_Total_: {}\n_Available_: {}\n_Free_: {}\n_Used_: {} ({}%)\n\n*Server uptime*: {}\n\n*Bot uptime*: {}" +
            u"\n\n*Posts Sent*: {}\n*Posts recieved*: {}\n*Posts reRecieved*: {}" +
            u"\n\n*Post attachments*: {}\n\n*VK Requests*: {}\n\n*Telegram calls*: {}")
                .format(psutil.cpu_percent(), 
                    utils.sizeof_fmt(mem.total), 
                    utils.sizeof_fmt(mem.available), 
                    utils.sizeof_fmt(mem.free), 
                    utils.sizeof_fmt(mem.used), 
                    mem.percent, 
                    utils.display_time(time.time() - psutil.boot_time(), 5), 
                    utils.display_time(time.time() - py.create_time(), 5),
                    cfg.globalStat.postSent,
                    cfg.globalStat.postRecieved,
                    cfg.globalStat.forcedRequests,
                    "list is empty" if len(cfg.globalStat.postAttachments) == 0 else '\n' + "\n".join([u"  - *{}* : _{}_".format(utils.escape_string(k, True), utils.escape_string(v, False, True)) for k, v in iter(cfg.globalStat.postAttachments.items())]),
                    "list is empty" if len(cfg.globalStat.vkRequests) == 0 else '\n' +"\n".join([u"  - *{}* : _{}_".format(utils.escape_string(k, True), utils.escape_string(v, False, True)) for k, v in iter(cfg.globalStat.vkRequests.items())]),
                    "list is empty" if len(cfg.globalStat.tgRequests) == 0 else '\n' +"\n".join([u"  - *{}* : _{}_".format(utils.escape_string(k, True), utils.escape_string(v, False, True)) for k, v in iter(cfg.globalStat.tgRequests.items())])),
            
            parse_mode = telegram.ParseMode.MARKDOWN,
            reply_markup = { "remove_keyboard" : True })
    
    except Exception as ex:
        postSender.notify_admin(ex, currentDataPackage)

@send_typing_action
@utils.restricted
def adm_db_dump(bot, update):
    utils.incStatTG("adm_dump")

    currentDataPackage = {
        "action" : "adm_dump",
        "chat_id" : update.message.chat_id,
    }

    try:
        db.statTimeHandle.store_stat(cfg.globalStat)
        
        with open(db.mainDBFileName) as f:
            data = json.load(f)

            bot.send_message(
                chat_id = update.message.chat_id, 
                text = u"```json{{\n{}```".format(json.dumps(data, sort_keys=True, indent=2)),
                parse_mode = telegram.ParseMode.MARKDOWN,
                reply_markup = { "remove_keyboard" : True })
        
    except Exception as ex:
        postSender.notify_admin(ex, currentDataPackage)


@send_typing_action
@utils.restricted
def adm_db_drop(bot, update):
    utils.incStatTG("adm_drop")

    currentDataPackage = {
        "action" : "adm_drop",
        "chat_id" : update.message.chat_id,
    }

    try:
        bot.send_message(
            chat_id = update.message.chat_id, 
            text = "Are you sure you want to drop database?",
            reply_markup = menuHandler.confirm_drop())

    except Exception as ex:
        postSender.notify_admin(ex, currentDataPackage)
