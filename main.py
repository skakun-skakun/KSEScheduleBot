import asyncio
# import logging
from bot import bot, dp, parser
from handlers import start, update_dfs, week_schedule, interval_schedule


async def main():
    dp.include_routers(start.router, update_dfs.router, week_schedule.router, interval_schedule.router)
    # logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        parser.dump_dfs()
        print("It's the end")
