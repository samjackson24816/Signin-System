from datetime import datetime
from enum import Enum
import random
import keyboard
import json
import easygui
import pygsheets
import playsound3

SIGNIN_SOUND = './signin.mp3'
SIGNOUT_SOUND = './signout.mp3'
NO_NAME_SOUND = './noname.mp3'

try:
    client = pygsheets.authorize(service_file='./service-account-key.json')
except E as e:
    print("Google Client was not authorized.  Check the error below:")
    print(e)
    quit(1)

sh = client.open_by_key("13a-zji7i5hih5loJxG55xtRv_mPDe2VjCdHcyz-XXCU")
add_data_ws = sh.worksheet_by_title("RFID Input")
names_and_ids_ws = sh.worksheet_by_title("Names & IDs")
dashboard_ws = sh.worksheet_by_title("Dashboard")


def add_row_to_sheet(time, name):
    # I'm doing it this way because this sheet currently has wierd hacky stuff going on in it.  Once I fix the sheet,
    # this should be done with the append function
    rows = add_data_ws.rows

    vals = add_data_ws.get_values('B2', 'B' + str(rows))

    # The sheet is 1-indexed, and we want the row after the current last one
    idx = len(vals) + 2

    add_data_ws.update_value("A" + str(idx), time)

    add_data_ws.update_value("B" + str(idx), name)

    return


def get_name_of_id(user_id: str) -> str | None:
    rows = names_and_ids_ws.rows
    vals = names_and_ids_ws.get_values("A1", "A" + str(rows))

    for i in range(len(vals)):
        e = vals[i][0]
        if e != user_id:
            continue

        name = str(names_and_ids_ws.get_value("B" + str(i + 1)))
        return name
    return None


def get_login_status(name: str) -> bool:
    rows = dashboard_ws.rows
    vals = dashboard_ws.get_values("A1", "A" + str(rows))

    for i in range(len(vals) + 1):
        e = vals[i][0]
        if e != name:
            continue

        status = str(dashboard_ws.get_value("B" + str(i + 1)))
        match status:
            case "Yes":
                return True
            case "No":
                return False
            case _:
                print("Error: The status column must be Yes or No")
                exit(1)


def play_sound(sound: str):
    try:
        playsound3.playsound(sound, False)
    except:
        print("Audio doesn't seem to be working.  Try restarting the program to get audio.")


def log_card(user_id: str) -> None:
    print("Read input " + user_id)
    name = get_name_of_id(user_id)

    match name:
        case None:
            print(
                "This card is not linked to a name.  If you want to add this card to the database, add it into the "
                "spreadsheet.")
            play_sound(NO_NAME_SOUND)

        case _:
            name = str(name)
            print("Welcome " + name)
            signed_in = get_login_status(name)
            match signed_in:
                case False:
                    print("You are now signed in")
                    play_sound(SIGNIN_SOUND)
                case True:
                    print("You are now signed out")
                    play_sound(SIGNOUT_SOUND)

    post_user_change(user_id)


def post_user_change(user_id: str):
    now = str(datetime.now())
    add_row_to_sheet(now, user_id)


def handle_card_input(input_str: str):
    # We don't sanitize the input data because I don't feel like doing that right now
    if input_str is None: return
    user_id = str(input_str)

    log_card(user_id)
    name = get_name_of_id(user_id)


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
