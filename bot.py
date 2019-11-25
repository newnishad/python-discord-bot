import discord
import time
import random
from random import randint
import os
import urllib.request
from discord.ext import commands
from discord.utils import get

TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' #Your Discord App Token
GOD = 'XXXXXXXXXXXXXXXXXXXXXXX' #Your discord ID

WELCOME_CHANNEL = 'XXXXXXXXXXXXX' #Channel id
USER_LEAVING_NOTIFICATION_CHANNEL = 'XXXXXXXXXXXXXXX' #Channel ID

admin = []


client = commands.Bot(command_prefix = '.')
client.remove_command('help')


game_guess = []
cooldownhzrp = []
spychannel = []

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


@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='type .help',type=random.randint(1,3)))
    print('Bot is ready.')
    print ("Name: " + client.user.name)
    print ("ID:  " + client.user.id)

@client.event
async def on_message(message):
    author = message.author
    if ('nisad' in message.content.lower() or GOD in message.content.lower()) and message.author != client.user and message.author.id != GOD:
        await client.add_reaction(message,emoji="\N{REGIONAL INDICATOR SYMBOL LETTER N}")
        await client.add_reaction(message,emoji="\N{REGIONAL INDICATOR SYMBOL LETTER I}")
        await client.add_reaction(message,emoji="\N{REGIONAL INDICATOR SYMBOL LETTER S}")
        await client.add_reaction(message,emoji="\N{REGIONAL INDICATOR SYMBOL LETTER A}")
        await client.add_reaction(message,emoji="\N{REGIONAL INDICATOR SYMBOL LETTER D}")
        
    #chatlogs
    content = message.content
    print('{} - {} - {} - {}'.format(author,message.server,message.channel,content))

#On join server
@client.event
async def on_member_join(member):
    await client.send_message(client.get_channel(WELCOME_CHANNEL), 'Hello {}, welcome to *The Rahmans*! Please introduce yourself.\n'.format(member.mention))

#On leave server
@client.event
async def on_member_remove(member):
    await client.send_message(client.get_channel(USER_LEAVING_NOTIFICATION_CHANNEL), '{} is a snitch.\n'.format(member.nick))
    

@client.command(pass_context=True)
async def setstatus(ctx):
    sta = ctx.message.content.lstrip('.setstatus')
    if ctx.message.author.id in admin:
        await client.change_presence(game=discord.Game(name=sta,type=random.randint(1,3)))
    else:
        await client.say('Who are you? !')
        
@client.command(pass_context=True)
async def makeadmin(ctx):
    sta = ctx.message.content.lstrip('.makeadmin')
    if ctx.message.author.id in admin:
        admin.append(ctx.message.mentions[0].id)
        await client.say('{} is a new admin!'.format(ctx.message.mentions[0].mention))
    else:
        await client.say('Who are you? !')
    

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
    embed.add_field(name='.slap',value='`Use [.slap @mention] to slap someone.`',inline=False)
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
async def hzrp(ctx):
    ign = ctx.message.content.lstrip('.hzrp ').replace(' ','_').lower()
    if not ign:
        await client.say('Hey {}, Let me show you an example of how to use that command.\n\nExample:\n`.hzrp Takeo_Matsumi`'.format(ctx.message.author.mention))
        return
    if guessfind(cooldownhzrp,ctx.message.author.id,False):
        if (time.time()-cooldownhzrp[guessfind(cooldownhzrp,ctx.message.author.id,True)][1]) <= 20:
            await client.say('{}, 20 seconds cool down for you! :stuck_out_tongue:'.format(ctx.message.author.mention))
            return

    url = 'https://signature.hzgaming.net/sig.php?name=' + ign + '&style=1'
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64'})
    response = urllib.request.urlopen(request)
    try:
        content = response.read().decode('utf-8')
    except:
        content = ""
    
    if "Non-Existant Player" in content:
        await client.say('{}, that player doesn\'t exist. '.format(ctx.message.author.mention))
        return
    elif "Access Denied" in content:
        await client.say('{}, stop right there. :raised_back_of_hand: :sos:'.format(ctx.message.author.mention))
        return
    
    filename = str(randint(1000000,9999999)) + str(randint(1000000,9999999)) + '.png'
    f = open(filename,'wb')
    f.write(urllib.request.urlopen(request).read())
    f.close()
    if guessfind(cooldownhzrp,ctx.message.author.id,False):
        cooldownhzrp.pop(guessfind(cooldownhzrp,ctx.message.author.id,True))
    cooldownhzrp.append([ctx.message.author.id,time.time()])
    await client.send_file(ctx.message.channel, filename)
    await client.say('Oi {}, the stats of {} are here.'.format(ctx.message.author.mention, ign))


@client.command(pass_context=True)
async def guess(ctx,value=""):
    if value.lower() == 'start':
        if guessfind(game_guess,ctx.message.server.id,False):
            await client.say('Hey {}, there is already a guessing match!\ntry to guess the number using `.guess number` command.'.format(ctx.message.author.mention))
        else:
            random_number = random.randint(1,100)
            game_guess.append([ctx.message.server.id,random_number])
            await client.say('A guessing match has just started, try to guess the number :smiley: \n`Hint: It must be in between 1 and 100`')
            await client.send_message(client.get_channel('598924476704358424'), 'Guess answer is {}\n'.format(random_number))
    elif value.isdigit():
        if guessfind(game_guess,ctx.message.server.id,False):
            number = game_guess[guessfind(game_guess,ctx.message.server.id,True)][1]
            value = int(value)
            if value > 100 or 1 > value:
                await client.say('Oi {}, as I said it must be in between 1 and 100.'.format(ctx.message.author.mention))
                return
            if number > value:
                await client.say('Wrong {}, {} is too low!'.format(ctx.message.author.mention,value))
            elif number < value:
                await client.say('Wrong {}, {} is too high!'.format(ctx.message.author.mention,value))
            else:
                await client.say('Wooohoo! :heart_eyes:{}:heart_eyes: is the winner! {} is the correct number :smiley:'.format(ctx.message.author.mention,value))
                game_guess.pop(guessfind(game_guess,ctx.message.server.id,True))
        else:
            await client.say('{}, there is no on going guessing match! Start a match by typing `.guess start` command. :-)'.format(ctx.message.author.mention))


@client.command(pass_context=True)
async def slap(ctx):
     if len(ctx.message.mentions) == 0:
         await client.say('{} you have to mention someone!'.format(ctx.message.author.mention))
     else:
         imgList = os.listdir("./slap")
         imgString = random.choice(imgList)
         path = "./slap/" + imgString
         await client.send_file(ctx.message.channel, path)
         await client.say('{} was slapped by {}'.format(ctx.message.mentions[0].mention,ctx.message.author.mention))

@client.command(pass_context=True)
async def spy(ctx):
    targetChannelId = ctx.message.content.lstrip('.spy')
    spychannel.append([targetChannelId,ctx.message.channel.id])

client.run(TOKEN)
