import logging

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, CallbackQueryHandler

import cfg
import postSender
import language
import vkcore
import tgcore
import utils
import db

def main():
    
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.log(logging.INFO, "[CFG]. Timeout: %s", cfg.globalCfg.timer_tick)
    logger.log(logging.INFO, "[CFG]. Between request delay: %s", cfg.globalCfg.between_request_delay)
    logger.log(logging.INFO, "[CFG]. Time zone: %s", cfg.globalCfg.time_zone)
    logger.log(logging.INFO, "[CFG]. Posts per requst: %s", cfg.globalCfg.posts_to_get)

    logger.log(logging.INFO, "Loading statistics...")
    cfg.globalStat = db.statTimeHandle.get_stat()
    if(cfg.globalStat is None):
        cfg.globalStat = cfg.stat()
        db.statTimeHandle.store_stat(cfg.globalStat)
    
    logger.log(logging.INFO, "Init vkcore...")
    vkcore.reinit(0)

    logger.log(logging.INFO, "Init tgcore...")
    updater = Updater(cfg.globalCfg.tg_token)
    tgcore.bot = updater.bot
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", tgcore.start))
    dp.add_handler(CommandHandler("settings", tgcore.settings))
    dp.add_handler(CommandHandler("help", tgcore.help))
    dp.add_handler(CommandHandler("subscribe", tgcore.subscribe))
    dp.add_handler(CommandHandler("unsubscribe", tgcore.unsubscribe))
    dp.add_handler(CommandHandler("getgroups", tgcore.getGroups))
    dp.add_handler(CommandHandler("getposts", tgcore.getPosts))
    
    #dp.add_handler(CommandHandler("adm_restart", getPosts))
    dp.add_handler(CommandHandler("adm_dbdump", tgcore.adm_db_dump))
    dp.add_handler(CommandHandler("dump", tgcore.adm_db_dump))

    dp.add_handler(CommandHandler("adm_stat", tgcore.adm_stat))
    dp.add_handler(CommandHandler("stat", tgcore.adm_stat))

    dp.add_handler(CommandHandler("adm_dbdrop", tgcore.adm_db_drop))
    dp.add_handler(CommandHandler("drop", tgcore.adm_db_drop))

    dp.add_handler(CallbackQueryHandler(tgcore.callback_inline))

    dp.add_handler(MessageHandler(Filters.text, tgcore.textInputHandler))
    dp.add_error_handler(tgcore.errorHandler)

    logger.log(logging.INFO, "Starting polling...")
    updater.start_polling()

    logger.log(logging.INFO, "Starting interval_func...")
    utils.set_interval(postSender.interval_func, cfg.globalCfg.timer_tick)

    logger.log(logging.INFO, "Going to loop...")
    updater.idle()


if __name__ == '__main__':
    main()
