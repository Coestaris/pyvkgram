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

            "dropped" : u"Database dropped!",
            "drop_confirm" : "Are you sure you want to drop database?",
            "drop_drop" : "Drop",
            "drop_cancel" : "Cancel",
            "dump_text" : u"Here's text dump for you...\n```json{{\n{}```",
            "dump_file" : u"Here's file dump for you...",
            "unhandled_error": "*Unhandled bot error!*\n\n_{}_\n\n{}{}",
            "unhandled_error_package": "\n\nAvailable data package: _{}_",
            "stat": 
                u"*CPU*: {}_%_\n\n*Mem*:\n_Total_: {}\n_Available_: {}\n_Free_: {}\n_Used_: {} ({}%)\n\n*Server uptime*: {}\n\n*Bot uptime*: {}" +
                u"\n\n*Posts Sent*: {}\n*Posts recieved*: {}\n*Posts reRecieved*: {}" +
                u"\n\n*Post attachments*: {}\n\n*VK Requests*: {}\n\n*Telegram calls*: {}",
            
            "stat_list_empty" : "list is empty",
            "stat_list_item" : u"  - *{}* : _{}_"
        }
    }
]

def getLang(l):
    global lang

    for a in lang:
        if(a["lang"] == l):
            return a["content"]

    raise ValueError("Unknown language")