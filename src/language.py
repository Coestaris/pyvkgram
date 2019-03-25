# coding=utf8

lang = [
    {
        "lang" : "ru",
        "content" : 
        {
            "help" : 

u"""Бот для автоматического репоста постов с ВэКа вам в телегу. Для начала вам необходимо подписаться на паблики, посты с которых вы хотите видеть в боте.

🤔Комманды бота🤔
Юзай:

/subscribe [айди-группы или ссылка на группу в ВК] - чтобы включить мониторинг указанного паблика

/getGroups - чтобы получить список всех прослушиваеммых пабликов

/unsubscribe - чтобы выключить мониторинг паблика

/getPosts [(опционально) количество постов] [(опционально) сдвиг постов]  - чтобы получить последние посты паблика

/help - Чтобы вывести эту хелпу

/settings - Меню настроек

Обозначения в постах:
📌 - Пост закрепленный в группе
💰 - Пост помечен как рекламный
➡️ - Пост переслан с другой страницы (группы или юзера)
❤️ - Количество лайков
💬 - Количество коментариев
📢️ - Количество репостов

Используй хэш-теги заголовках поста для быстрой навигации  между группами.
На данный момент поддерживается: изображения, гифки, документы, видео. Все остальное, возможно, когда-то...

Изменить формат поста (влючить отображение времени поста, строки с лайками и тд.) можно в меню настроек.

По всем вопросам, предложениям и багтреку: @coestaris """,

            "forwaded_from" : u"\n\n_Переслано от _\"*{}*\"",
            "ori_post_text" : u"_, текст оригинального поста:_\n\n{}",
            "name_format" : u"(польз.) {} {}",

            "err_unknown_id" : u"️⛔️Группа с данным ID не числится в ваших группах",
            "err_empty_public_url" : u"️⛔️Пожалуйста, укажите URL-аддрес паблика или его ID",
            "err_wrong_public_url" : u"️⛔️Введенный URL имел неправильный формат, пожалуйста введите корректый аддрес/номер.",
            "err_already_exists_url" : u"⛔️Вы уже мониторите данную группу",
            "err_cant_find_url" : u"⛔️Не было найдено указанной группы в ВК.",
            "err_not_allowed" : u"️️⛔️Вас (UserID: {}) нету в списке тех, кому разрешено юзать эту функцию.",

            "succ_added_new_url" : u"✅Группа \"*{}*\" (ID: #g{}) была добавлена в список ваших групп!",
            "succ_removed_url" : u"✅Группа \"*{}*\" (ID: #g{}) была удалена со списка ваших групп",

            "select_group" : u"Выберите, от какой группы вы желаете отписаться",
            "group_list_is_empty" : u"Cписок групп пуст",
            "group_list" : u"Вы мониторите следующие группы:",
            "get_posts" : u"Выберите, откуда желаете получить {} постов",
            "getting_posts" : u"Отсылаю {} постов с *{}* (ID: #g{})",
            "get_groups" : u"- *{}* (ID: #g{})\n",

            "post_video" : u"""\nВидео: "*{}*"\[_{}_] - [ссылка]({})""",

            "server_error" : u"Произошла серверная ошибка😢😢",
            "post_header" : u"By \"*{}*\"",
            
            "post_header_id" : u" | (ID: #g{})",
            "post_header_likes" : u"\n❤️ {} | 💬 {} | 📢 {}",
            "post_header_at" : u"\nat _{}_",
            "post_header_status" : u"\n{}{}{}",
            "post_header_link" : u" | ([ссылка](https://vk.com/wall-{}_{}))",

            "group_text_reply" : [ 
                u"И зачем ты мне прислал эту группу?", 
                u"Для постов юзай /getPosts", 
                u"Хз что мне делать с этой группой" 
            ],

            "text_reply" : [ 
                u"И что мне с этим делать?", 
                u"Юзай /help чтобы получить список команд", 
                u"Без понятия что ты от меня хочешь", 
                u"Прикольно, но что дальше?",
                u"Как хорошо, что я не Игорь",
                u"Говорят, поступать на ФИВТ нужно, только если тебе слишком сложно на СФ"
            ],

            "menu": u"Выберите кнопку из списка",
            "menu_monitoring" : u"{} Мониторинг",
            "menu_lang" : u"Выбрать язык",
            "menu_postformat" : u"Формат поста",
            "menu_close" : u"Закрыть",

            "menu_lang_ru" : u"{} Русский🇷🇺",
            "menu_lang_en" : u"{} English🇺🇸",
            "menu_lang_back" : "Назад",

            "menu_format_id" : u"{}Отображать ID",
            "menu_format_date" : u"{}Отображать дату",
            "menu_format_likes" : u"{}Отображать строку с лайками",
            "menu_format_status" : u"{}Отображать статусную строку",
            "menu_format_link" : u"{}Отображать ссылку на пост в ВК",
            "menu_format_autor" : u"{}Отображать автора поста",
            "menu_format_close" : "Назад",

            "dropped" : u"База данных сброшена!",
            "drop_confirm" : u"Вы дейтсвительно желаете сбросить всю БДху?",
            "drop_drop" : u"Сбросить",
            "drop_cancel" : u"Отмена",
            "dump_text" : u"Вот тебе текстовый дамп, любимый...\n```json{{\n{}```",
            "dump_file" : u"Вот тебе файловый дамп, любимый...",
            "unhandled_error": u"*Непредусмотренная ошибка!*\n\n_{}_\n\n{}{}",
            "unhandled_error_package": u"\n\nДоступные данные: _{}_",
            "stat": 
                u"*CPU*: {}_%_\n\n*Память*:\n_Общее_: {}\n_Доступно_: {}\n_Свободно_: {}\n_Использовано_: {} ({}%)\n\n*Ап-тайм сервера*: {}\n\n*Ап-тайм бота*: {}" +
                u"\n\n*Отправлeно постов*: {}\n*Постов обработано*: {}\n*Повторных запросов постов*: {}" +
                u"\n\n*Вложения постов*: {}\n\n*VK Запросы*: {}\n\n*Telegram запросы*: {}",
            
            "stat_list_empty" : u"Список пуст",
            "stat_list_item" : u"  - *{}* : _{}_"
        }
    }
]

