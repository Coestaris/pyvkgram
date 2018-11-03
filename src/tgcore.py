#coding:utf-8

import time
import psutil
import re
import os
import telegram
from datetime import datetime
import random
import json
import traceback

import menuHandler
import dbUser
import vkcore
import posts
import db
import utils
import cfg
import language
import requests

startTime = time.time()

urlRePublicFull = re.compile(r"((?<=^https:\/\/vk\.com\/club)\d{4,})|((?<=^https:\/\/vk\.com\/public)\d{4,})$", re.MULTILINE)
urlRePublic = re.compile(r"(?<=^https:\/\/vk\.com\/)(.+)$", re.MULTILINE)
urlRePublicId = re.compile(r"^\d{4,}$", re.MULTILINE)
groupRe = re.compile(r"^\d{4,} - .+$")
bot = None

send_typing_action = utils.send_action(telegram.ChatAction.TYPING)
send_upload_video_action = utils.send_action(telegram.ChatAction.UPLOAD_VIDEO)
send_upload_photo_action = utils.send_action(telegram.ChatAction.UPLOAD_PHOTO)

def notify_admin(ex):
    print("Error: {}\nAdmin has been notifyed".format(ex))
    for admin in cfg.globalCfg.admins:
        bot.send_message(
            chat_id=admin,
            text="*Bot error!*\n\n_{}_\n\n{}".format(
                utils.escape_string(ex.__str__()), 
                utils.escape_string(traceback.format_exc())), 
            parse_mode = telegram.ParseMode.MARKDOWN)
    pass

def send_post(bot, grName, grId, lang, id, post):
    text = language.getLang(lang)["post_header"].format(
        grName, 
        grId, 
        datetime.fromtimestamp(post.date + 3600 * cfg.globalCfg.time_zone).strftime(cfg.globalCfg.time_format), 
        u'📌' if post.isPinned else ' ',
        u'💰' if post.isAd else ' ',
        u'➡️' if post.isForwarded else ' ',
        post.likeCount, 
        post.commentsCount, 
        post.repostsCount)
    
    if(post.text != ''):
        text += "\n\n" + post.escapeText()

    if(post.forwarded_text != ''):
        text += language.getLang(lang)["ori_post_text"].format(post.escapeFText())

    if(len(post.attachments) == 1 and post.attachments[0].type == posts.attachmentTypes.photo):
        
        bot.send_chat_action(chat_id=id, action=telegram.ChatAction.UPLOAD_PHOTO)
        bot.send_photo(chat_id = id, caption = text, parse_mode = telegram.ParseMode.MARKDOWN, photo = post.attachments[0].getUrl()['url'] )

    elif(len(post.attachments) == 1 and post.attachments[0].type == posts.attachmentTypes.video):

        if(post.attachments[0].isYouTube()):
            text += '\n' + post.attachments[0].getUrl()
            bot.send_message(chat_id = id, text = text, parse_mode = telegram.ParseMode.MARKDOWN)

        else:
            #TODO!
            text += language.getLang(lang)["post_video"].format(post.attachments[0].getUrl())
            bot.send_message(chat_id = id, text = text, parse_mode = telegram.ParseMode.MARKDOWN)
        #bot.send_chat_action(chat_id=id, action=telegram.ChatAction.UPLOAD_VIDEO)
        #bot.send_video(chat_id = id, caption = text, parse_mode = telegram.ParseMode.MARKDOWN, video = post.attachments[0].getUrl() )

    elif(len(post.attachments) == 1 and post.attachments[0].type == posts.attachmentTypes.doc):

        bot.send_chat_action(chat_id=id, action=telegram.ChatAction.UPLOAD_DOCUMENT)
        if(post.attachments[0].ext == 'gif'):
            bot.send_animation(chat_id = id, caption = text, parse_mode = telegram.ParseMode.MARKDOWN, animation = post.attachments[0].url, filename = post.attachments[0].title)
        else:
            bot.send_document(chat_id = id, caption = text, parse_mode = telegram.ParseMode.MARKDOWN, document = post.attachments[0].url, filename = post.attachments[0].title)
    else:

        if(len(post.attachments) != 0):
            for a in [x for x in post.attachments if x.type == posts.attachmentTypes.link]:
                text += "\n" + a.toMarkdown()

            media_group = []
            for a in [x for x in post.attachments if x.type == posts.attachmentTypes.photo]:
                media_group.append(telegram.InputMediaPhoto(a.getUrl()["url"]))
           
            for a in [x for x in post.attachments if x.type == posts.attachmentTypes.video]:
                if(a.isYouTube()):
                    text += '\n' + a.getUrl()

                else:                    
                    text += language.getLang(lang)["post_video"].format(a.getUrl())
                #media_group.append(telegram.InputMediaVideo(a.getUrl()))
           
            if(len(media_group) != 0):

                bot.send_chat_action(chat_id=id, action=telegram.ChatAction.UPLOAD_PHOTO)
                try:
                    bot.send_media_group(chat_id=id, media=media_group)
                except:
                    print('unable to send media group, trying to download files to disk...')

                    parentDir = os.path.dirname(os.path.realpath(__file__))
                    os.mkdir(u"{}/{}".format(parentDir, "download_data"))

                    counter = 0
                    for photoToDownload in [x.media for x in media_group]:
                        
                        r = requests.get(photoToDownload)
                        with open(u'{}/{}/tmp{}.jpg'.format(parentDir, "download_data", counter), 'wb') as f:  
                            f.write(r.content)
                            counter += 1
                        
                    counter = 0
                    nmedia_group = []
                    for photoToDownload in [x.media for x in media_group]:
                        nmedia_group.append(telegram.InputMediaPhoto(open(u'{}/{}/tmp{}.jpg'.format(parentDir, "download_data", counter))))
                        counter += 1

                    try:
                        bot.send_media_group(chat_id=id, media=nmedia_group)
                    except Exception as ex:
                        print(u'still cant send media group =c. {}'.format(ex.message))
            
            for a in [x for x in post.attachments if x.type == posts.attachmentTypes.doc]:

                bot.send_chat_action(chat_id=id, action=telegram.ChatAction.UPLOAD_DOCUMENT)
                if(a.ext == 'gif'):
                    bot.send_animation(chat_id = id, animation = a.url)
                else:
                    bot.send_document(chat_id = id, document = a.url, filename = a.title)

        bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
        bot.send_message(chat_id = id, text = text, parse_mode = telegram.ParseMode.MARKDOWN)
    pass

