import datetime
import random


strings = ["a", "b", "c", "d"]
sent_strings = []


def send(user_input):
    print(f"[INFO] - {datetime.datetime.now().strftime('%H:%M:%S')} - " + user_input)


def send_random_string():
    if len(sent_strings) == len(strings):
        sent_strings.clear()
        # All strings have been sent, clear the sent_strings list

    # Get the remaining unsent strings
    remaining_strings = list(set(strings) - set(sent_strings))
    # Shuffle the remaining strings
    random.shuffle(remaining_strings)

    # Select the first string from the shuffled list
    string_to_send = remaining_strings[0]
    # Add the sent string to the sent_strings list
    sent_strings.append(string_to_send)

    return "Would you rather " + string_to_send
