import discord
import random
import asyncio
from discord.ext import commands
#from discord.ext import unbelieva

from datetime import datetime
import pytz
import math
bot = commands.Bot(command_prefix='$', description="A bot that runs Western Kingdoms")
global override
override = False

global oddMod
oddMod = 0

global murderOverride
murderOverride = False

global assassinateOverride
assassinateOverride = False

#unbelieva.inject()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(pass_context=True)
@commands.has_role('Game Manager')
async def overrideAssassinate(ctx, setBool: bool):
    global assassinateOverride
    assassinateOverride = setBool
    await ctx.send("Assassinate Override set to: " + str(assassinateOverride))
    
@commands.has_any_role('Peasant', 'Nobility', 'Chancellor')
@bot.command(pass_context=True)
async def register(ctx):
    file = open("./candidates.txt", "a")
    file.append("\n" + str(ctx.author.id))

@bot.command(pass_context=True)	
async def randomMember(ctx):
	server = bot.get_guild(667585691621916702)
	memberList = server.members
	peasant = discord.utils.get(server.roles, name = "Peasant")
	hitList = []
	for member in memberList:
		if peasant in member.roles:
			hitList.append(member.mention)            
	random.shuffle(hitList)
	ctx.send(hitList[0])
@bot.command(pass_context=True)
async def jury(ctx):
	server = bot.get_guild(667585691621916702)
	courtCh = bot.get_channel(671761760348536863)
	jurorList = []
	for member in memberList:
		if(peasant in member.roles or noble in member.roles) and court not in member.roles:
			jurorList.append(member.mention)            
	random.shuffle(jurorList)
	memberList = server.members
	
	court = discord.utils.get(server.roles, name = "Court")
	peasant = discord.utils.get(server.roles, name = "Peasant")
	noble = discord.utils.get(server.roles, name = "Nobility")
	
	jurorList = []
	for member in memberList:
		if(peasant in member.roles or noble in member.roles) and court not in member.roles:
			jurorList.append(member.mention)            
	random.shuffle(jurorList)
	await ctx.message.delete()
	await courtCh.send("The jurors are " + jurorList[0] + ", " + jurorList[1] + ", " + jurorList[2] + ", " + jurorList[3] + ", " + jurorList[4] + ", and " + jurorList[5])


@bot.command(pass_context=True)
async def candidates(ctx):
    await ctx.send("Candidates:")
    file = open("./candidates.txt", "r")
    candidateList = file.read()
    candidateList = candidateList.split("\n")
    print(candidateList)
    for x in candidateList:
        x = int(x)
        print(x)
        x = ctx.message.guild.get_member(x)
        await ctx.send(x.mention)

@bot.command(pass_context=True)
@commands.has_any_role('Chancellor', 'Game Manager')
async def arrest(ctx, user: str):
	server = bot.get_guild(667585691621916702)
	announcements = bot.get_channel(668143653709152296)
	user = server.get_member_named(user)
	prisonerRoles = user.roles
	gm = discord.utils.get(server.roles, name="Game Manager")	
	chancellor = discord.utils.get(server.roles, name="Chancellor")
	botUser = discord.utils.get(server.roles, name="Bot Management")
	if gm not in prisonerRoles and bot not in prisonerRoles:
		everyone = discord.utils.get(server.roles, name ="@everyone")
		prisonerRoles.remove(everyone)
		await user.remove_roles(*prisonerRoles)
		prisoner = discord.utils.get(server.roles, name="Prisoner")
		await user.add_roles(prisoner)
		await announcements.send(ctx.author.mention + " arrested " + user.mention + "!")
	else:
		await ctx.send("You cannot arrest Game Managers or Bots")

@bot.command(pass_context=True)
@commands.has_any_role('Chancellor', 'Game Manager')
async def noble(ctx, user: str):
	server = bot.get_guild(667585691621916702)
	announcements = bot.get_channel(668143653709152296)
	user = server.get_member_named(user)
	targetRoles = user.roles
	peasant = discord.utils.get(server.roles, name="Peasant")
	if peasant in targetRoles:
		everyone = discord.utils.get(server.roles, name ="@everyone")
		targetRoles.remove(everyone)
		await user.remove_roles(*targetRoles)
		noble = discord.utils.get(server.roles, name="Nobility")
		await user.add_roles(noble)
		await announcements.send(ctx.author.mention + " promoted " + user.mention + "!")
	else:
		await ctx.send("You can only promote peasants")

		
