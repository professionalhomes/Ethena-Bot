import asyncio
import os
from datetime import datetime, timedelta, timezone

import discord
from dotenv import load_dotenv

from utils.fetch_data import sendDM

intents = discord.Intents.default()
bot = discord.Bot(intents=intents)
tz = timezone(timedelta(hours=8))


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    bot.loop.create_task(daily_task())

async def daily_task():
    while True:
        tz = timezone(timedelta(hours=8))
        now = datetime.now(tz)
        target_time = datetime(now.year, now.month, now.day, 14, 40, 10, tzinfo=tz)

        if now >= target_time:
            target_time += timedelta(days=1)

        wait_time = (target_time - now).total_seconds()
        print(f'current time: {now}\nfetch data at: {target_time}({wait_time} sec later)')
        await asyncio.sleep(wait_time)
        await sendDM(bot, int(target_time.timestamp()))


if __name__ == '__main__':
    extensions = [
        'cogs.ping',
        'cogs.settings',

    ]
    for extension in extensions:
        bot.load_extension(extension)

load_dotenv()
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
