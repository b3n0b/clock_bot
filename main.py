import discord
import os
import time
import nacl
import datetime
import pytz
from dateutil import tz

client = discord.Client()
f = open("token.txt", "r")
TOKEN = f.read()

@client.event
async def on_message(message):
    cntnt = message.content

    if (cntnt.startswith("$")):
        if cntnt.startswith("$ping"):
            await message.channel.send("ding dong")

        if cntnt.startswith("$ring"):
            substrings = cntnt.split(" ")
            num_times = find_num(substrings)
            channel = message.author.voice.channel
            
            await play_chime(channel, num_times)

        if cntnt.startswith("$time"):
            current_time = datetime.datetime.now(pytz.timezone("US/Central"))
            await message.channel.send("Hour: " + str(current_time.hour))
            await message.channel.send("Minute: " + str(current_time.minute))
            await message.channel.send("Second: " + str(current_time.second))

        if cntnt.startswith("$activate"):
            await message.channel.send("The clock is active!")
            channel = message.author.voice.channel

            while (True):
                print("loop")
                current_time = datetime.datetime.now(pytz.timezone("US/Central"))

                if (current_time.hour == 23):
                    next_hour = 0
                    next_day = current_time.day + 1
                else:
                    next_hour = current_time.hour + 1
                    next_day = current_time.day

                if ((next_day == 32) and (current_time.month == 1 or current_time.month == 3 or current_time.month == 5 or current_time.month == 7 or current_time.month == 8 or current_time.month == 10 or current_time.month == 12)):
                    next_month = current_time.month + 1
                    next_day = 1
                elif ((next_day == 31) and (current_time.month == 4 or current_time.month == 6 or current_time.month == 9 or current_time.month == 1)):
                    next_month = current_time.month + 1
                    next_day = 1
                elif ((next_day == 29) and (current_time.month == 2)):
                    next_month = current_time.month + 1
                    next_day = 1
                else:
                    next_month = current_time.month

                if (next_month == 13):
                    next_year = current_time.year + 1
                else:
                    next_year = current_time.year

                next_time = datetime.datetime(next_year, next_month, next_day, next_hour, 0, 0, 0)
                central = pytz.timezone("US/Central")
                print(central.localize(next_time))

                await discord.utils.sleep_until(central.localize(next_time))
                
                if (next_hour > 12):
                    next_hour -= 12
                if(next_hour == 0):
                    next_hour = 12
                
                await play_chime(channel, next_hour)


async def play_chime(channel, num_times):
    file = "singlechime.mp3"
    voice_client = await channel.connect()

    for i in range(num_times):  
        voice_client.play(discord.FFmpegPCMAudio(file))
        time.sleep(3)

    time.sleep(3)

    await voice_client.disconnect()

def find_num(substrings):
    nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    for i in substrings:
        for j in nums:
            if i.startswith(j):
                return int(i)
    
    return 1


client.run(TOKEN)