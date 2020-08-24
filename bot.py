import discord

from dtoken import TOKEN

from discord.ext import commands

import json

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
	@commands.has_role("bad coder")
	async def create(self, ctx, name, link):
		with open('projects.json','r') as datafile:
			data=json.load(datafile)
			new={
			"members" :[data['members'][str(ctx.author.id)]["name"]],
			"link":link,
			"status": "open"
			}
			data["projects"][name] = new
		with open('projects.json', 'w') as datafile:
			json.dump(data, fp = datafile, indent = 4)

	@commands.command()
	@commands.has_role("bad coder")
	async def add(self, ctx, member: discord.Member, project):
		global data
		with open('projects.json', 'r') as datafile:
			try:
				data = json.load(datafile)
				data['projects'][project]['members'].append(data['members'][str(member.id)]['name'])
			except:
				await ctx.send("Could not find that member.")

bot.add_cog(Project_Leaders(bot))

class General(commands.Cog):
	def __init__(self, bot):
		self.bot=bot

	@commands.command()
	async def list(self, ctx, what, open_only='open'):
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

	@commands.command()
	async def project(self, ctx, name):
		pass

	@commands.command()
	async def updateuser(self, ctx, Name, email):
		global data
		names = Name.split('-')
		name = names[0] + ' ' + names[1]
		with open('projects.json', 'r') as datafile:
			data = json.load(datafile)
			data['members'][str(ctx.author.id)] = {"name": name, "status": "Member", "email": email}

		with open('projects.json', 'w') as datafile:
			json.dump(data, fp = datafile, indent = 4)
			await ctx.send('User updated.')

bot.add_cog(General(bot))



bot.run(TOKEN)
