from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from database import get_all_subscriptions, mark_reminded_5, mark_reminded_1

scheduler = AsyncIOScheduler()

def start_scheduler(bot):
    scheduler.add_job(
        check_subscriptions,
        trigger='cron',
        hour=12,
        args=(bot,)
    )
    scheduler.start()

async def check_subscriptions(bot):
    today = datetime.today().date()
    subs = await get_all_subscriptions()

    for sub in subs:
        (
            sub_id,
            user_id,
            title,
            price,
            end_date,
            reminded_5_days,
            reminded_1_day,
            comment,
        ) = sub[:8]

        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        days_left = (end - today).days

        if days_left < 0:
            continue

        if days_left == 5 and not reminded_5_days:
            await bot.send_message(
                chat_id=user_id,
                text=f"Reminder: {title} ends in 5 days."
            )

            await mark_reminded_5(sub_id)

        if days_left == 1 and not reminded_1_day:
            await bot.send_message(
                chat_id=user_id,
                text=f"[!] {title} ends tomorrow!"
            )

            await mark_reminded_1(sub_id)



# async def scheduler_loop(bot):
#     while True:
#         await check_subscriptions(bot)
#         await asyncio.sleep(86400)
