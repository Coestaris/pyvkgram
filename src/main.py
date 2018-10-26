from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import json
import dbUser

import re
import db
import language
import cfg
import vkcore

urlRePublicFull = re.compile(r"((?<=^https:\/\/vk\.com\/club)\d{4,})|((?<=^https:\/\/vk\.com\/public)\d{4,})$")
urlRePublic = re.compile(r"(?<=^https:\/\/vk\.com\/)(.+)$")
urlRePublicId = re.compile(r"^\d{4,}$")

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
        update.message.reply_text("new one!")
        db.store_user(dbUser.dbUser(update.message.chat_id))

    user = db.get_user(update.message.chat_id)
    update.message.reply_text(language.getLang(user.lang)["help"])

def help(bot, update):
    user = db.get_user(update.message.chat_id)
    update.message.reply_text(language.getLang(user.lang)["help"])

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

def subscribe(bot, update):
    user = db.get_user(update.message.chat_id)
    url = update.message.text.replace("/subscribe", "").strip()
    
    if(url == ""):
        update.message.reply_text(language.getLang(user.lang)["err_empty_public_url"])
    else:
        if(urlRePublic.search(url)):
            id = urlRePublic.match(url)
            print(id)

        elif(urlRePublicFull.search(url)):
            id = urlRePublicFull.match(url).string
            print("full " + id)
        elif(urlRePublicId.search(url)):
            id = urlRePublicId.match(url).string
            print("id " + id)
        else:
            print("wrong format")

def main():
    cfg = loadCfg()
    vkcore.init(cfg)

    updater = Updater(cfg.tg_token)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("subscribe", subscribe))
    dp.add_error_handler(error)

    logger.log(logging.INFO, "Starting polling...")
    updater.start_polling()

    logger.log(logging.INFO, "Going to loop...")
    updater.idle()

if __name__ == '__main__':
    main()