import discord

from dtoken import TOKEN

from discord.ext import commands

import json

data = {}

guild = None
users = []
bot = commands.Bot(command_prefix='>', description="Codeucate's Customer Service Bot")
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
	await member.send("Welcome to the bad coders inc club! To get started, please answer the following prompt.")
	prompt = '''
	What programming languages are you familiar with?
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
@commands.has_role("Admin")
async def add(ctx, member: discord.Member, project):
	global data
	with open('projects.json', 'r') as datafile:
		try:
			data = json.load(datafile)
			data['projects'][project]['members'].append(data['members'][str(member.id)]['name'])
		except:
			await ctx.send("Could not find that member.")


@bot.command()
async def list(ctx, what, open_only='open'):
	with open('projects.json', 'r') as datafile:
		data=json.load(datafile)
		line=""
		if (what=="projects"):
			for project in data["projects"].keys():
				value = data["projects"][project]
				status = value['status']
				if open_only=="open":
					if status=='open':
						members = ""
						for member in value["members"]:
							members += member+", "
						members = members[:len(members)-2]

						formatted = str(project)+": "+value["link"]+"\n"+members+"\n\n"

						line+=formatted
				elif open_only=='all':
					members = ""
					for member in value["members"]:
						members += member+", "
					members = members[:len(members)-2]

					formatted = str(project)+": "+value["link"]+"\n"+members+"\n\n"

					line+=formatted

			if line.strip()=="":
				line = "no open projects currently"
			else:
				line = line[:len(line)-2]
			await ctx.send(line)
		elif (what=="members"):
			for member in data["members"].values():
				line+=str(member["name"]+", ")
			line = line[:len(line)-2]
			await ctx.send(line)
		else:
			await ctx.send("Please type in members or projects :)")

@bot.command()
async def create(ctx, name, link):
	pass

@bot.command()
async def project(ctx, name):
	pass

@bot.command()
async def updateuser(ctx, Name, email):
	global data
	names = Name.split('-')
	name = names[0] + ' ' + names[1]
	with open('projects.json', 'r') as datafile:
		data = json.load(datafile)
		data['members'][ctx.author.id] = {"name": name, "status": "Member", "email": email}

	with open('projects.json', 'w') as datafile:
		json.dump(data, fp = datafile, indent = 4)

bot.run(TOKEN)
