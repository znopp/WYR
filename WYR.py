import logging
import time
import discord
from util import Utils
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# loggers
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

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
    if message.author.bot:
        return

    channel_id = message.channel.id

    # Increment the count for the channel or set it to 1 if it doesn't exist
    message_counts[channel_id] = message_counts.get(channel_id, 0) + 1

    current_time = time.time()

    # Only send if there's been >= 5 messages in the channel and time since last bot message was >= 5 minutes
    if message_counts[channel_id] >= 5 and (channel_id not in last_message_times
                                            or current_time - last_message_times[channel_id] >= 300):
        # Actual message
        await message.channel.send("Hello")
        await message.channel.send(Utils.send_random_string())

        # Resetting variables
        message_counts[channel_id] = 0
        last_message_times[channel_id] = current_time

    # Store the timestamp of the message
    print(last_message_times)


load_dotenv()
client.run(os.getenv("TOKEN"), log_level=logging.INFO)