@send_typing_action
def start(bot, update):
    
    try:
        if(not db.has_user(update.message.chat_id)):
            db.store_user(dbUser.dbUser(teleid=update.message.chat_id, debugName=update.message.from_user.first_name))

        user = db.get_user(update.message.chat_id)
        update.message.reply_text(language.getLang(user.lang)["help"], reply_markup = { "remove_keyboard" : True })
    
    except Exception as ex:
        notify_admin(ex)

@send_typing_action
def help(bot, update):
    
    try:
        user = db.get_user(update.message.chat_id)
        update.message.reply_text(language.getLang(user.lang)["help"], reply_markup = { "remove_keyboard" : True })

    except Exception as ex:
        notify_admin(ex)

@send_typing_action
def settings(bot, update):

    try:
        user = db.get_user(update.message.chat_id)
        bot.send_message(chat_id=user.teleId, text="Выбирите кнопку из списка", reply_markup=menuHandler.get_main_menu(user, bot))
    
    except Exception as ex:
        notify_admin(ex)

def callback_inline(bot, update):

    try:
        query = update.callback_query

        user = db.get_user(query.message.chat_id)
        act = query.data

        markup = menuHandler.get_menu(act, user, bot)
        if(not isinstance(markup, telegram.InlineKeyboardMarkup)):
            bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        else:
            bot.edit_message_reply_markup(chat_id=query.message.chat_id, reply_markup = markup, message_id=query.message.message_id)

    except Exception as ex:
        notify_admin(ex)

def errorHandler(bot, update, error):
    print(error)
    try:
        user = db.get_user(update.message.chat_id)
        update.message.reply_text(language.getLang(user.lang)["server_error"], reply_markup = { "remove_keyboard" : True })
    
    except Exception as ex:
        notify_admin(ex)

@send_typing_action
def unsubscribe(bot, update):
    
    try:
        user = db.get_user(update.message.chat_id)
        if(len(user.vkGroups) == 0):
            update.message.reply_text(language.getLang(user.lang)["group_list_is_empty"], reply_markup = { "remove_keyboard" : True })
            return
        
        custom_keyboard = []
        for group in user.vkGroups:
            custom_keyboard.append([telegram.KeyboardButton(text=u"{} - {}".format(group["id"], group["name"]))])

        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
        update.message.reply_text(language.getLang(user.lang)["select_group"], reply_markup=reply_markup)
        user.currListening = 1
        db.store_user(user)
    
    except Exception as ex:
        notify_admin(ex)

@send_typing_action
def getPosts(bot, update):
    
    try:
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
            custom_keyboard.append([telegram.KeyboardButton(text=u"{} - {}".format(group["id"], group["name"]))])

        user.getPosts = { "count" : count, "offset" : offset }
        user.currListening = 2

        db.store_user(user)

        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
        update.message.reply_text(language.getLang(user.lang)["get_posts"].format(count), reply_markup=reply_markup)

    except Exception as ex:
        notify_admin(ex)

