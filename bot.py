# bot1.py
# A rewrite of bot.py, changing to the bot subclass from client superclass

import os
import discord
import word_filter
import datetime 
import asyncio

from discord.ext import commands, tasks
from dotenv import load_dotenv
from googletrans import Translator

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='$')

base_role_name = "Plebs"
time_out_time = 0

#Prints to console connection confirmation, initializes roles needed for bot functionality
@bot.event
async def on_ready():

	guild = discord.utils.get(bot.guilds, name=GUILD)
	guild_roles = guild.roles
	found = False

	print(
		f'{bot.user} is connected to the following guild:\n'
		f'{guild.name}(id: {guild.id})'
	)
	#removes permmisions from @everyone
	for i in guild_roles:
		if i.name == "@everyone":
			general_permissions = i.permissions
			await i.edit(permissions = discord.Permissions.none())
								
	#intitalizes base role type that gives user permissions normally given by @everyone
	for i in guild_roles:
		if base_role_name == i.name:
			found = True		
	
	if found == False:
		await guild.create_role(name = base_role_name, permissions = general_permissions )


# Welcome DM to new user
@bot.event
async def on_member_join(member):
	
	guild = discord.utils.get(bot.guilds, name=GUILD)
	guild_roles = guild.roles

	for i in guild_roles:
		if i.name == base_role_name:
			base_role = i

	await member.create_dm()
	await member.edit(roles = [base_role])
	await member.dm_channel.send(
		f'VOLTRON WELCOMES YOU, {member.name}'
	)

#client message parsing 
@bot.event
async def on_message(message):
	if (message.author == bot.user):
		return

	#checks all user input against list of banned words
	if (word_filter.banned_string(message.content)):
		user = message.author
		await message.delete()
		await message.author.send('Please no swearing in my Christian Discord Server')
		print(f'Banned message from {user}')

	await bot.process_commands(message)

