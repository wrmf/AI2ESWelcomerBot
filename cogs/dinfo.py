from io import BytesIO
import logging
import os

import discord
import random
from discord.ext import commands

logger = logging.getLogger("bot")

def fmt(d):
    return d.strftime('%A, %B %e %Y at %H:%M:%S')

def is_owner(ctx: commands.Context):
    return ctx.author.id == 555207100603826177


def is_admin(ctx: commands.Context):
    member: discord.Member = ctx.author
    roles: List[discord.Role] = member.roles
    return is_owner(ctx) or any([role.permissions.administrator for role in roles])


def is_mod(ctx: commands.Context):
    member: discord.Member = ctx.author
    roles: List[discord.Role] = member.roles
    return is_admin(ctx) or any([role.permissions.manage_messages for role in roles])



class Discord_Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Discord_Info(bot))




