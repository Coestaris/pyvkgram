#coding: utf-8

import telegram
import db
import random
import dbUser
import os

def get_main_menu(user, bot):
    return telegram.InlineKeyboardMarkup([
        [telegram.InlineKeyboardButton(text=u"{} Мониторинг".format(u'❌' if user.ignoreMonitoring else u'✅'), callback_data="btn_monitoring")],
        [telegram.InlineKeyboardButton(text="Выбрать язык", callback_data="btn_language")],
        [telegram.InlineKeyboardButton(text="Формат поста", callback_data="btn_post_format")],
        [telegram.InlineKeyboardButton(text="Закрыть", callback_data="btn_close")]
    ])

def get_menu(act, user, bot):
    if(act == "btn_tomain"):
        return get_main_menu(user, bot)
    if(act in ["btn_language", "btn_ru", "btn_en"]):

        if(act == "btn_ru"): 
            user.lang = "ru"
            db.store_user(user)
        if(act == "btn_en"): 
            user.lang = "en"
            db.store_user(user)

        return telegram.InlineKeyboardMarkup([
            [telegram.InlineKeyboardButton(text= u"{} Русский🇷🇺".format(u'✅' if user.lang == "ru" else u' '), callback_data="btn_ru")],
            [telegram.InlineKeyboardButton(text= u"{} English🇺🇸".format(u'✅' if user.lang == "en" else u' '), callback_data="btn_en")],
            [telegram.InlineKeyboardButton(text="Назад", callback_data="btn_tomain")]
        ])
    
    if(act == "btn_monitoring"):
        user.ignoreMonitoring = not user.ignoreMonitoring
        db.store_user(user)
        return get_main_menu(user, bot)
    
    if(act in ["btn_post_format", "btn_post_id", "btn_post_date", "btn_post_likes", "btn_post_status" , "btn_post_link"]):

        if(act == "btn_post_id"):
            user.postFormat['show_id'] = not user.postFormat['show_id']
            db.store_user(user)

        if(act == "btn_post_date"):
            user.postFormat['show_date'] = not user.postFormat['show_date']
            db.store_user(user)

        if(act == "btn_post_likes"):
            user.postFormat['show_likes'] = not user.postFormat['show_likes']
            db.store_user(user)

        if(act == "btn_post_status"):
            user.postFormat['show_status'] = not user.postFormat['show_status']
            db.store_user(user)

        if(act == "btn_post_link"):
            user.postFormat['show_link'] = not user.postFormat['show_link']
            db.store_user(user)

        return telegram.InlineKeyboardMarkup([
            [
                telegram.InlineKeyboardButton(text=u"{}Отображать ID".format(u'✅' if user.postFormat['show_id'] else u'❌'), callback_data="btn_post_id"), 
                telegram.InlineKeyboardButton(text=u"{}Отображать дату".format(u'✅' if user.postFormat['show_date'] else u'❌'), callback_data="btn_post_date")
            ],
            [telegram.InlineKeyboardButton(text=u"{}Отображать строку с лайками".format(u'✅' if user.postFormat['show_likes'] else u'❌'), callback_data="btn_post_likes")],
            [telegram.InlineKeyboardButton(text=u"{}Отображать статусную строку".format(u'✅' if user.postFormat['show_status'] else u'❌'), callback_data="btn_post_status")],
            [telegram.InlineKeyboardButton(text=u"{}Отображать ссылку на по в ВК".format(u'✅' if user.postFormat['show_link'] else u'❌'), callback_data="btn_post_link")],
            [telegram.InlineKeyboardButton(text="Назад", callback_data="btn_tomain")]
        ])

    if(act == "btn_close" or act == "adm_drop_cancel"):
        return {}

    if(act == "adm_drop"):
        os.remove(db.dbFileName)
        db.reassign_db()
        db.store_user(dbUser.dbUser(user.teleId))
        return {}

def confirm_drop():
    array = []
    count = random.randint(3, 5)
    yes = random.randint(1, count) - 1
    for a in range(0, count):
        array.append([telegram.InlineKeyboardButton(text=u"%s" % "drop" if a == yes else "cancel",
            callback_data= ("adm_drop" if a == yes else "adm_drop_cancel"))])

    return telegram.InlineKeyboardMarkup(array)