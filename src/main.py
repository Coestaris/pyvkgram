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

def start(bot, update):
    if(not db.has_user(update.message.chat_id)):
        db.store_user(dbUser.dbUser(update.message.chat_id))

    user = db.get_user(update.message.chat_id)
    update.message.reply_text(language.getLang(user.lang)["help"])

def help(bot, update):
    user = db.get_user(update.message.chat_id)
    update.message.reply_text(language.getLang(user.lang)["help"])

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

def getGroups(bot, update):
    user = db.get_user(update.message.chat_id)
    if(len(user.vkGroups) == 0):
        update.message.reply_text(language.getLang(user.lang)["group_list_is_empty"])
    else:
        text = language.getLang(user.lang)["group_list"] + '\n'
        for group in user.vkGroups:
            text += '- *{}* (ID: {})\n'.format(group["name"], group["id"])
        
        bot.send_message(
            chat_id = update.message.chat_id, 
            text = text, 
            parse_mode = telegram.ParseMode.MARKDOWN)
        
        

def subscribe(bot, update):
    user = db.get_user(update.message.chat_id)
    url = update.message.text.replace("/subscribe", "").strip()
    id = ""

    if(url == ""):
        update.message.reply_text(language.getLang(user.lang)["err_empty_public_url"])
        return
    else:
        if(urlRePublicFull.search(url)):
            id = urlRePublicFull.search(url).group()

        elif(urlRePublic.search(url)):
            id = urlRePublic.search(url).group()

        elif(urlRePublicId.search(url)):
            id = urlRePublicId.search(url).group()

        else:
            update.message.reply_text(language.getLang(user.lang)["err_wrong_public_url"])
            return
    
    if(any(x["id"] == int(id) for x in user.vkGroups)):
        update.message.reply_text(language.getLang(user.lang)["err_already_exists_url"])
        return


    info = vkcore.get_group_info(id)
    if(info[0] == ''):
        update.message.reply_text(language.getLang(user.lang)["err_cant_find_url"])
        return

    user.vkGroups.append( { "name" : info[0], "id" : info[1] } )
    db.store_user(user)
    
    bot.send_message(
        chat_id = update.message.chat_id, 
        text = language.getLang(user.lang)["succ_added_new_url"].format(info[0], info[1]), 
        parse_mode = telegram.ParseMode.MARKDOWN)

def main():
    cfg = loadCfg()
    vkcore.init(cfg)

    updater = Updater(cfg.tg_token)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("subscribe", subscribe))
    dp.add_handler(CommandHandler("getgroups", getGroups))
    dp.add_error_handler(error)

    logger.log(logging.INFO, "Starting polling...")
    updater.start_polling()

    logger.log(logging.INFO, "Going to loop...")
    updater.idle()

if __name__ == '__main__':
    main()