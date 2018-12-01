#coding: utf-8

import telegram
import db
import random
import dbUser
import os
import language

def get_main_menu(user, bot):
    lang = language.getLang(user.lang)
    return telegram.InlineKeyboardMarkup([
        [telegram.InlineKeyboardButton(text=lang["menu_monitoring"].format(u'❌' if user.ignoreMonitoring else u'✅'), callback_data="btn_monitoring")],
        [telegram.InlineKeyboardButton(text=lang["menu_lang"], callback_data="btn_language")],
        [telegram.InlineKeyboardButton(text=lang["menu_postformat"], callback_data="btn_post_format")],
        [telegram.InlineKeyboardButton(text=lang["menu_close"], callback_data="btn_close")]
    ])

def get_menu(act, user, bot):
    lang = language.getLang(user.lang)

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
            [telegram.InlineKeyboardButton(text=lang["menu_lang_ru"].format(u'✅' if user.lang == "ru" else u' '), callback_data="btn_ru")],
            [telegram.InlineKeyboardButton(text=lang["menu_lang_en"].format(u'✅' if user.lang == "en" else u' '), callback_data="btn_en")],
            [telegram.InlineKeyboardButton(text=lang["menu_lang_back"], callback_data="btn_tomain")]
        ])
    
    if(act == "btn_monitoring"):
        user.ignoreMonitoring = not user.ignoreMonitoring
        db.store_user(user)
        return get_main_menu(user, bot)
    
    if(act in ["btn_post_format", "btn_post_id", "btn_post_date", "btn_post_likes", "btn_post_status" , "btn_post_link", "btn_autor"]):

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

        if(act == "btn_autor"):
            user.postFormat['show_autor'] = not user.postFormat['show_autor']
            db.store_user(user)

        if(act == "btn_post_link"):
            user.postFormat['show_link'] = not user.postFormat['show_link']
            db.store_user(user)

        return telegram.InlineKeyboardMarkup([
            [telegram.InlineKeyboardButton(text=lang["menu_format_id"].format(u'✅' if user.postFormat['show_id'] else u'❌'), callback_data="btn_post_id")],
            [telegram.InlineKeyboardButton(text=lang["menu_format_date"].format(u'✅' if user.postFormat['show_date'] else u'❌'), callback_data="btn_post_date")],
            [telegram.InlineKeyboardButton(text=lang["menu_format_likes"].format(u'✅' if user.postFormat['show_likes'] else u'❌'), callback_data="btn_post_likes")],
            [telegram.InlineKeyboardButton(text=lang["menu_format_status"].format(u'✅' if user.postFormat['show_status'] else u'❌'), callback_data="btn_post_status")],
            [telegram.InlineKeyboardButton(text=lang["menu_format_link"].format(u'✅' if user.postFormat['show_link'] else u'❌'), callback_data="btn_post_link")],
            [telegram.InlineKeyboardButton(text=lang["menu_format_autor"].format(u'✅' if user.postFormat['show_autor'] else u'❌'), callback_data="btn_autor")],
            [telegram.InlineKeyboardButton(text=lang["menu_format_close"], callback_data="btn_tomain")]
        ])

    if(act == "btn_close" or act == "adm_drop_cancel"):
        return {}

    if(act == "adm_drop"):
        os.remove(db.dbFileName)
        db.reassign_db()
        db.store_user(dbUser.dbUser(user.teleId))
        bot.send_message(chat_id = user.teleId, text = 'Database dropped!')
        return {}

def confirm_drop():
    array = []
    count = random.randint(3, 5)
    yes = random.randint(1, count) - 1
    for a in range(0, count):
        array.append([telegram.InlineKeyboardButton(text=u"%s" % "drop" if a == yes else "cancel",
            callback_data= ("adm_drop" if a == yes else "adm_drop_cancel"))])

    return telegram.InlineKeyboardMarkup(array)