import discord

from dtoken import TOKEN

from discord.ext import commands

guild = None
users = []
bot = commands.Bot(command_prefix='+', description="Codeucate's Customer Service Bot")
@bot.event
async def on_ready():

	print('Logged in as')

	print(bot.user.name)

	print(bot.user.id)

	print('------')

@bot.event
async def on_message(message):
	global users
	global guild
	if message.author in users and "Direct Message" in str(message.channel):
		print(message.channel)
		for user in users:
			if message.author == user:
				the_user = user
				break
		selected_roles = message.content.replace(' ','').split(',')
		for a_role in selected_roles:
			role_name = a_role.title()
			try:
				role = discord.utils.get(guild.roles, name=role_name)
				await the_user.add_roles(role)
			except:
				await message.author.send(f"Could not find {a_role}")
		users.remove(the_user)
		print(users)
	else:
		await bot.process_commands(message)







@bot.event
async def on_member_join(member):
	global guild
	guild = member.guild
	global users
	users.append(member)
	await member.send("Hello! I am a bot here to help you, and I'll be there to answer any questions about our club that you might have!")
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

@bot.command()
async def add(ctx, member, project):
	pass

@bot.command()
async def list(ctx, what):
	pass



bot.run(TOKEN)
