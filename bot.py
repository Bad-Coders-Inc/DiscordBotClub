import discord

from dtoken import TOKEN

from discord.ext import commands

roles_assigned = True
guild = None
the_user = None
bot = commands.Bot(command_prefix='+', description="Codeucate's Customer Service Bot")
@bot.event
async def on_ready():

	print('Logged in as')

	print(bot.user.name)

	print(bot.user.id)

	print('------')

@bot.event
async def on_message(message):
	global roles_assigned
	global the_user
	global guild
	if not roles_assigned and the_user == message.author:
		selected_roles = message.content.replace(' ','').split(',')
		for a_role in selected_roles:
			role_name = a_role.title()
			try:
				role = discord.utils.get(guild.roles, name=role_name)
				await the_user.add_roles(role)
			except:
				await message.author.send(f"Could not find {a_role}")
		roles_assigned=True
	else:
		await bot.process_commands(message)







@bot.event
async def on_member_join(member):
	global guild
	guild = member.guild
	global the_user
	the_user  = member
	await member.send("Hello! I am a bot here to help you, and I'll be there to answer any questions about our club that you might have!")
	global roles_assigned
	roles_assigned = False
	prompt = '''
	Which programming languages do you use?
	-Python
	-Java
	-C
	-C++
	-C#
	-Swift
	-Other
	-No experience
	(Please seperate your choices by commas only):
	'''
	await member.send(prompt)


@bot.command()
async def hello(ctx):
	await ctx.send("Hi!!")

@bot.command()
async def hi(ctx):
	await ctx.send("Hi!!")

bot.run(TOKEN)
