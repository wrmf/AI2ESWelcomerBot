import json
import logging
import os
import re

import discord.opus
from discord.ext.commands import AutoShardedBot, when_mentioned_or, Context
from discord.ext.commands import CommandNotFound

from tokenfile import token

logger = logging.getLogger('bot')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='NerdBot.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
logger.info('=== RESTART ===')

TNMN = 555207100603826177

with open("options.json") as f:
	options = json.loads(f.read())

class Bot(AutoShardedBot):
	def __init__(self, *args, prefix=None, **kwargs):
		super().__init__(prefix, *args, **kwargs)

	async def on_command_error(self, context, exception):
		await context.send(f'{exception}')
		logging.error(exception)

	async def on_message(self, msg: discord.Message):
		if not self.is_ready() or msg.author.bot:
			return

		logger.debug(f'{msg}: {msg.clean_content} [{msg.system_content}]')

		ctx = await self.get_context(msg)

		try:
			await self.process_commands(msg)
			if 'delete_orig' in options and options['delete_orig'] and isinstance(ctx, Context) and ctx.valid:
				await msg.delete()
		except BaseException as e:
			logger.error(repr(e))

		if msg.guild.me in msg.mentions:
			if(ctx.message.author.id == TNMN):
				pass
			else:
				await ctx.send("My prefix is h-. You can get my command list by doing h-help")

		for m in msg.mentions:
			if await self.is_owner(m) and not await self.is_owner(msg.author):
				await msg.add_reaction("<:pingsock:638087023269380126>")


client = Bot(prefix=when_mentioned_or('h-' if 'prefix' not in options else options['prefix']),
			 pm_help=True if 'pm_help' not in options else options['pm_help'],
			 activity=discord.Game(
				 'with python' if 'game' not in options else options['game']))

@client.event
async def on_member_join(member):
	channel = discord.utils.get(member.guild.channels, name="general")
	await channel.send("Welcome %s to the AI2ES discord server! We will have chat and video and audio channels for the retreat here. Please set your nickname to be your real name. Ask @TechSupport if you have any questions!" %(member.mention))

@client.event
async def on_ready():
	print('--------------------')
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('--------------------')

for file in os.listdir("cogs"):
	if file.endswith(".py"):
		name = file[:-3]
client.load_extension(f"cogs.{name}")

client.load_extension("jishaku")

client.run(token)
