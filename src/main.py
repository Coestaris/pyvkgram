import json
import logging
import random
import re
from datetime import datetime

import telegram
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

import cfg
import db
import dbUser
import language
import vkcore
from posts import attachmentTypes
import utils

urlRePublicFull = re.compile(r"((?<=^https:\/\/vk\.com\/club)\d{4,})|((?<=^https:\/\/vk\.com\/public)\d{4,})$", re.MULTILINE)
urlRePublic = re.compile(r"(?<=^https:\/\/vk\.com\/)(.+)$", re.MULTILINE)
urlRePublicId = re.compile(r"^\d{4,}$", re.MULTILINE)
groupRe = re.compile(r"^\d{4,} - .+$")

send_typing_action = utils.send_action(telegram.ChatAction.TYPING)
send_upload_video_action = utils.send_action(telegram.ChatAction.UPLOAD_VIDEO)
send_upload_photo_action = utils.send_action(telegram.ChatAction.UPLOAD_PHOTO)

def send_post(bot, grName, grId, lang, id, post):
    text = language.getLang(lang)["post_header"].format(grName, grId, datetime.utcfromtimestamp(post.date).strftime(cfg.globalCfg.time_format), post.likeCount, post.commentsCount, post.repostsCount)
    
    if(post.text != ''):
        text += "\n\n" + post.escapeText()

    if(len(post.attachments) == 1 and post.attachments[0].type == attachmentTypes.photo):
        
        bot.send_chat_action(chat_id=id, action=telegram.ChatAction.UPLOAD_PHOTO)
        bot.send_photo(chat_id = id, caption = text, parse_mode = telegram.ParseMode.MARKDOWN, photo = post.attachments[0].getUrl()['url'] )

    elif(len(post.attachments) == 1 and post.attachments[0].type == attachmentTypes.video):

        bot.send_chat_action(chat_id=id, action=telegram.ChatAction.UPLOAD_VIDEO)
        bot.send_video(chat_id = id, caption = text, parse_mode = telegram.ParseMode.MARKDOWN, video = post.attachments[0].getUrl() )

    elif(len(post.attachments) == 1 and post.attachments[0].type == attachmentTypes.doc):

        bot.send_chat_action(chat_id=id, action=telegram.ChatAction.UPLOAD_DOCUMENT)
        bot.send_document(chat_id = id, caption = text, parse_mode = telegram.ParseMode.MARKDOWN, document = post.attachments[0].url, filename = post.attachments[0].title)
    else:

        if(len(post.attachments) != 0):
            for a in [x for x in post.attachments if x.type == attachmentTypes.link]:
                text += "\n" + a.toMarkdown()

            media_group = []
            for a in [x for x in post.attachments if x.type == attachmentTypes.photo]:
                media_group.append(telegram.InputMediaPhoto(a.getUrl()["url"]))
           
            for a in [x for x in post.attachments if x.type == attachmentTypes.video]:
                media_group.append(telegram.InputMediaVideo(a.getUrl()))
           
            if(len(media_group) != 0):

                bot.send_chat_action(chat_id=id, action=telegram.ChatAction.UPLOAD_PHOTO)
                bot.send_media_group(chat_id = id, media = media_group)
            
            for a in [x for x in post.attachments if x.type == attachmentTypes.doc]:

                bot.send_chat_action(chat_id=id, action=telegram.ChatAction.UPLOAD_DOCUMENT)
                bot.send_document(chat_id = id, document = a.url, filename = a.title)

        bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
        bot.send_message(chat_id = id, text = text, parse_mode = telegram.ParseMode.MARKDOWN)
    pass

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
    user = db.get_user(update.message.chat_id)
    update.message.reply_text(language.getLang(user.lang)["server_error"], reply_markup = { "remove_keyboard" : True })

@send_typing_action
def unsubscribe(bot, update):
    user = db.get_user(update.message.chat_id)
    
    if(len(user.vkGroups) == 0):
        update.message.reply_text(language.getLang(user.lang)["group_list_is_empty"], reply_markup = { "remove_keyboard" : True })
        return
    
    custom_keyboard = []
    for group in user.vkGroups:
        custom_keyboard.append([telegram.KeyboardButton(text="{} - {}".format(group["id"], group["name"]))])

    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    update.message.reply_text(language.getLang(user.lang)["select_group"], reply_markup=reply_markup)
    user.currListening = 1
    db.store_user(user)
    pass