@bot.command(pass_context=True)
@commands.has_any_role('Chancellor', 'Game Manager')
async def execute(ctx, user: str):
	server = bot.get_guild(667585691621916702)
	announcements = bot.get_channel(668143653709152296)
	user = server.get_member_named(user)
	prisonerRoles = user.roles
	gm = discord.utils.get(server.roles, name="Game Manager")	
	chancellor = discord.utils.get(server.roles, name="Chancellor")
	botUser = discord.utils.get(server.roles, name="Bot Management")
	if gm not in prisonerRoles and bot not in prisonerRoles:
		everyone = discord.utils.get(server.roles, name ="@everyone")
		prisonerRoles.remove(everyone)
		await user.remove_roles(*prisonerRoles)
		prisoner = discord.utils.get(server.roles, name="Talking Dead")
		await user.add_roles(prisoner)
		await announcements.send(ctx.author.mention + " executed " + user.mention + "!")
	else:
		await ctx.send("You cannot kill Game Managers or Bots")
		


@bot.command(pass_context=True)
@commands.has_role('Game Manager')
async def overrideMurder(ctx, setBool: bool):
    global murderOverride
    murderOverride = setBool
    await ctx.send("Murder Override set to: " + str(murderOverride))

@bot.command(pass_context=True)
@commands.has_role('Game Manager')
async def overrideKill(ctx, setBool: bool):
    global override
    override = setBool
    await ctx.send("Kill Override set to: " + str(override))
    
@bot.command(pass_context=True)
@commands.cooldown(1, 43200, commands.BucketType.user)
async def assassinate(ctx, user: str):
    global assassinateOverride
    global override
    tz_MST = pytz.timezone('Canada/Mountain') 
    datetime_Calgary = datetime.now(tz_MST)
    hour = datetime_Calgary.hour
    timeCheck = (hour >= 18 or  hour <9)

    server = bot.get_guild(667585691621916702)
    announcements = bot.get_channel(668143653709152296)
    assassinLog = bot.get_channel(668323099288010752)
    x = server.members
    assassin = ctx.message.author
    odds = random.randint(0,100)
    assassin = server.get_member(assassin.id)
    targetMember = server.get_member_named(user)
    aRoles = assassin.roles
    
    noble = discord.utils.get(server.roles, name="Noble")
    peasant = discord.utils.get(server.roles, name="Peasant")
    gameManager = discord.utils.get(server.roles, name="Game Manager")
    botManagement = discord.utils.get(server.roles, name="Bot Management")
    chancellor = discord.utils.get(server.roles, name="Chancellor")
    death = discord.utils.get(server.roles, name="Death Scythe")
    vital = discord.utils.get(server.roles, name="Blade of Vitality")
    tRoles = targetMember.roles
    global oddMod
    oddMod = 0
    if death in aRoles:

        oddMod += 25
    else:

        oddMod += 0

    if vital in tRoles:

        oddMod -= 25
    else:

        oddMod -= 0
        
    permission = (noble in aRoles or gameManager in aRoles)
    print(str(permission))
    validTarget = not( chancellor in tRoles or gameManager in tRoles or botManagement in tRoles)
    global y
    y = []
    if (timeCheck or override or assassinateOverride) and permission and validTarget:

        for member in x:
            role = discord.utils.find(lambda r: r.name == 'Nobility', server.roles)
            if role in member.roles and member != assassin and member != targetMember:
                y.append(member.mention)            
        random.shuffle(y)
    
        y = [y[0],y[1],y[2],assassin.mention]
        random.shuffle(y)

        await assassinLog.send("Assassin: " + assassin.mention + "\nTarget: " + targetMember.mention)
        
        if odds < (15+(oddMod/2)):
            roles = targetMember.roles
            everyone = discord.utils.get(server.roles, name ="@everyone")
            roles.remove(everyone)
            await targetMember.remove_roles(*roles)
            dead = discord.utils.get(server.roles, name="Talking Dead")
            await targetMember.add_roles(dead)
            await announcements.send(assassin.mention + " assassinated " + targetMember.mention + "!")
        
        elif odds < (30+(oddMod/2)):
            roles = targetMember.roles
            everyone = discord.utils.get(server.roles, name ="@everyone")
            roles.remove(everyone)
            await targetMember.remove_roles(*roles)
            dead = discord.utils.get(server.roles, name="Talking Dead")
            await targetMember.add_roles(dead)

            await announcements.send("Someone assassinated " + targetMember.mention + "!")
            await announcements.send("Suspects are " + y[0] + ", " + y[1] + ", " +
                                 y[2] + ", " + y[3])
        
        elif odds < ((100-(30+oddMod))/2 + (oddMod+30)):
            await announcements.send(assassin.mention + " attempted to assassinate " + targetMember.mention + "!")
        
        else:
            await announcements.send("Someone attempted to assassinate " + targetMember.mention + "!")
            await announcements.send("Suspects are " + y[0] + ", " + y[1] + ", " +
                                 y[2] + ", " + y[3])
    else:
        if not (timeCheck or override or assassinateOverride):
            await ctx.send("The assassin is only available between 9PM MST and 9AM MST")
        if not permission:
            await ctx.send("The assassin can only be hired by Nobility, perhaps you meant murder?")
        if not validTarget:
            await ctx.send("You cannot hire the assassin to kill the Chancellor or a Game Manager")

