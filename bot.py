import discord

from bot_token import TOKEN

from discord.ext import commands

import chatbot

bot = commands.Bot(command_prefix='', description="Codeucate's Customer Service Bot")
@bot.event
async def on_ready():

    print('Logged in as')

    print(bot.user.name)

    print(bot.user.id)

    print('------')



@bot.event
async def on_message(message):
    

async def on_member_join(member):
    await member.send("Hello! I am a bot here to help you, and I'll be there to answer any questions about our club that you might have!")


bot.run(TOKEN)