@send_typing_action
def getPosts(bot, update):
    user = db.get_user(update.message.chat_id)
    
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
        custom_keyboard.append([telegram.KeyboardButton(text="{} - {}".format(group["id"], group["name"]))])

    user.getPosts = { "count" : count, "offset" : offset }
    user.currListening = 2

    db.store_user(user)

    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    update.message.reply_text(language.getLang(user.lang)["get_posts"].format(count), reply_markup=reply_markup)

    pass

@send_typing_action
def textInput(bot, update):
    user = db.get_user(update.message.chat_id)

    if(groupRe.search(update.message.text)):

        id = int(update.message.text.split('-')[0].strip())
        name = update.message.text.split('-')[1].strip()
        
        if(any(x["id"] == id for x in user.vkGroups)):
            
            if(user.currListening == 1):
                
                user.vkGroups = [x for x in user.vkGroups if x["id"] != id]
                db.store_user(user)
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
                for post in posts:
                    send_post(bot, name, id, user.lang, user.teleId, post)
            else:
                update.message.reply_text(random.choice(language.getLang(user.lang)["group_text_reply"]), reply_markup = { "remove_keyboard" : True })

        else:
            update.message.reply_text(language.getLang(user.lang)["err_unknown_id"], reply_markup = { "remove_keyboard" : True })
            return

        user.currListening = 0
        db.store_user(user)

    else:
        update.message.reply_text(random.choice(language.getLang(user.lang)["text_reply"]), reply_markup = { "remove_keyboard" : True })
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
    
    info = vkcore.get_group_info(id)

    if(info[0] == ''):
        update.message.reply_text(language.getLang(user.lang)["err_cant_find_url"], reply_markup = { "remove_keyboard" : True })
        return
    
    if(any(x["id"] == info[1] for x in user.vkGroups)):
        update.message.reply_text(language.getLang(user.lang)["err_already_exists_url"], reply_markup = { "remove_keyboard" : True })
        return

    user.vkGroups.append( { "name" : info[0], "id" : info[1] } )
    db.store_user(user)
    
    bot.send_message(
        chat_id = update.message.chat_id, 
        text = language.getLang(user.lang)["succ_added_new_url"].format(info[0], info[1]), 
        parse_mode = telegram.ParseMode.MARKDOWN,
        reply_markup = { "remove_keyboard" : True })


@send_typing_action
@utils.restricted
def adm_db_dump(bot, update):
    with open('db.json') as f:
        data = json.load(f)

        bot.send_message(
            chat_id = update.message.chat_id, 
            text = "```json{{\n{}```".format(json.dumps(data, sort_keys=True, indent=2)),
            parse_mode = telegram.ParseMode.MARKDOWN,
            reply_markup = { "remove_keyboard" : True })
    pass

def interval_func():
    
    pass

def main():
    
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.log(logging.INFO, "Loading configs...")
    cfg.globalCfg = utils.loadCfg()
    utils.LIST_OF_ADMINS = cfg.globalCfg.admins

    logger.log(logging.INFO, "Init vkcore...")
    vkcore.init(cfg.globalCfg)

    logger.log(logging.INFO, "Init tgcore...")
    updater = Updater(cfg.globalCfg.tg_token)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("subscribe", subscribe))
    dp.add_handler(CommandHandler("unsubscribe", unsubscribe))
    dp.add_handler(CommandHandler("getgroups", getGroups))
    dp.add_handler(CommandHandler("getposts", getPosts))
    
    #dp.add_handler(CommandHandler("adm_restart", getPosts))
    dp.add_handler(CommandHandler("adm_db_dump", adm_db_dump))
    #dp.add_handler(CommandHandler("adm_db_clear", getPosts))    
    #dp.add_handler(CommandHandler("adm_stat", getPosts))

    dp.add_handler(MessageHandler(Filters.text, textInput))
    dp.add_error_handler(error)

    logger.log(logging.INFO, "Starting polling...")
    updater.start_polling()

    logger.log(logging.INFO, "Starting interval_func...")
    utils.set_interval(interval_func, cfg.globalCfg.timer_tick)

    logger.log(logging.INFO, "Going to loop...")
    updater.idle()


if __name__ == '__main__':
    main()
