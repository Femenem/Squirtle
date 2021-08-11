#!/usr/bin/env python
import discord
import json
import datetime
import asyncio
import random
import logging
from os import listdir

# create logger with 'spam_application'
logger = logging.getLogger('squirtle_bot')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('bot.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

class Bot(discord.Client):
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def my_background_task(self):
        await self.wait_until_ready()
        self.targetGuild = None
        # Get user ID data (add more to this if needed)
        userFile = "settings/userIDs.json"
        userData = open(userFile)
        users = json.load(userData)

        for guild in client.guilds:
            if(guild.id == 105348086737420288):
                self.targetGuild = guild
                logger.info("Target guild found!")

        sendMessage = False
        lastTime = datetime.datetime.now().time()
        triggerTime = [datetime.time(10, 0, 0, 0), datetime.time(22, 0, 0, 0)] # 10 AM, 10 PM

        foundUser = False

        if(self.targetGuild == None):
            logger.error('Cannot find target guild.')
            foundUser = False
        else:
            logger.info("Found guild, finding name")
            foundUser = True
            users = await self.targetGuild.query_members(user_ids=users["users"])
            squirt = users[1]
            emily = users[0]
            logger.info("Found name: " + squirt.display_name)
            logger.info("Found name: " + emily.display_name)
        
        logger.info("Trigger times: " + triggerTime[0].strftime("%H:%M:%S") + " and " + triggerTime[1].strftime("%H:%M:%S"))
        
        while(1):
            # Cant find users from ID
            if(not foundUser):
                # Discord down? Idk
                if(self.targetGuild == None):
                    logger.error('Cannot find target guild.')
                    foundUser = False
                else:
                    logger.info("Found guild, finding name")
                    foundUser = True
                    squirt = discord.utils.find(lambda m: m.name == 'Enchilada', self.targetGuild.members)
                    emily = discord.utils.find(lambda m: m.name == 'Emily <3', self.targetGuild.members)
                    logger.info("Found name: " + squirt.display_name)
                    logger.info("Found name: " + emily.display_name)

            now = datetime.datetime.now().time()
            # Time to trigger sending the image!
            if(lastTime <= triggerTime[0] and now >= triggerTime[0] or lastTime <= triggerTime[1] and now >= triggerTime[1]):
                logger.info("Sending message!")
                sendMessage =  True
            else:
                sendMessage = False
            
            lastTime = now

            if(sendMessage):
                try:
                    # While not broken (:
                    while not self.is_closed():
                        image = random.choice(listdir("img/"))
                        logger.info(image)
                        # Send image to all users in userIDs File
                        for user in users:
                            file = discord.File("img/{0}".format(image))
                            await user.send(content="Take your pills!", file=file)
                        sendMessage = False
                        break
                except Exception as e:
                    logger.exception("message" + e)

            await asyncio.sleep(60) # task runs every 60 seconds


    async def on_ready(self):
        logger.info('Logged on as ' + self.user.name)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        privateChannel = discord.ChannelType.private
        if message.author == discord.utils.find(lambda m: m.name == 'Enchilada', self.targetGuild.members) and message.channel.type == privateChannel:
            logger.info(message.content)
            emily = discord.utils.find(lambda m: m.name == 'Emily <3', self.targetGuild.members)
            await emily.send(message.content)
            return

        if message.content == 'ping':
            await message.channel.send('pong')

loginFile = "settings/login.json"
loginData = open(loginFile)
login = json.load(loginData)
status = discord.Activity(name="", state="", type=discord.ActivityType.playing, details="")
client = Bot(activity=status)

client.run(login['token'])