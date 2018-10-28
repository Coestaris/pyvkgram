# coding=utf8

lang = [
    {
        "lang" : "ru",
        "content" : 
        {
            "help" : 

"""Бот для автоматического репоста постов с ВэКа вам в телегу. Для начала вам необходимо
подписаться на паблики, посты с которых вы хотите видеть в боте.\n
Комманды бота\nЮзай:\n
/subscribe [group-id or group-link] - чтобы включить мониторинг указанного паблика\n
/getGroups - чтобы получить список всех прослушиваеммых пабликов\n
/unsubscribe - чтобы выключить мониторинг паблика\n
/getPosts <optional: group-id or group-link> <optional: posts count> - чтобы получить последние посты паблика\n
/getWall <optional: posts count> - чтобы получить сквозной список постов со всех подписанных пабликов\n
/help - Чтобы вывести эту хелпу""",

            "err_unknown_id" : u"""️⛔️Группа с данным ID не числится в ваших группах""",
            "err_empty_public_url" : u"""️⛔️Пожалуйста, укажите URL-аддрес паблика или его ID""",
            "err_wrong_public_url" : u"""️⛔️Введенный URL имел неправильный формат, пожалуйста введите корректый аддрес/номер.""",
            "err_already_exists_url" : u"""⛔️Вы уже мониторите данную группу""",
            "err_cant_find_url" : u"""⛔️Не было найдено указанной группы в ВК.""",

            "succ_added_new_url" : u"""✅Группа "*{}*" (ID: {}) была добавлена в список ваших групп!""",
            "succ_removed_url" : u"""✅Группа "*{}*" (ID: {}) была удалена со списка ваших групп""",

            "select_group" : """Выберите, от какой группы вы желаете отписаться""",
            "group_list_is_empty" : """Cписок групп пуст""",
            "group_list" : """Вы мониторите следующие группы:""",
            "get_posts" : """Выберите, откуда желаете получить {} постов""",
            "getting_posts" : """Getting {} posts from *{}* (ID: {})""",


            "post_header" : u"Posted by *{}* (ID: {})\nat _{}_.\n❤️ {} | 💬 {} | 📢 {}"
        }
    }
]

def getLang(l):
    global lang

    for a in lang:
        if(a["lang"] == l):
            return a["content"]

    raise ValueError("Unknown language")