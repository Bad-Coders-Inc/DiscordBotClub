
from dtoken import TOKEN

from discord.ext import commands

bot = commands.Bot(command_prefix='', description="Codeucate's Customer Service Bot")
@bot.event
async def on_ready():

	print('Logged in as')

	print(bot.user.name)

	print(bot.user.id)

	print('------')

rolesAssigned = False
guild = None

@bot.event
async def on_message(message):

	if not rolesAssigned:
		selected_roles = message.content.split(",")
		for a_role in selected_roles:
			role_name = a_role.lower()
			try:
				user = message.author
				role = discord.utils.get(guild.roles, name=role_name)
				await client.add_roles(user, role)
			except:
				await message.author.send(f"Could not find {a_role}")
		rolesAssigned=True
	else:
		await bot.process_commands(message)







@bot.event
async def on_member_join(member):
	guild = member.guild
	await member.send("Hello! I am a bot here to help you, and I'll be there to answer any questions about our club that you might have!")
	if not rolesAssigned:
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
