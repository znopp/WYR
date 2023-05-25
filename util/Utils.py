import datetime
import random
import discord

strings = ["Never sleep", "Be the richest person alive"]
strings_2 = ["Never eat", "Be immortal forever"]

used_strings = []
user_id_list = {}


def send(user_input):
    print(f"[INFO] - {datetime.datetime.now().strftime('%H:%M:%S')} - " + user_input)


def send_random_string():
    if len(used_strings) == len(strings):
        used_strings.clear()
        # All strings have been sent, clear the sent_strings list

    # Get the remaining unsent strings
    remaining_strings = list(set(strings) - set(used_strings))
    # Shuffle the remaining strings
    random.shuffle(remaining_strings)
    shuffled_strings_2 = [strings_2[strings.index(string)] for string in remaining_strings]

    # Select the first string from the shuffled list
    string_to_send = f"{remaining_strings[0]} or {shuffled_strings_2[0].lower()}"
    # Add the sent string to the sent_strings list
    used_strings.append(string_to_send)

    return string_to_send, remaining_strings, shuffled_strings_2


async def handle_button_click(interaction: discord.Interaction, button: discord.ui.Button):

    user_id = interaction.user.id
    button_label = button.label

    label_text = button_label[0] + button_label[1:].lower()

    if user_id in user_id_list:
        previous_button = user_id_list[user_id]
        if previous_button == button_label.lower():
            await interaction.response.send_message("You have already pressed this button!", ephemeral=True)
        else:
            await interaction.response.send_message(f"Changing result to the {label_text}", ephemeral=True)
            user_id_list[user_id] = button_label.lower()
    else:
        await interaction.response.send_message(f"Your ID is {user_id},"
                                                f" and you voted for the {label_text}!", ephemeral=True)
        user_id_list[user_id] = button_label.lower()

    print(user_id_list)


class ButtonClass(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="First Option", style=discord.ButtonStyle.blurple)
    async def first_option_click(self, interaction: discord.Interaction, button: discord.ui.Button):
        await handle_button_click(interaction, button)

    @discord.ui.button(label="Second Option", style=discord.ButtonStyle.red)
    async def second_option_click(self, interaction: discord.Interaction, button: discord.ui.Button):
        await handle_button_click(interaction, button)


async def embed():
    msg_embed = discord.Embed(title="Would you rather..?", color=0xda005d)
    string_to_send, remaining_strings, shuffled_strings_2 = send_random_string()
    msg_embed.description = string_to_send

    view = ButtonClass()

    return msg_embed, view, remaining_strings, shuffled_strings_2


async def tallying(remaining_strings, shuffled_strings_2):
    tallying_1 = 0
    tallying_2 = 0

    for item in user_id_list.values():
        if item == "first option":
            tallying_1 += 1
        else:
            tallying_2 += 1

    total = tallying_1 + tallying_2

    tallying_embed = discord.Embed(title="The results are in!", color=0xda005d)
    tallying_embed.description = f"{tallying_1} or {(tallying_1 / total) * 100}% " \
                                 f"of people voted for {remaining_strings[0]}, while " \
                                 f"{tallying_2} or {(tallying_2 / total) * 100}% " \
                                 f"of people voted for {shuffled_strings_2[0]}!"

    return tallying_embed
