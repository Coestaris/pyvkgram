#coding: utf-8

import os
import time
import traceback
from datetime import datetime

import requests
import telegram

import cfg
import db
import language
import tgcore
import utils
import vkcore

def getText(grName, grId, id, post, lang):
    text = language.getLang(lang)["post_header"].format()    
    pass

def send_post(bot, grName, grId, lang, id, post):
    maxCaptionLength = 200

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
        if(len(text) <= maxCaptionLength):
            bot.send_photo(chat_id = id, caption = text, parse_mode = telegram.ParseMode.MARKDOWN, photo = post.attachments[0].getUrl()['url'] )
        else:
            bot.send_photo(chat_id = id, photo = post.attachments[0].getUrl()['url'] )
            bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
            bot.send_message(chat_id = id, text = text, parse_mode = telegram.ParseMode.MARKDOWN)


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
        if(len(text) <= maxCaptionLength):
            bot.send_document(chat_id = id, caption = text, parse_mode = telegram.ParseMode.MARKDOWN, document = post.attachments[0].url, filename = post.attachments[0].title)
        else:
            bot.send_document(chat_id = id, document = post.attachments[0].url, filename = post.attachments[0].title)
            bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
            bot.send_message(chat_id = id, text = text, parse_mode = telegram.ParseMode.MARKDOWN)

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


def notify_admin(ex):
    print("Error: {}\nAdmin has been notifyed".format(ex))
    for admin in cfg.globalCfg.admins:
        tgcore.bot.send_message(
            chat_id=admin,
            text="*Bot error!*\n\n_{}_\n\n{}".format(
                utils.escape_string(ex.__str__()), 
                utils.escape_string(traceback.format_exc())), 
            parse_mode = telegram.ParseMode.MARKDOWN)
    pass


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
                    send_post(tgcore.bot, group["name"], group["id"], user.lang, user.teleId, post)
                    postsSent += 1
    except Exception as ex:
        notify_admin(ex)

    lastUpdate = updateStartTime
    db.store_time(lastUpdate)
    pass
