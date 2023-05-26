import logging
import time
import discord
from discord import app_commands
from discord.ext import commands
from util import Utils
import os
from dotenv import load_dotenv
import asyncio
import json

# discord.dev stuff needed to make the bot work properly
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)
client.remove_command("help")

# loggers
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# local channel list, updated on slash command and on startup
channels = []

# number of messages and timestamps, related to on_message function
message_counts = {}
last_message_times = {}

channels_file = "json/channels.json"
questions_data = Utils.data


# all channels that the WYR bot will look and send embeds in
def load_channels():
    if os.path.exists(channels_file) and os.path.getsize(channels_file) > 0:
        with open(channels_file, "r") as file:
            try:
                data = json.load(file)
                channels.extend(data["channel_ids"])
            except json.JSONDecodeError:
                Utils.error("Invalid JSON format in the channels file.")


# update channel list
def save_channels():
    data = {"channel_ids": channels}
    with open(channels_file, "w") as file:
        json.dump(data, file)


@client.event
async def on_ready():
    Utils.send(user_input="I used the json to destroy the json.")

    start_time = time.time()

    try:
        synced = await client.tree.sync()
        Utils.send(user_input=f"Synced {len(synced)} command(s)")
    except Exception as e:
        Utils.send(user_input=e)

    end_time = time.time()
    elapsed_time = end_time - start_time
    Utils.send(user_input=f"Sync operation took {elapsed_time} seconds")

    load_channels()
    Utils.send(user_input="Loaded channels:", prefix="\n")

    for channel in channels:
        print(f"- \"{client.get_channel(channel).name}\" with ID \"{channel}\"")


@client.tree.command(name="add_channel", description="WYR will be allowed in this channel")
async def command(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.manage_channels:
        await interaction.response.send_message("You don't have permission to run this command!", ephemeral=True)
        return

    channel_id = interaction.channel_id
    if channel_id not in channels:
        channels.append(channel_id)
        await interaction.response.send_message("Channel added!", ephemeral=True)
        save_channels()
    else:
        await interaction.response.send_message("Channel already added!", ephemeral=True)


@client.tree.command(name="remove_channel", description="WYR will not be allowed in this channel")
async def command(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.manage_channels:
        await interaction.response.send_message("You don't have permission to run this command!", ephemeral=True)
        return

    channel_id = interaction.channel_id
    if channel_id in channels:
        channels.remove(channel_id)
        await interaction.response.send_message("Channel removed!", ephemeral=True)
        save_channels()
    else:
        await interaction.response.send_message("Channel already not in list!", ephemeral=True)


# @discord.app_commands.command(name="add_question", description="Adds a question to WYR JSON list")
@client.tree.command(name="add_question", description="Adds a question to WYR JSON list! "
                                                      "Example: Never eat meat, Never drink milk")
@app_commands.describe(part_1="Would you rather...", part_2="...Or...")
async def add_question(interaction: discord.Interaction, part_1: str, part_2: str):
    if not interaction.user.guild_permissions.manage_channels:
        await interaction.response.send_message("You don't have permission to run this command!", ephemeral=True)
        return

    # formatting in case user did not
    part_1 = part_1.lower()
    part_1 = part_1[0].upper() + part_1[1:]

    part_2 = part_2.lower()
    part_2 = part_2[0].upper() + part_2[1:]

    questions_data.append([part_1, part_2])

    with open("json/questions.json", "r+") as file:

        lines = file.readlines()

        if len(lines) >= 2:
            file.seek(0, 2)
            file.seek(file.tell() - 3, 0)
            file.truncate()
            file.write(",")

        file.write("\n  " + json.dumps(questions_data[-1]) + "\n]")

    await interaction.response.send_message("Question added!", ephemeral=True)


@client.event
async def on_message(message):
    channel_id = message.channel.id

    if message.author.bot:
        return

    if channel_id not in channels:
        return

    # Increment the count for the channel or set it to 1 if it doesn't exist
    message_counts[channel_id] = message_counts.get(channel_id, 0) + 1

    # Only send if there's been >= 5 messages in the channel and time since last bot message was >= 5 minutes
    if message_counts[channel_id] == 5:

        current_time = time.time()

        if channel_id not in last_message_times or current_time - last_message_times[channel_id] >= 300:

            # Actual message below vvv

            # Relevant variables from Utils.embed as well as other called functions
            embed, view, part_1, part_2 = await Utils.embed()

            # Sending the initial embed
            sent_msg = await message.channel.send(embed=embed, view=view)

            # Deleting it after x seconds
            await asyncio.sleep(30)
            await sent_msg.delete()

            # Sending embed with results from vote
            tally_embed = await Utils.tallying(part_1=part_1, part_2=part_2)
            sent_tally = await message.channel.send(embed=tally_embed)

            # Deleting it after x seconds
            await asyncio.sleep(15)
            await sent_tally.delete()

            # Resetting variables
            message_counts[channel_id] = 0
            last_message_times[channel_id] = time.time()

        else:
            message_counts[channel_id] = 0

    # Store the user ID and timestamp of the message
    # print(last_message_times) (for debug purposes)


load_dotenv()
client.run(os.getenv("TOKEN"), log_level=logging.INFO)
