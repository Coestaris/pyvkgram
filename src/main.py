import logging

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

import cfg
import language
import vkcore
import tgcore
import utils

def main():
    
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.log(logging.INFO, "Loading configs...")
    cfg.globalCfg = utils.loadCfg()
    utils.LIST_OF_ADMINS = cfg.globalCfg.admins

    logger.log(logging.INFO, "Init vkcore...")
    vkcore.init(cfg.globalCfg)

    logger.log(logging.INFO, "Init tgcore...")
    updater = Updater(cfg.globalCfg.tg_token)
    tgcore.bot = updater.bot
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", tgcore.start))
    dp.add_handler(CommandHandler("help", tgcore.help))
    dp.add_handler(CommandHandler("subscribe", tgcore.subscribe))
    dp.add_handler(CommandHandler("unsubscribe", tgcore.unsubscribe))
    dp.add_handler(CommandHandler("getgroups", tgcore.getGroups))
    dp.add_handler(CommandHandler("getposts", tgcore.getPosts))
    
    #dp.add_handler(CommandHandler("adm_restart", getPosts))
    dp.add_handler(CommandHandler("adm_db_dump", tgcore.adm_db_dump))
    dp.add_handler(CommandHandler("adm_db_drop", tgcore.adm_db_drop))
    #dp.add_handler(CommandHandler("adm_db_clear", getPosts))    
    #dp.add_handler(CommandHandler("adm_stat", getPosts))

    dp.add_handler(MessageHandler(Filters.text, tgcore.textInputHandler))
    dp.add_error_handler(tgcore.errorHandler)

    logger.log(logging.INFO, "Starting polling...")
    updater.start_polling()

    logger.log(logging.INFO, "Starting interval_func...")
    utils.set_interval(tgcore.interval_func, cfg.globalCfg.timer_tick)

    logger.log(logging.INFO, "Going to loop...")
    updater.idle()


if __name__ == '__main__':
    main()
