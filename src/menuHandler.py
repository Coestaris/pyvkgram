#coding: utf-8

import telegram
import db

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
            [telegram.InlineKeyboardButton(text= u"{} Русский🇷🇺".format(u'✅' if user.lang == "ru" else u'❌'), callback_data="btn_ru")],
            [telegram.InlineKeyboardButton(text= u"{} English🇺🇸".format(u'✅' if user.lang == "en" else u'❌'), callback_data="btn_en")],
            [telegram.InlineKeyboardButton(text="Назад", callback_data="btn_tomain")]
        ])
    
    if(act == "btn_monitoring"):
        user.ignoreMonitoring = not user.ignoreMonitoring
        db.store_user(user)
        return get_main_menu(user, bot)
    
    if(act in ["btn_post_format", "btn_post_id", "btn_post_date", "btn_post_likes", "btn_post_status"]):

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

        return telegram.InlineKeyboardMarkup([
            [
                telegram.InlineKeyboardButton(text=u"{}Отображать ID".format(u'✅' if user.postFormat['show_id'] else u'❌'), callback_data="btn_post_id"), 
                telegram.InlineKeyboardButton(text=u"{}Отображать дату".format(u'✅' if user.postFormat['show_date'] else u'❌'), callback_data="btn_post_date")
            ],
            [telegram.InlineKeyboardButton(text=u"{}Отображать строку с лайками".format(u'✅' if user.postFormat['show_likes'] else u'❌'), callback_data="btn_post_likes")],
            [telegram.InlineKeyboardButton(text=u"{}Отображать статусную строку".format(u'✅' if user.postFormat['show_status'] else u'❌'), callback_data="btn_post_likes")],
            [telegram.InlineKeyboardButton(text="Назад", callback_data="btn_tomain")]
        ])

    if(act == "btn_close"):
        return {}