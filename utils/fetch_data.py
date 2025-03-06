import discord


async def fetchData(bot):
    user = await bot.fetch_user(874806243208871977)
    if user:
        try:
            await user.send('data')
        except discord.Forbidden:
            print('DM closed')
    else:
        print('User not found')