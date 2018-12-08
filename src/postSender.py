#coding: utf-8

import os
import time
import traceback
from datetime import datetime
import shutil

import requests
import telegram

import cfg
import db
import language
import tgcore
import utils
from posts import attachmentTypes 
import vkcore

def getText(grName, grId, post, user):
    lang = language.getLang(user.lang)

    text = u""
    if(user.postFormat["show_autor"]):
        text += lang["post_header"].format(utils.escape_string(grName, True))
        if(user.postFormat["show_id"]): text += lang["post_header_id"].format(grId)
        if(user.postFormat["show_link"]): text += lang["post_header_link"].format(grId, post.id)

    if(user.postFormat["show_date"]):
        text += lang["post_header_at"].format(datetime.fromtimestamp(post.date + 3600 * cfg.globalCfg.time_zone).strftime(cfg.globalCfg.time_format))
    
    if(user.postFormat["show_likes"]):
        text += lang["post_header_likes"].format(
            post.likeCount, 
            post.commentsCount, 
            post.repostsCount)

    if(user.postFormat["show_status"]):
        text += lang["post_header_status"].format(
            u'📌' if post.isPinned else ' ',
            u'💰' if post.isAd else ' ',
            u'➡️' if post.isForwarded else ' ')

    if(post.text != ''):
        text += u"\n\n" + utils.makeVKLinks(post.escapeText())

    if(post.forwarded_text != ''):
        text += lang["ori_post_text"].format(utils.makeVKLinks(post.escapeFText()))

    return text

def send_post(bot, grName, grId, post, user):
    try:
        maxCaptionLength = 200
        text = getText(grName, grId, post, user)
        id = user.teleId

        if(len(post.attachments) == 1 and post.attachments[0].type == attachmentTypes.photo):
            utils.incAttachments("photo", 1)
            
            bot.send_chat_action(chat_id= id, action=telegram.ChatAction.UPLOAD_PHOTO)
            if(len(text) <= maxCaptionLength):
                bot.send_photo(
                    chat_id = id, 
                    caption = text, 
                    parse_mode = telegram.ParseMode.MARKDOWN, 
                    photo = post.attachments[0].getUrl()['url'],
                    timeout=cfg.globalCfg.sendFileTimeout)

            else:
                bot.send_photo(
                    chat_id = id, 
                    photo = post.attachments[0].getUrl()['url'], 
                    timeout=cfg.globalCfg.sendFileTimeout)
                bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
                bot.send_message(chat_id = id, text = text, parse_mode = telegram.ParseMode.MARKDOWN)

        elif(len(post.attachments) == 1 and post.attachments[0].type == attachmentTypes.video):
            utils.incAttachments("video", 1)

            if(post.attachments[0].isYouTube()):
                text += u'\n' + post.attachments[0].getUrl()
                bot.send_message(chat_id = id, text = text, parse_mode = telegram.ParseMode.MARKDOWN)

            else:
                #TODO!
                text += language.getLang(user.lang)["post_video"].format(post.attachments[0].getUrl())
                bot.send_message(chat_id = id, text = text, parse_mode = telegram.ParseMode.MARKDOWN)

                #bot.send_chat_action(chat_id=id, action=telegram.ChatAction.UPLOAD_VIDEO)
                #bot.send_video(chat_id = id, caption = text, parse_mode = telegram.ParseMode.MARKDOWN, video = post.attachments[0].getUrl() )

        elif(len(post.attachments) == 1 and post.attachments[0].type == attachmentTypes.doc):
            utils.incAttachments("doc", 1)

            bot.send_chat_action(chat_id=id, action=telegram.ChatAction.UPLOAD_DOCUMENT)
            if(len(text) <= maxCaptionLength):
                bot.send_document(
                    chat_id = id, 
                    caption = text, 
                    parse_mode = telegram.ParseMode.MARKDOWN, 
                    document = post.attachments[0].url, 
                    filename = post.attachments[0].title,
                    timeout=cfg.globalCfg.sendFileTimeout)

            else:
                bot.send_document(
                    chat_id = id, 
                    document = post.attachments[0].url, 
                    filename = post.attachments[0].title,
                    timeout=cfg.globalCfg.sendFileTimeout)

                bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
                bot.send_message(chat_id = id, text = text, parse_mode = telegram.ParseMode.MARKDOWN)

        else:
            
            if(len(post.attachments) != 0):
                for a in [x for x in post.attachments if x.type == attachmentTypes.link]:
                    text += "\n" + a.toMarkdown()
                    utils.incAttachments("link", 1)

                media_group = []
                for a in [x for x in post.attachments if x.type == attachmentTypes.photo]:
                    media_group.append(telegram.InputMediaPhoto(a.getUrl()["url"]))
                    utils.incAttachments("photo", 1)

                for a in [x for x in post.attachments if x.type == attachmentTypes.video]:
                    utils.incAttachments("video", 1)
                    if(a.isYouTube()):
                        text += '\n' + a.getUrl()

                    else:                    
                        text += language.getLang(user.lang)["post_video"].format(a.getUrl())
                    #media_group.append(telegram.InputMediaVideo(a.getUrl()))
            
                if(len(media_group) != 0):
                    utils.incAttachments("photo", len(media_group))

                    bot.send_chat_action(chat_id=id, action=telegram.ChatAction.UPLOAD_PHOTO)
                    try:
                        bot.send_media_group(
                            chat_id=id, 
                            media=media_group,
                            timeout=cfg.globalCfg.sendFileTimeout)

                    except:
                        print('unable to send media group, trying to download files to disk...')

                        parentDir = os.path.dirname(os.path.realpath(__file__))
                        
                        dirName = u"{}/{}".format(parentDir, "download_data") 
                        
                        shutil.rmtree(dirName)
                        os.mkdir(dirName)

                        counter = 0
                        for photoToDownload in [x.media for x in media_group]:
                            
                            r = requests.get(photoToDownload)
                            with open(u'{}/tmp{}.jpg'.format(dirName, counter), 'wb') as f:  
                                f.write(r.content)
                                counter += 1
                            
                        counter = 0
                        nmedia_group = []
                        for photoToDownload in [x.media for x in media_group]:
                            nmedia_group.append(telegram.InputMediaPhoto(open(u'{}/tmp{}.jpg'.format(dirName, counter))))
                            counter += 1

                        try:
                            bot.send_media_group(
                                chat_id=id, 
                                media=nmedia_group,
                                timeout=cfg.globalCfg.sendFileTimeout)

                        except Exception as ex:
                            print(u'still cant send media group =c. {}'.format(ex.message))
                
                for a in [x for x in post.attachments if x.type == attachmentTypes.doc]:
                    utils.incAttachments("doc", 1)
                    
                    bot.send_chat_action(chat_id=id, action=telegram.ChatAction.UPLOAD_DOCUMENT)
                    if(a.ext == 'gif'):
                        bot.send_animation(
                            chat_id = id, 
                            animation = a.url,
                            timeout=cfg.globalCfg.sendFileTimeout)

                    else:
                        bot.send_document(
                            chat_id = id, 
                            document = a.url, 
                            filename = a.title,
                            timeout=cfg.globalCfg.sendFileTimeout)

            bot.send_chat_action(chat_id=id, action=telegram.ChatAction.TYPING)
            bot.send_message(chat_id = id, text = text, parse_mode = telegram.ParseMode.MARKDOWN)
            
    except telegram.utils.request.TimedOut:
        print "Timeout =c"

    pass
 