@bot.command(name = 'help')
async def help(ctx):

	await ctx.channel.send("Please see this link for a detailed list of commands and their syntax: https://github.com/cs340-20/InstantMessengerBot/blob/master/HelpFile.txt"
	
#Kicks a user from the server. They may join back at any time
@bot.command(name = 'kick')
async def kick(ctx, member : discord.Member, *, reason = "none"):

	await member.kick(reason = reason)

	if (reason != "none"):
		await message.member.dm_channel.send{ "You were kicked for the following reason: " + reason }

#bans a user from the server.
@bot.command(name = 'ban')
async def ban(ctx, member : discord.Member, days = 0, *, reason= "none"):

    await member.ban(reason = reason, delete_msg_days = days)
	
	if (reason != "none"):
		await message.member.dm_channel.send{ "You were banned for the following reason: " + reason }


#puts a user in timeout, prventing them from sending any messages but keeping them in the server
@bot.command(name = 'timeout')
async def timeout(ctx, member : discord.Member, TO_time, *, reason = "none"):

	guild = ctx.guild
	old_roles = member.roles	
	guild_roles = guild.roles
	timeout_role_name = "Timeout"
	found = False
	
	time_out_time = TO_time

	for i in guild_roles:
		if i.name == timeout_role_name: 
			timeout_role = i
			found = True
	
	for i in old_roles:
		print(i.name)

	if found == False:
		timeout_role = await guild.create_role(name = timeout_role_name)

	await member.edit(roles = [timeout_role])

	for i in member.roles:
		print(i.name)

	loop = asyncio._get_running_loop()
	end_time = loop.time() + (TO_time *60)

	if (reason != "none"):
		await message.member.dm_channel.send{ "You were timed out for %d mintes for the following reason: %s" % (TO_time, reason) }
	else
		await message.member.dm_channel.send{ "You have been timed out from the server for %d minutes." % (TO_time) }

	while True:
		
		if(loop.time() + 1) >= end_time:
			await member.edit(roles = old_roles)
			for i in member.roles:
				print(i.name)
			break
		await asyncio.sleep(1)
	
	await message.member.dm_channel.send{ "You are no longer timed out" }

#adds a word to a file containing all banned words
@bot.command(name='ban_word')
async def ban_word(ctx, *, word = ''):
	
	if(word != ''):
		word_filter.ban_string(word)
	
#makes text channels from user input
@bot.command(name='makechannel')
#@commands.has_role('admin')
async def makechannel(ctx, channel_name='Voltron-Conference'):
	guild = ctx.guild
	existing_channel = discord.utils.get(guild.channels, name=channel_name)
	if not existing_channel:		
		print(f'Creating new channel: {channel_name}')
		await guild.create_text_channel(channel_name)

#translate command 
@bot.command(name='translate')
async def translate(ctx, msg="ex phrase: $translate \"Hello!\" french" , dst='english'):
    
    #sets up translator object
    translator = Translator()
    
    #A list made of a key-map for languages
    LANGUAGES = {
        'af': 'afrikaans',
        'sq': 'albanian',
        'am': 'amharic',
        'ar': 'arabic',
        'hy': 'armenian',
        'az': 'azerbaijani',
        'eu': 'basque',
        'be': 'belarusian',
        'bn': 'bengali',
        'bs': 'bosnian',
        'bg': 'bulgarian',
        'ca': 'catalan',
        'ceb': 'cebuano',
        'ny': 'chichewa',
        'zh-cn': 'chinese',
        'co': 'corsican',
        'hr': 'croatian',
        'cs': 'czech',
        'da': 'danish',
        'nl': 'dutch',
        'en': 'english',
        'eo': 'esperanto',
        'et': 'estonian',
        'tl': 'filipino',
        'fi': 'finnish',
        'fr': 'french',
        'fy': 'frisian',
        'gl': 'galician',
        'ka': 'georgian',
        'de': 'german',
        'el': 'greek',
        'gu': 'gujarati',
        'ht': 'haitian',
        'ha': 'hausa',
        'haw': 'hawaiian',
        'iw': 'hebrew',
        'hi': 'hindi',
        'hmn': 'hmong',
        'hu': 'hungarian',
        'is': 'icelandic',
        'ig': 'igbo',
        'id': 'indonesian',
        'ga': 'irish',
        'it': 'italian',
        'ja': 'japanese',
        'jw': 'javanese',
        'kn': 'kannada',
        'kk': 'kazakh',
        'km': 'khmer',
        'ko': 'korean',
        'ku': 'kurdish',
        'ky': 'kyrgyz',
        'lo': 'lao',
        'la': 'latin',
        'lv': 'latvian',
        'lt': 'lithuanian',
        'lb': 'luxembourgish',
        'mk': 'macedonian',
        'mg': 'malagasy',
        'ms': 'malay',
        'ml': 'malayalam',
        'mt': 'maltese',
        'mi': 'maori',
        'mr': 'marathi',
        'mn': 'mongolian',
        'my': 'myanmar',
        'ne': 'nepali',
        'no': 'norwegian',
        'ps': 'pashto',
        'fa': 'persian',
        'pl': 'polish',
        'pt': 'portuguese',
        'pa': 'punjabi',
        'ro': 'romanian',
        'ru': 'russian',
        'sm': 'samoan',
        'gd': 'gaelic',
        'sr': 'serbian',
        'st': 'sesotho',
        'sn': 'shona',
        'sd': 'sindhi',
        'si': 'sinhala',
        'sk': 'slovak',
        'sl': 'slovenian',
        'so': 'somali',
        'es': 'spanish',
        'su': 'sundanese',
        'sw': 'swahili',
        'sv': 'swedish',
        'tg': 'tajik',
        'ta': 'tamil',
        'te': 'telugu',
        'th': 'thai',
        'tr': 'turkish',
        'uk': 'ukrainian',
        'ur': 'urdu',
        'uz': 'uzbek',
        'vi': 'vietnamese',
        'cy': 'welsh',
        'xh': 'xhosa',
        'yi': 'yiddish',
        'yo': 'yoruba',
        'zu': 'zulu',
        'fil': 'Filipino',
        'he': 'Hebrew'
    }
    LANGCODES = dict(map(reversed, LANGUAGES.items()))
    
    #translator(phrase, destination lang, source language)
    newlang = translator.translate(msg, LANGCODES[dst.lower()], src='auto')

    #print to console and print to server
    print(f'translated {msg} to {newlang.text}')
    await ctx.send(newlang.text)

bot.run(TOKEN)