months_dict_ru =  [u"месяц",   u"месяца",  u"месяцев"]
weeks_dict_ru =   [u"неделя",  u"недели",  u"недель"]
days_dict_ru =    [u"день",    u"дня",     u"дней"]
hours_dict_ru =   [u"час",     u"часа",    u"часов"]
minutes_dict_ru = [u"минута",  u"минуты",  u"минут"]
seconds_dict_ru = [u"секунда", u"секунды", u"секунд"]

dict_en = [ "month", "week", "day", "hour", "minute", "second" ]

def date_make_rus(value, dict, i):
    ld = value % 10
    if(ld == 1): return dict[0]
    elif(ld == 2 or ld == 3 or ld == 4): return dict[1]
    else: return dict[2]

def date_make_en(value, dict, i):
    if(value == 1): return dict[i]
    else: return dict[i] + u's'

def make_date(value, dict, lang, i):
    if(lang == 'ru'): return date_make_rus(value, dict, i)
    elif(lang == 'en'): return date_make_en(value, dict, i)
    else: pass 

intervals = (
    ( 1, { 'ru' : months_dict_ru,  'en' : dict_en }, 2419200), # 60 * 60 * 24 * 7 * 4
    ( 2, { 'ru' : weeks_dict_ru,   'en' : dict_en }, 604800),  # 60 * 60 * 24 * 7
    ( 3, { 'ru' : days_dict_ru,    'en' : dict_en }, 86400),   # 60 * 60 * 24
    ( 4, { 'ru' : hours_dict_ru,   'en' : dict_en }, 3600),    # 60 * 60
    ( 5, { 'ru' : minutes_dict_ru, 'en' : dict_en }, 60),      # 60
    ( 6, { 'ru' : seconds_dict_ru, 'en' : dict_en }, 1),       # 1
)

def display_time(seconds, lang, granularity=2):
    result = []
    for index, dict, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            result.append(u"{0:.0f} {1}".format(value, make_date(value, dict[lang], lang, index)))
    return u', '.join(result[:granularity])

def getLang(l):
    global lang

    for a in lang:
        if(a["lang"] == l):
            return a["content"]

    raise ValueError("Unknown language")