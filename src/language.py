# coding=utf8

lang = [
    {
        "lang" : "ru",
        "content" : 
        {
            "help" : 

u"""Бот для автоматического репоста постов с ВэКа вам в телегу. Для начала вам необходимо
подписаться на паблики, посты с которых вы хотите видеть в боте.\n
🤔Комманды бота🤔\nЮзай:\n
/subscribe [group-id or group-link] - чтобы включить мониторинг указанного паблика\n
/getGroups - чтобы получить список всех прослушиваеммых пабликов\n
/unsubscribe - чтобы выключить мониторинг паблика\n
/getPosts <optional: posts count> <optional: posts offset>  - чтобы получить последние посты паблика\n
/getWall <optional: posts count> - чтобы получить сквозной список постов со всех подписанных пабликов\n
/help - Чтобы вывести эту хелпу
/settings - Меню настроек

Обозначения в постах:
📌 - Пост закрепленный в группе
💰 - Пост помечен как рекламный
➡️ - Пост репост

❤️ - Количество лайков
💬 - Количество коментариев
📢️ - Количество репостов

Используй хэш-теги заголовках поста для быстрой навигации  между группами""",

            "ori_post_text" : u"""\n\n===Содержание оригинального поста===\n{}""",

            "err_unknown_id" : u"""️⛔️Группа с данным ID не числится в ваших группах""",
            "err_empty_public_url" : u"""️⛔️Пожалуйста, укажите URL-аддрес паблика или его ID""",
            "err_wrong_public_url" : u"""️⛔️Введенный URL имел неправильный формат, пожалуйста введите корректый аддрес/номер.""",
            "err_already_exists_url" : u"""⛔️Вы уже мониторите данную группу""",
            "err_cant_find_url" : u"""⛔️Не было найдено указанной группы в ВК.""",
            "err_not_allowed" : u"""️️⛔️Вас (UserID: {}) нету в списке тех, кому разрешено юзать эту функцию.""",

            "succ_added_new_url" : u"""✅Группа "*{}*" (ID: #g{}) была добавлена в список ваших групп!""",
            "succ_removed_url" : u"""✅Группа "*{}*" (ID: #g{}) была удалена со списка ваших групп""",

            "select_group" : u"""Выберите, от какой группы вы желаете отписаться""",
            "group_list_is_empty" : u"""Cписок групп пуст""",
            "group_list" : u"""Вы мониторите следующие группы:""",
            "get_posts" : u"""Выберите, откуда желаете получить {} постов""",
            "getting_posts" : u"""Отсылаю {} постов с *{}* (ID: #g{})""",
            "get_groups" : u"- *{}* (ID: #g{})\n",

            "post_video" : u"\n\n====Видео поста: [тыц сюда]({})(встроенное видео будет скоро...)===",

            "server_error" : u"Произошла серверная ошибка😢😢",
            "post_header" : u"Опубликовано \"*{}*\"",
            
            "post_header_id" : u" | (ID: #g{})",
            "post_header_likes" : u"❤️ {} | 💬 {} | 📢 {}",
            "post_header_at" : u"at _{}_",
            "post_header_status" : u" {}{}{}",
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
                u"Говорят, поступать на ФИВТ нужно, только если тебе слишком сложно на СФ",
            ],

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
            "menu_format_close" : "Назад"
        }
    }
]

def getLang(l):
    global lang

    for a in lang:
        if(a["lang"] == l):
            return a["content"]

    raise ValueError("Unknown language")