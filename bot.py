import discord
import random
import time
import urllib.request
import pymysql
from discord.ext import commands
from discord.utils import get

TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' #Your Bot Token


game_guess = []
cooldownhzrp = []

def guessfind(mylist,find,value=False):
    index = 0
    for x in mylist:
        if find == x[0]:
            if value:
                return index
            else:
                return True

        index+=1
    return False

client = commands.Bot(command_prefix = '.')
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='type .help',type=random.randint(1,3)))
    print('Bot is ready.')
    print ("Name: " + client.user.name)
    print ("ID:  " + client.user.id)

@client.event
async def on_message(message):
    author = message.author
    content = message.content
    print('{} - {} - {} - {}'.format(author,message.server,message.channel,content))
    if message.author != client.user and GOD not in str(message.author.id) and BETA not in str(message.author.id):
        await client.send_message(client.get_channel('551290282482597889'), '{} - {} - {} - {}\n'.format(author,message.server,message.channel,content))
    await client.process_commands(message)

    

@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Colour.blue()
    )
    embed.set_author(name="Help")
    embed.add_field(name='.ping',value='`Helps you to know about the condition of your connection`',inline=False)
    embed.add_field(name='.say',value='`.say [Message] to announce something as bot`',inline=False)
    embed.add_field(name='.clear',value='`.clear [1-100] to clear chat as an adminstrator`',inline=False)
    embed.add_field(name='.guess start',value='`To start a guessing number match.`',inline=False)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def ping(ctx):
    await client.say("{} Pong!".format(ctx.message.author.mention))

@client.command(pass_context=True)
async def clear(ctx,amount = 1):
    if not ctx.message.author.server_permissions.administrator:
        await client.say("{} you are not an administrator!".format(ctx.message.author.mention))
        return
    if amount > 100:
        await client.say("The maximum limit is 100 {}".format(ctx.message.author.mention))
        return
    elif amount < 100:
        amount+=1
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit = int(amount)):
        messages.append(message)
    if len(messages) == 1:
        await client.delete_message(messages[0])
        selft = await client.say("Message Deleted!")
        time.sleep(2)
        await client.delete_message(self)
    elif len(messages) == 0:
        self = await client.say("There is no message to delete!")
        time.sleep(2)
        await client.delete_message(self)
    else:  
        await client.delete_messages(messages)
        self = await client.say("Messages Deleted!")
        time.sleep(2)
        await client.delete_message(self)
        

@client.command(pass_context=True)
async def say(ctx):
    message = ctx.message
    if message.author == client.user:
        return
    await client.send_message(message.channel, message.content.lstrip('.say'))
    await client.delete_message(message)

@client.command(pass_context=True)
async def guess(ctx,value=""):
    if value.lower() == 'start':
        if guessfind(game_guess,ctx.message.server.id,False):
            await client.say('Hey {}, there is already a guessing match!\ntry to guess the number using `.guess number` command.'.format(ctx.message.author.mention))
        else:
            random_number = random.randint(1,100)
            game_guess.append([ctx.message.server.id,random_number])
            await client.say('A guessing match has just started, try to guess the number :smiley: \n`Hint: It must be in between 1 and 100`')
    elif value.isdigit():
        if guessfind(game_guess,ctx.message.server.id,False):
            number = game_guess[guessfind(game_guess,ctx.message.server.id,True)][1]
            value = int(value)
            if value > 100 or 1 > value:
                await client.say('Oi {}, as I said it must be in between 1 and 100.'.format(ctx.message.author.mention))
                return
            if number > value:
                await client.say('Uh uh {}, {} is too low!'.format(ctx.message.author.mention,value))
            elif number < value:
                await client.say('Uh uh {}, {} is too high!'.format(ctx.message.author.mention,value))
            else:
                await client.say('Wooohoo! :heart_eyes:{}:heart_eyes: is the winner! {} is the correct number :smiley:'.format(ctx.message.author.mention,value))
                game_guess.pop(guessfind(game_guess,ctx.message.server.id,True))
        else:
            await client.say('{}, there is no on going guessing match! Start a match by typing `.guess start` command. :-)'.format(ctx.message.author.mention))

client.run(TOKEN)
