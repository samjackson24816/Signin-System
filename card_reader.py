from enum import Enum
import keyboard
import json
import easygui

''' 
users.json is formatted like so:
{
    "123123": {
        "name": "Sam",
        "signed_in": false
    },
    "234234": {
        "name": "Bob",
        "signed_in": true
    }
}
'''


def load_users() -> dict:
    with open('users.json', 'r') as infile:
        users = dict(json.load(infile))
    return users


def save_users(users: dict):
    with open("users.json", "w") as outfile:
        json.dump(users, outfile, indent=4)


def get_user(users: dict, user_id: int) -> dict | None:
    val = users.get(str(user_id))
    if val is None:
        return None
    else:
        return dict(val)


def validate_input(input_str: str) -> str | None:
    # Clean and validate input
    cleaned_input = str.strip(str.lower(input_str))
    if not str.isalnum(cleaned_input):
        return None
    else:
        return input_str


def toggle_user(users: dict, user_id: int) -> dict:
    signed_in = not bool(users[str(user_id)]["signed_in"])
    users[str(user_id)]["signed_in"] = signed_in
    if signed_in:
        print("Signed in!")
    else:
        print("Signed out")

    return users


def new_user(users: dict, user_id: int):
    name = get_new_user(user_id)

    if name is not None:
        users[str(user_id)] = {
            "name": name,
            "signed_in": False
        }

    return users


def handle_given_id(users: dict, user_id: int) -> dict:
    user = get_user(users, user_id)
    if user is None:
        # New user
        users = new_user(users, user_id)

    else:
        # Toggle user state
        users = toggle_user(users, user_id)

    return users


def handle_card_input(input_str: str):
    user_id = validate_input(input_str)
    users = load_users()
    users = handle_given_id(users, user_id)
    save_users(users)


def start_reading_gui():
    pass


def start_reading_cli():
    print("Recording inputs")


def get_new_user_cli(user_id: int) -> str | None:
    add = input("User not found.  Add new user with id " + str(user_id) + "?\nEnter Y to continue: ")
    if not isinstance(add, str): return None
    if not str.capitalize(add) == "Y": return None

    name = input("Enter the new user's username: ")
    if not isinstance(name, str): return None

    print("New user added!  Name: " + name + "  Id: " + str(user_id))
    return name


def get_new_user_gui(user_id: int) -> str | None:
    add: bool = easygui.boolbox("User not found.  Add new user with id " + str(user_id) + "?", "User not found",
                                ["Add", "Cancel"], None, "Cancel", "Cancel")
    if not add: return None

    invar = easygui.enterbox("Enter the new user's username", "Add new user")

    if not isinstance(invar, str): return None

    return invar


Mode = Enum('Mode', ["CLI", "GUI"])

mode = Mode.CLI

get_new_user = None
start_reading = None

match mode:
    case Mode.CLI:
        get_new_user = get_new_user_cli
        start_reading = start_reading_cli
    case Mode.GUI:
        get_new_user = get_new_user_gui
        start_reading = start_reading_gui

while True:
    instr = ""
    start_reading()
    while True:
        event = keyboard.read_event()
        # print(event.event_type)
        if event.event_type == 'down' or None: continue

        char = event.name

        if char is None: continue

        if char == "enter" and len(instr) > 0: break

        if len(char) > 1: continue
        if not char.isalnum(): continue

        instr += char

        print(char)

    # Once we get a full input
    print(instr)
    handle_card_input(str(instr))
