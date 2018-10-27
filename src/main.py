from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram

import logging
import json
import dbUser

import re
import db
import language
import cfg
import vkcore

urlRePublicFull = re.compile(r"((?<=^https:\/\/vk\.com\/club)\d{4,})|((?<=^https:\/\/vk\.com\/public)\d{4,})$", re.MULTILINE)
urlRePublic = re.compile(r"(?<=^https:\/\/vk\.com\/)(.+)$", re.MULTILINE)
urlRePublicId = re.compile(r"^\d{4,}$", re.MULTILINE)
groupRe = re.compile(r"^\d{4,} - .+$")

from functools import wraps
from telegram import ChatAction

def send_action(action):
    def decorator(func):
        @wraps(func)
        def command_func(*args, **kwargs):
            bot, update = args
            bot.send_chat_action(chat_id=update.message.chat_id, action=action)
            func(bot, update, **kwargs)
        return command_func
    
    return decorator

send_typing_action = send_action(ChatAction.TYPING)
send_upload_video_action = send_action(ChatAction.UPLOAD_VIDEO)
send_upload_photo_action = send_action(ChatAction.UPLOAD_PHOTO)

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


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

@send_typing_action
def start(bot, update):
    if(not db.has_user(update.message.chat_id)):
        db.store_user(dbUser.dbUser(update.message.chat_id))

    user = db.get_user(update.message.chat_id)
    update.message.reply_text(language.getLang(user.lang)["help"], reply_markup = { "remove_keyboard" : True })

@send_typing_action
def help(bot, update):
    user = db.get_user(update.message.chat_id)
    update.message.reply_text(language.getLang(user.lang)["help"], reply_markup = { "remove_keyboard" : True })

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

@send_typing_action
def unsubscribe(bot, update):
    user = db.get_user(update.message.chat_id)
    
    if(len(user.vkGroups) == 0):
        update.message.reply_text(language.getLang(user.lang)["group_list_is_empty"], reply_markup = { "remove_keyboard" : True })
        return
    
    custom_keyboard = []
    for group in user.vkGroups:
        custom_keyboard.append([telegram.KeyboardButton(text="{} - {}".format(group["id"], group["name"]))])

    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text(language.getLang(user.lang)["select_group"], reply_markup=reply_markup)
    user.currListening = 1
    db.store_user(user)

    pass

@send_typing_action
def textInput(bot, update):
    user = db.get_user(update.message.chat_id)

    if(groupRe.search(update.message.text) and user.currListening == 1):

        user.currListening = 0
        db.store_user(user)

        id = int(update.message.text.split('-')[0].strip())
        name = update.message.text.split('-')[1].strip()
        
        if(any(x["id"] == id for x in user.vkGroups)):
            user.vkGroups = [x for x in user.vkGroups if x["id"] != id]
            db.store_user(user)
            
            bot.send_message(
                chat_id = update.message.chat_id, 
                text = language.getLang(user.lang)["succ_removed_url"].format(name, id), 
                parse_mode = telegram.ParseMode.MARKDOWN,
                reply_markup = { "remove_keyboard" : True })
        else:

            update.message.reply_text(language.getLang(user.lang)["err_unknown_id"], reply_markup = { "remove_keyboard" : True })
            return

    else:
        return

@send_typing_action
def getGroups(bot, update):
    user = db.get_user(update.message.chat_id)
    if(len(user.vkGroups) == 0):
        update.message.reply_text(language.getLang(user.lang)["group_list_is_empty"], reply_markup = { "remove_keyboard" : True })
    else:
        text = language.getLang(user.lang)["group_list"] + '\n'
        for group in user.vkGroups:
            text += '- *{}* (ID: {})\n'.format(group["name"], group["id"])
        
        bot.send_message(
            chat_id = update.message.chat_id, 
            text = text, 
            parse_mode = telegram.ParseMode.MARKDOWN,
            reply_markup = { "remove_keyboard" : True })
        
        
@send_typing_action
def subscribe(bot, update):
    user = db.get_user(update.message.chat_id)
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
    
    if(any(x["id"] == int(id) for x in user.vkGroups)):
        update.message.reply_text(language.getLang(user.lang)["err_already_exists_url"], reply_markup = { "remove_keyboard" : True })
        return


    info = vkcore.get_group_info(id)
    if(info[0] == ''):
        update.message.reply_text(language.getLang(user.lang)["err_cant_find_url"], reply_markup = { "remove_keyboard" : True })
        return

    user.vkGroups.append( { "name" : info[0], "id" : info[1] } )
    db.store_user(user)
    
    bot.send_message(
        chat_id = update.message.chat_id, 
        text = language.getLang(user.lang)["succ_added_new_url"].format(info[0], info[1]), 
        parse_mode = telegram.ParseMode.MARKDOWN,
        reply_markup = { "remove_keyboard" : True })

def main():
    cfg = loadCfg()
    vkcore.init(cfg)

    updater = Updater(cfg.tg_token)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("subscribe", subscribe))
    dp.add_handler(CommandHandler("unsubscribe", unsubscribe))
    dp.add_handler(CommandHandler("getgroups", getGroups))

    dp.add_handler(MessageHandler(Filters.text, textInput))

    dp.add_error_handler(error)

    logger.log(logging.INFO, "Starting polling...")
    updater.start_polling()

    logger.log(logging.INFO, "Going to loop...")
    updater.idle()

if __name__ == '__main__':
    main()