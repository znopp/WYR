import logging
import time
import discord
from util import Utils
import os
from dotenv import load_dotenv
import asyncio

# discord.dev stuff needed to make the bot work properly
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# loggers
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# all channels that the WYR bot will look and send embeds in
channels = [1012218708065787917]

message_counts = {}
last_message_times = {}


@client.event
async def on_ready():
    Utils.send(user_input="I used the json to destroy the json.")

    for channel in channels:
        channel = client.get_channel(channel)
        await channel.send("I used the json to destroy the json.")


@client.event
async def on_message(message):
    channel_id = message.channel.id

    if message.author.bot:
        return

    if channel_id not in channels:
        return

    # Increment the count for the channel or set it to 1 if it doesn't exist
    message_counts[channel_id] = message_counts.get(channel_id, 0) + 1

    current_time = time.time()

    # Only send if there's been >= 5 messages in the channel and time since last bot message was >= 5 minutes
    if message_counts[channel_id] == 5 and (channel_id not in last_message_times
                                            or current_time - last_message_times[channel_id] >= 20):

        # is there a bug?!?!??


        print(last_message_times[channel_id])

        # Actual message below vvv

        # Relevant variables from Utils.embed as well as other called functions
        embed, view, remaining_strings, shuffled_strings_2 = await Utils.embed()

        # Sending the initial embed
        sent_msg = await message.channel.send(embed=embed, view=view)

        # Deleting it after x seconds
        await asyncio.sleep(10)
        await sent_msg.delete()

        # Sending embed with results from vote
        tally_embed = await Utils.tallying(remaining_strings=remaining_strings, shuffled_strings_2=shuffled_strings_2)
        sent_tally = await message.channel.send(embed=tally_embed)

        # Deleting it after x seconds
        await asyncio.sleep(10)
        await sent_tally.delete()

        # Resetting variables
        message_counts[channel_id] = 0
        last_message_times[channel_id] = current_time

    # Prevents spam of WYR questions
    elif message_counts[channel_id] != 5:
        return

    # Store the user ID and timestamp of the message
    # print(last_message_times) (for debug purposes)


load_dotenv()
client.run(os.getenv("TOKEN"), log_level=logging.INFO)
