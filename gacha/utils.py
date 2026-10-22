import discord

async def get_display_name(bot, guild, user_id: int) -> str:
    if guild is not None:
        member = guild.get_member(user_id)
        if member is not None:
            return member.display_name      # server nickname
    user = bot.get_user(user_id)            # cache, no network
    if user is None:
        try:
            user = await bot.fetch_user(user_id)   # API call
        except discord.NotFound:
            return "Unknown user"
    return user.display_name