def notify_admin_message(error):
    utils.incStatTG("_error_notified")

    print("Error: {}\nAdmin has been notified".format(error))
    for admin in cfg.globalCfg.admins:
        tgcore.bot.send_message(
            chat_id=admin,
            text="*Unhandled bot error (message type)!*\n\n{}".format(
                utils.escape_string(error, False, False)), 
            parse_mode = telegram.ParseMode.MARKDOWN)
    pass

def notify_admin(ex):
    utils.incStatTG("_error_notified")
    
    print("Error: {}\nAdmin has been notified".format(ex))
    for admin in cfg.globalCfg.admins:
        tgcore.bot.send_message(
            chat_id=admin,
            text="*Unhandled bot error!*\n\n_{}_\n\n{}".format(
                utils.escape_string(ex.__str__(), False, True), 
                utils.escape_string(traceback.format_exc(), False, False)), 
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

                if(len(posts) == 0):
                    continue

                while(posts[-1].date  >= lastUpdate):
                    nposts = vkcore.get_posts(group["id"], True, cfg.globalCfg.posts_to_get, postsRerecieved)
                    postsRerecieved += len(nposts)

                    #print [x.toDebugJSON() for x in nposts]
                    time.sleep(cfg.globalCfg.between_request_delay)
                    posts += nposts
                
                totalPosts += len(posts)

                postsToSend = []
                for post in posts:
                    if(post.date >= lastUpdate):
                        postsToSend.append(post)
                
                for post in postsToSend:
                    send_post(tgcore.bot, group["name"], group["id"], post, user)
                    postsSent += 1
    except Exception as ex:
        notify_admin(ex)

    cfg.globalStat.postRecieved += totalPosts
    cfg.globalStat.postSent += postsSent
    cfg.globalStat.forcedRequests += postsRerecieved

    lastUpdate = updateStartTime
    db.store_time(lastUpdate)
    db.store_stat(cfg.globalStat)
    pass