@bot.command(pass_context=True, cooldown_after_parsing=True)
@commands.cooldown(1, 43200, commands.BucketType.user)
async def murder(ctx, user: str):
    print("Starting murder")
    global murderOverride
    global override
    tz_MST = pytz.timezone('Canada/Mountain') 
    datetime_Calgary = datetime.now(tz_MST)
    hour = datetime_Calgary.hour
    timeCheck = (hour >= 18 or  hour <9)

    server = bot.get_guild(667585691621916702)
    announcements = bot.get_channel(668143653709152296)
    assassinLog = bot.get_channel(668323099288010752)
    x = server.members
    assassin = ctx.message.author
    odds = random.randint(0,100)
    targetMember = server.get_member_named(user)
    assassin = server.get_member(assassin.id)
    aRoles = assassin.roles
    

    noble = discord.utils.get(server.roles, name="Noble")
    peasant = discord.utils.get(server.roles, name="Peasant")
    gameManager = discord.utils.get(server.roles, name="Game Manager")
    botManagement = discord.utils.get(server.roles, name="Bot Management")
    chancellor = discord.utils.get(server.roles, name= "Chancellor")
    death = discord.utils.get(server.roles, name="Death Scythe")
    vital = discord.utils.get(server.roles, name="Blade of Vitality")
    tRoles = targetMember.roles
    global oddMod
    oddMod = 0
    
    if death in aRoles:
        oddMod += 25
    else:
        oddMod += 0

    if vital in tRoles:

        oddMod -= 25
    else:

        oddMod -= 0
                                   
    permission = peasant in aRoles or gameManager in aRoles
    print(str(permission))
    validTarget = not(noble in tRoles or chancellor in tRoles or gameManager in tRoles or botManagement in tRoles)
    global y
    y = []
    if (timeCheck or murderOverride or override) and permission and validTarget:
        for member in x:
            role = discord.utils.find(lambda r: r.name == 'Peasant', server.roles)
            if role in member.roles and member != assassin and member != targetMember:
                y.append(member.mention)
                print(member.mention)
        random.shuffle(y)
    
        y = [y[0],y[1],y[2],assassin.mention]
        random.shuffle(y)
        print(y)
        await assassinLog.send("Murderer: " + assassin.mention + "\nTarget: " + targetMember.mention)

        
        if odds < (15+(oddMod/2)):
            roles = targetMember.roles
            everyone = discord.utils.get(server.roles, name ="@everyone")
            roles.remove(everyone)
            await targetMember.remove_roles(*roles)
            dead = discord.utils.get(server.roles, name="Talking Dead")
            await targetMember.add_roles(dead)
            await announcements.send(assassin.mention + " murdered " + targetMember.mention + "!")
        
        elif odds < (30+(oddMod/2)):
            roles = targetMember.roles
            everyone = discord.utils.get(server.roles, name ="@everyone")
            roles.remove(everyone)
            await targetMember.remove_roles(*roles)
            dead = discord.utils.get(server.roles, name="Talking Dead")
            await targetMember.add_roles(dead)

            await announcements.send("Someone murdered " + targetMember.mention + "!")
            await announcements.send("Suspects are " + y[0] + ", " + y[1] + ", " +
                                 y[2] + ", " + y[3])
        
        elif odds < (100-(30+oddMod))/2 + (30+oddMod):
            await announcements.send(assassin.mention + " attempted to murder " + targetMember.mention + "!")
        
        else:
            await announcements.send("Someone attempted to murder " + targetMember.mention + "!")
            await announcements.send("Suspects are " + y[0] + ", " + y[1] + ", " +
                                 y[2] + ", " + y[3])
    else:
        if not (timeCheck or override or murderOverride):
            await ctx.send("Murder may only occur between 9PM MST and 9AM MST")
            reset_cooldown(ctx)
        if not permission:
            await ctx.send("Only peasants are able to commit murder, perhaps you meant assassinate?")
            reset_cooldown(ctx)
        if not validTarget:
            await ctx.send("You cannot murder nobles, the Chancellor or a Game Manager")
            reset_cooldown(ctx)
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("This command is on cooldown, please retry in {} hours.".format(round((math.ceil(error.retry_after))/3600)))
        return
    else:
        print(error)


bot.run("NDU3Njk5ODY4NjM1NTYxOTg1.XijKIg.PnrExzKy0mwuXYuzXIBdQtnc-XM")
