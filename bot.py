import discord

from dtoken import TOKEN

from discord.ext import commands

import json

from discord import Colour

import random

data = {}

guild = None
users = []
bot = commands.Bot(command_prefix='*', description="Welcome to Bad Coders Inc Club!")
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
		prompt = '''
		Please type in *updateuser **firstname-lastname email**
You can always rerun the same command if you spelled something wrong

Ex: *updateuser Jane-Doe janedoe36@gmail.com
		'''
		await message.channel.send(prompt)
	else:
		await bot.process_commands(message)


@bot.event
async def on_member_join(member):
	global guild
	guild = member.guild
	global users
	users.append(member)
	await member.send("Welcome to the bad coders inc club! To get started, please answer/do the follwoing prompts.")
	prompt = '''
	What programming languages are you familiar with?

(Please seperate your choices by commas only):
	'''
	await member.send(prompt)





class Miscellaneous(commands.Cog):
	def __init__(self, bot):
		self.bot=bot

	@commands.command()
	async def hello(self, ctx):
		await ctx.send("Hi!!")

	@commands.command()
	async def hi(self, ctx):
		await ctx.send("Hi!!")

bot.add_cog(Miscellaneous(bot))




class Project_Leaders(commands.Cog):
	def __init__(self, bot):
		self.bot=bot

	@commands.command()
	@commands.has_role("project leader")
	async def create(self, ctx, name=None, link=None):
		if name==None or link==None:
			await ctx.send('Please use the following format: *create <name of project> <github link>')
			return None
		with open('projects.json','r') as datafile:
			global data
			data=json.load(datafile)
			if str(ctx.author.id) not in data['members'].keys():
				await ctx.send('You are not in the database. Please use updateuser')
			new={
			"members" :{str(ctx.author.id): 'Leader'},
			"link":link,
			"status": "open"
			}
			data["projects"][name] = new
		with open('projects.json', 'w') as datafile:
			json.dump(data, fp = datafile, indent = 4)

		random_number = random. randint(0,16777215)
		hex_number = int(hex(random_number), base = 16)
		color = Colour(hex_number)
		await ctx.guild.create_role(name = name,color = color, mentionable = True)
		role = discord.utils.get(ctx.guild.roles, name=name)
		await ctx.author.add_roles(role)
		await ctx.send('Project created.')

	@commands.command()
	@commands.has_role("project leader")
	async def add(self, ctx, member: discord.Member, project=None):
		if project==None:
			await ctx.send("Please specify the project you want to add the member to")
			return None
		with open('projects.json', 'r') as datafile:
			try:
				global data
				data = json.load(datafile)
				dic = data['members'][str(member.id)]
				try:
					if data['projects'][project]['members'][str(member.id)] != None:
						await ctx.send('This user is already on this project.')
						return None
				except KeyError:
					pass
				data['projects'][project]['members'][str(member.id)] = 'Member'
			except KeyError:
				await ctx.send("This member is not in the database. Please tell him/her to use updateuser.")
				return None

		with open('projects.json', 'w') as datafile:
			json.dump(data, fp = datafile, indent = 4)
			await ctx.send('Member added')

		role = discord.utils.get(ctx.guild.roles, name=project)
		await member.add_roles(role)


	@commands.command()
	@commands.has_role("project leader")
	async def close(self, ctx, project=None):
		if project==None:
			await ctx.send("Please specify the project you want to close")
			return None
		with open('projects.json', 'r') as datafile:
			global data
			data = json.load(datafile)
			data['projects'][project]['status'] = 'closed'
		with open('projects.json', 'w') as datafile:
			json.dump(data, fp = datafile, indent = 4)
		await ctx.send('Project closed.')
		role = discord.utils.get(ctx.guild.roles, name=project)
		await role.delete()



bot.add_cog(Project_Leaders(bot))

class General(commands.Cog):
	def __init__(self, bot):
		self.bot=bot

	@commands.command()
	async def list(self, ctx, what=None, open_only='open'):
		if what==None:
			await ctx.send('Please specify whether you want to list projects or members')
			return None
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
							for memberid in value["members"].keys():
								members += data['members'][memberid]['name']+", "
							members = members[:len(members)-2]

							formatted = str(project)+": "+value["link"]+"\n"+members+"\n\n"

							line+=formatted
					elif open_only=='all':
						members = ""
						for memberid in value["members"].keys():
							members += data['members'][memberid]['name']+", "
						members = members[:len(members)-2]

						formatted = str(project)+": "+value["link"]+"\n"+members+"\n\n"

						line+=formatted
					else:
						await ctx.send('Please type in all or open after *list projects')
						return None

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
				return None

	@commands.command()
	async def project(self, ctx, name):
		pass

	@commands.command()
	async def updateuser(self, ctx, Name=None, email=None):
		if Name==None or email==None:
			await ctx.send('Please follow this format: *updateuser **firstname-lastname email** \nEx: *updateuser Jane-Doe janedoe36@gmail.com')
			return None
		global data
		names = Name.split('-')
		name = ''
		for part in names:
			name+= part + ' '
		name = name.strip()
		with open('projects.json', 'r') as datafile:
			data = json.load(datafile)
			data['members'][str(ctx.author.id)] = {"name": name, "status": "Member", "email": email}

		with open('projects.json', 'w') as datafile:
			json.dump(data, fp = datafile, indent = 4)
			await ctx.send('User ' + str(ctx.author) + ' updated.')

		await ctx.author.edit(nick = name)

bot.add_cog(General(bot))



bot.run(TOKEN)
