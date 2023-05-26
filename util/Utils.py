import datetime
import json
import random
import discord

user_id_list = {}

now = datetime.datetime.now().strftime('%H:%M:%S')

with open("json/questions.json") as file:
    data = json.load(file)


def send(user_input):
    print(f"[INFO] - {now} - " + user_input)


def error(user_input):
    print(f"[ERROR] - {now} - " + user_input)


def send_random_string():

    random.shuffle(data)

    first_array = data[0]

    part_1 = first_array[0]

    part_2 = first_array[1]

    # Select the first string from the shuffled list
    string_to_send = f"{part_1} or {part_2.lower()}"

    return string_to_send, part_1, part_2


async def handle_button_click(interaction: discord.Interaction, button: discord.ui.Button, part_1, part_2):

    user_id = interaction.user.id

    if button.label == "First Option":
        button_label = part_1
    else:
        button_label = part_2

    label_text = button_label

    if user_id in user_id_list:
        previous_button = user_id_list[user_id]
        if previous_button == button_label.lower():
            await interaction.response.send_message("You have already pressed this button!", ephemeral=True)
        else:
            await interaction.response.send_message(f"Changing result to {label_text}!", ephemeral=True)
            user_id_list[user_id] = button_label.lower()
    else:
        await interaction.response.send_message(f"You voted for {label_text}!", ephemeral=True)
        user_id_list[user_id] = button_label.lower()

    # print(user_id_list) (for debug purposes)


class ButtonClass(discord.ui.View):
    def __init__(self, part_1, part_2):
        super().__init__()
        self.part_1 = part_1
        self.part_2 = part_2

    # Button 1, named First Option
    @discord.ui.button(label="First Option", style=discord.ButtonStyle.blurple)
    async def first_option_click(self, interaction: discord.Interaction, button: discord.ui.Button):
        await handle_button_click(interaction, button, self.part_1, self.part_2)

    # Button 2, named Second Option
    @discord.ui.button(label="Second Option", style=discord.ButtonStyle.red)
    async def second_option_click(self, interaction: discord.Interaction, button: discord.ui.Button):
        await handle_button_click(interaction, button, self.part_1, self.part_2)


async def embed():
    msg_embed = discord.Embed(title="Would you rather..?", color=0xda005d)
    string_to_send, part_1, part_2 = send_random_string()
    msg_embed.description = string_to_send
    msg_embed.set_footer(text="For help with issues, contact Nik#9121")

    view = ButtonClass(part_1, part_2)

    return msg_embed, view, part_1, part_2


async def tallying(part_1, part_2):
    tallying_1 = 0
    tallying_2 = 0

    for item in user_id_list.values():
        if item == "first option":
            tallying_1 += 1
        else:
            tallying_2 += 1

    total = tallying_1 + tallying_2

    tallying_embed = discord.Embed(title="The results are in!", color=0xda005d)

    if total != 0:
        tallying_embed.description = f"{tallying_1} or {(tallying_1 / total) * 100}% " \
                                     f"of people voted for {part_1}, while " \
                                     f"{tallying_2} or {(tallying_2 / total) * 100}% " \
                                     f"of people voted for {part_2}!"
        
        tallying_embed.set_footer(text="For help with issues, contact Nik#9121")

    else:
        tallying_embed.description = "Nobody voted! :("
        tallying_embed.set_footer(text="For help with issues, contact Nik#9121")

    user_id_list.clear()

    return tallying_embed
