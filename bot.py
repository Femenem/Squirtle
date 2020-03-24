import discord
import json
from classes.Movie import Movie
import sqlite3
from pprint import pprint
import datetime
import asyncio
import random

helpMessage = """
```
##### GOD COMMANDS #####
!god help = This help message.
!god dev = The open source github repo.
### Randomised commands ###
!god choice [choice, choice, choice] = Picks an option at random.
!god coin = Flip a coin.

### Movie commands ###
!god movie [title] = Get info about a specific movie.

### CS commands ###
!cs status = See the current status of the CS game.
!cs reset = Resets the CS game to default settings. (Use this after completing a game)
!cs mode [comp|br] = Sets the mode for the cs game (Competitive or Battle Royale)
!cs captains [@name, @name] = Sets the captains for the cs game
!cs players [name,name,name,name...] = Sets the players for the cs game
!cs go = Starts the veto/random teams process.
!cs randomise = Re-randomise the teams for the cs game. (used after !cs go)
```
"""

class Bot(discord.Client):
    client = discord.Client

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def my_background_task(self):
        await self.wait_until_ready()
        self.targetGuild = None

        serverFile = "settings/allowedServers.json"
        serverData = open(serverFile)
        server = json.load(serverData)
        for guild in client.guilds:
            if(guild.name == server['targetServer']):
                self.targetGuild = guild
                print("Target guild found!")

        sendMessage = False
        lastTime = datetime.datetime.now().time()
        triggerTime = datetime.time(10, 0, 0, 0) # 10 AM
        messages = []
        messages.append("Pill time!")
        messages.append("TAKE YOUR PILLS!!!!!")
        messages.append("Go drug yourself.")
        messages.append("Time to take some pills.")

        while(1):
            if(self.targetGuild == None):
                print("Cannot find target guild.")
            else:
                member = discord.utils.find(lambda m: m.name == 'EpicEnchilada', self.targetGuild.members)

            now = datetime.datetime.now().time()
            if(lastTime <= triggerTime and now >= triggerTime):
                sendMessage =  True
                lastTime = now
            else:
                sendMessage = False

            if(sendMessage):
                while not self.is_closed():
                    ## RANDOM HERE
                    roll = random.randint(0, 1)
                    if (roll == 0): ## Texts
                        roll =  random.randint(0, len(messages)-1)
                        await member.send(messages[roll])
                    elif (roll == 1): ## Pictures
                        roll = random.randint(0, 3)
                        if(roll == 0):
                            file = discord.File("img/cat-pill.jpeg")
                            await member.send(content="nom nom nom", file=file)
                        elif(roll == 1):
                            file = discord.File("img/cat-pill2.jpeg")
                            await member.send(content="dont make me chew your fingers...", file=file)
                        elif(roll == 2):
                            file = discord.File("img/happy-pills.jpeg")
                            await member.send(content=":)", file=file)
                        elif(roll == 3):
                            file = discord.File("img/matrix-pill.jpeg")
                            await member.send(content="which one?", file=file)

                    sendMessage = False
                    break

            await asyncio.sleep(60) # task runs every 60 seconds


    async def on_ready(self):
        # self.load_movie_lists()
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')


        if message.content.startswith('!god'):
            option = message.content[5:].split(' ')
            if(option[0].lower() == 'help'):
                await message.channel.send(helpMessage)
            if(option[0].lower() == 'dev'):
                devUrl = "https://github.com/Mattmor/Discord-bot"
                await message.channel.send("This is the dev repo: " + devUrl)
            #####################
            # Movie options     #
            #####################
            if(option[0].lower() == 'movie' or option[0].lower() == 'film'):
                movieString = ""
                for op in option:
                    if(op != 'movie' and op != 'film'):
                        movieString += op + " "
                movie = Movie(movieString)
                await message.channel.send(movie.print_movie())
            #####################
            # Random options    #
            #####################
            if(option[0] == 'choice'):
                await self.random_choice(message)
            if(option[0] == 'flip'):
                await self.coin_flip(message)


    async def random_choice(self, message):
        choices = message.content[11:].split(',')
        randomNumber = random.randint(0, len(choices)-1)
        await message.channel.send(choices[randomNumber])

    async def coin_flip(self, message):
        roll = random.randint(0, 1)
        if (roll == 0):
            coin = "heads"
        elif (roll == 1):
            coin = "tails"
        await message.channel.send("<@" + str(message.author.id) + "> flipped a coin and it landed on " + coin)


loginFile= "settings/login.json"
loginData = open(loginFile)
login = json.load(loginData)
status = discord.Activity(name="", state="", type=discord.ActivityType.playing, details="")
client = Bot(activity=status)

client.run(login['token'])
