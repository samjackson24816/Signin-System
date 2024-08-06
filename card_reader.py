import os
from datetime import datetime
import keyboard
import pygsheets
import playsound3
from gtts import gTTS

from sounds import *

try:
    client = pygsheets.authorize(service_file='./service-account-key.json')
except:
    print("Google Client was not authorized.  Check the error below:")
    print(Exception)
    quit(1)

sh = client.open_by_key("13a-zji7i5hih5loJxG55xtRv_mPDe2VjCdHcyz-XXCU")
add_data_ws = sh.worksheet_by_title("RFID Input")
names_and_ids_ws = sh.worksheet_by_title("Names & IDs")
form_input_ws = sh.worksheet_by_title("Form Input")

audio = Audio()

audio.queue_sound(TextToSpeech("Signin system activated"))


def add_row_to_sheet(time, name):
    rows = add_data_ws.rows

    vals = add_data_ws.get_values('B2', 'B' + str(rows))

    # The sheet is 1-indexed, and we want the row after the current last one
    idx = len(vals) + 2

    add_data_ws.update_value("A" + str(idx), time)
    add_data_ws.update_value("B" + str(idx), name)
    return


def search_sheet(ws, keys: list[str], key_col: str, val_col: str) -> list[str]:
    rows = ws.rows
    key_list = ws.get_values(str(key_col) + "1", str(key_col) + str(rows))

    stuff = list()

    for i in range(len(key_list)):
        element = str(key_list[i][0])
        if element in keys:
            stuff.append(ws.get_value(str(val_col) + str(i + 1)))

    return stuff


def get_name_of_id(user_id: str) -> str | None:
    names = search_sheet(names_and_ids_ws, [user_id], "A", "B")

    if len(names) > 0:
        return names[0]
    else:
        return None


def get_all_ids(name: str) -> list[str]:
    return search_sheet(names_and_ids_ws, [name], "B", "A")


def get_login_status(user_ids: list[str]) -> bool:
    form_data = search_sheet(form_input_ws, user_ids, "B", "B")
    rfid_data = search_sheet(add_data_ws, user_ids, "B", "B")

    datapoints = len(form_data) + len(rfid_data)

    return datapoints % 2 == 1


def post_user_change(user_id: str):
    now = str(datetime.now())
    add_row_to_sheet(now, user_id)


def handle_card_input(input_str: str):
    # TODO: sanitize the input data
    user_id = input_str
    print("Read input " + user_id)

    name = get_name_of_id(user_id)

    match name:
        case None:
            print(
                "This card is not linked to a name.  If you want to add this card to the database, add it into the "
                "spreadsheet.")
            audio.play_sound('noname')
            audio.say(
                "This card is not linked to a name.  If you want to add this card to the database, add it into the "
                "spreadsheet.")

        case _:
            name = str(name)
            print("Hello " + name)
            text_to_say = "Hello " + name + "! "

            ids = get_all_ids(name)

            signed_in = get_login_status(ids)

            match signed_in:
                case False:
                    print("You are now signed in")
                    audio.play_sound('signin')
                    text_to_say += "You are now signed in"
                case True:
                    print("You are now signed out")
                    audio.play_sound('signout')
                    text_to_say += "You are now signed out"

            audio.say(text_to_say)

    # We do this regardless of whether the input is linked to a name so we can see the invalid inputs on sheet and debug if there are problems
    post_user_change(user_id)


while True:
    instr = ""
    while True:
        event = keyboard.read_event()
        if event.event_type == 'down' or None: continue

        char = event.name

        if char is None: continue

        if char == "enter" and len(instr) > 0: break

        if len(char) > 1: continue
        if not char.isalnum(): continue

        instr += char

        print(char)

    # Once we get a full input
    handle_card_input(str(instr))
