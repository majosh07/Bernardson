from discord.ext import commands
import discord.utils


class Notifs(commands.Cog):
    def __init__(self, bot, args) -> None:
        self.bot = bot
        self.args = args

    @commands.command(aliases=['notifs',])
    async def askb_notifs(self, ctx):
        if not self.has_roles_perms(ctx.guild.me):
            await ctx.send("I don't have permission to manage roles...")
            return

        # can make this modular later if wanted
        notif_role = discord.utils.get(ctx.guild.roles, name="askb Notifs")

        if notif_role is None:
            await ctx.send('Couldn\'t find the role "askb_notifs" in the roles list...')
            return


        if notif_role in ctx.author.roles:
            await ctx.author.remove_roles(notif_role)
            await ctx.send(f"Removed askb_notifs from {ctx.author.name}...")
        else:
            await ctx.author.add_roles(notif_role)
            await ctx.send(f"Added askb_notifs to {ctx.author.name}!")


    def has_roles_perms(self, bot):
        return bot.guild_permissions.manage_roles

