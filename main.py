import asyncio
import os
from datetime import datetime, timedelta, timezone

import discord
from dotenv import load_dotenv

intents = discord.Intents.default()
bot = discord.Bot(intents=intents)
tz = timezone(timedelta(hours=8))


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    bot.loop.create_task(daily_task())

async def daily_task():
    while True:
        now = datetime.now()
        target_time = datetime(now.year, now.month, now.day, 17, 48, 30)

        if now >= target_time:
            target_time += timedelta(days=1)

        wait_time = (target_time - now).total_seconds()
        print(f'Wait {wait_time} sec to fetch data')
        await asyncio.sleep(wait_time)
        await fetchData()


async def fetchData():
    user = await bot.fetch_user(874806243208871977)
    if user:
        try:
            await user.send('data')
            print(f"DM sent {user}, time: {datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')}")
        except discord.Forbidden:
            print('DM closed')
    else:
        print('User not found')


if __name__ == '__main__':
    extensions = [
        'cogs.ping',
        'cogs.settings',

    ]
    for extension in extensions:
        bot.load_extension(extension)

load_dotenv()
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