@send_typing_action
def textInputHandler(bot, update):

    try:
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
    
    except Exception as ex:
        notify_admin(ex)

@send_typing_action
def getGroups(bot, update):
    
    try:
        user = db.get_user(update.message.chat_id)
        if(len(user.vkGroups) == 0):
            update.message.reply_text(language.getLang(user.lang)["group_list_is_empty"], reply_markup = { "remove_keyboard" : True })
        else:
            text = language.getLang(user.lang)["group_list"] + '\n'
            for group in user.vkGroups:
                text += language.getLang(user.lang)["get_groups"].format(group["name"], group["id"])
            
            bot.send_message(
                chat_id = update.message.chat_id, 
                text = text, 
                parse_mode = telegram.ParseMode.MARKDOWN,
                reply_markup = { "remove_keyboard" : True })  
    except Exception as ex:
        notify_admin(ex)
        
@send_typing_action
def subscribe(bot, update):
    
    try:
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

    except Exception as ex:
        notify_admin(ex)


@send_typing_action
@utils.restricted
def adm_stat(bot, update):

    try:
        pid = os.getpid()
        py = psutil.Process(pid)
        memoryUse = py.memory_info()[0]/2.**30 

        bot.send_message(
            chat_id = update.message.chat_id, 
            text = u"*CPU*: {}_%_\n\n*FMem*: {}_GB_\n\n*Mem*: {}\n\n*Server uptime*: {}\n\n*Bot uptime*: {}"
                .format(psutil.cpu_percent(), memoryUse, psutil.virtual_memory(), 
                    utils.display_time(time.time() - psutil.boot_time(), 5), 
                    utils.display_time(time.time() - py.create_time(), 5)),
            parse_mode = telegram.ParseMode.MARKDOWN,
            reply_markup = { "remove_keyboard" : True })
    
    except Exception as ex:
        notify_admin(ex)

@send_typing_action
@utils.restricted
def adm_db_dump(bot, update):

    try:
        with open(db.dbFileName) as f:
            data = json.load(f)

            bot.send_message(
                chat_id = update.message.chat_id, 
                text = u"```json{{\n{}```".format(json.dumps(data, sort_keys=True, indent=2)),
                parse_mode = telegram.ParseMode.MARKDOWN,
                reply_markup = { "remove_keyboard" : True })
        
    except Exception as ex:
        notify_admin(ex)


@send_typing_action
@utils.restricted
def adm_db_drop(bot, update):

    try:
        os.remove(db.dbFileName)
        db.reassign_db()
        db.store_user(dbUser.dbUser(update.message.chat_id))

        bot.send_message(
            chat_id = update.message.chat_id, 
            text = "Database dropped",
            reply_markup = { "remove_keyboard" : True })

    except Exception as ex:
        notify_admin(ex)

lastUpdate = db.get_time()
if(lastUpdate == None):
    lastUpdate = time.time()
    db.store_time(lastUpdate)

def interval_func():

    updateStartTime = time.time()

    global lastUpdate
    totalPosts = 0
    postsRerecieved = 0
    postsSent = 0

    try:

        for user in db.get_users():
            for group in user.vkGroups:
            
                posts = vkcore.get_posts(group["id"], True, cfg.globalCfg.posts_to_get, 0)
                time.sleep(cfg.globalCfg.between_request_delay)

                while(posts[-1].date  >= lastUpdate):
                    postsRerecieved += cfg.globalCfg.posts_to_get
                    nposts = vkcore.get_posts(group["id"], True, cfg.globalCfg.posts_to_get, postsRerecieved)

                    #print [x.toDebugJSON() for x in nposts]
                    time.sleep(cfg.globalCfg.between_request_delay)
                    posts += nposts
                
                totalPosts += len(posts)

                postsToSend = []
                for post in posts:
                    if(post.date >= lastUpdate):
                        postsToSend.append(post)
                
                for post in postsToSend:
                    send_post(bot, group["name"], group["id"], user.lang, user.teleId, post)
                    postsSent += 1
    except Exception as ex:
        notify_admin(ex)

    lastUpdate = updateStartTime
    db.store_time(lastUpdate)

    print('Tick at {} ({}). Total: {}. PostRe: {}. Sent: {}'.format(
        datetime.utcfromtimestamp(lastUpdate).strftime(cfg.globalCfg.time_format), 
        lastUpdate,
        totalPosts,
        postsRerecieved,
        postsSent))
    pass
