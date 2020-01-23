import discord
import random
import asyncio
from discord.ext import commands

bot = commands.Bot(command_prefix='$', description='A bot that posts raffles.')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(pass_context=True)
@commands.cooldown(1, 30, commands.BucketType.user)
async def assassinate(ctx, user: str):
    server = bot.get_guild(667585691621916702)
    announcements = bot.get_channel(668143653709152296)
    assassinLog = bot.get_channel(668323099288010752)
    x = server.members
    assassin = ctx.message.author
    odds = random.randint(0,100)
    targetMember = server.get_member_named(user)

    global y
    y = []
    for member in x:
        role = discord.utils.find(lambda r: r.name == 'Nobility', server.roles)
        if role in member.roles and member != assassin and member != targetMember:
                y.append(member.mention)            
    random.shuffle(y)
    
    y = [y[0],y[1],y[2],assassin.mention]
    random.shuffle(y)

    await assassinLog("Assassin: " + assasin.mention + "Target: " + targetMember.mention)
    
    if odds < 15:
        roles = targetMember.roles
        everyone = discord.utils.get(server.roles, name ="@everyone")
        roles.remove(everyone)
        await targetMember.remove_roles(*roles)
        dead = discord.utils.get(server.roles, name="Talking Dead")
        await targetMember.add_roles(dead)
        await announcements.send(assassin.mention + " assassinated " + targetMember.mention + "!")
        
    elif odds < 30:
        roles = targetMember.roles
        everyone = discord.utils.get(server.roles, name ="@everyone")
        roles.remove(everyone)
        await targetMember.remove_roles(*roles)
        dead = discord.utils.get(server.roles, name="Talking Dead")
        await targetMember.add_roles(dead)

        await announcements.send("Someone assassinated " + targetMember.mention + "!")
        await announcements.send("Suspects are " + y[0] + ", " + y[1] + ", " +
                                 y[2] + ", " + y[3])
        
    elif odds < 65:
        await announcements.send(assassin.mention + " attempted to assassinate " + targetMember.mention + "!")
        
    else:
        await announcements.send("Someone attempted to assassinate " + targetMember.mention + "!")
        await announcements.send("Suspects are " + y[0] + ", " + y[1] + ", " +
                                 y[2] + ", " + y[3])
@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        await bot.send_message(ctx.message.channel, content='This command is on a %.2fs cooldown' % error.retry_after)
    raise error  # re-raise the error so all the errors will still show up in console

bot.run("NDU3Njk5ODY4NjM1NTYxOTg1.XijKIg.PnrExzKy0mwuXYuzXIBdQtnc-XM")
