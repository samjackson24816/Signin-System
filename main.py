import time
from datetime import datetime


import remote_data
import remote_recorder
from local_data import get_user_data, log_input


def handle_card_input(input_str: str):
    # TODO: sanitize the input data
    user_id = input_str
    print("Read input " + user_id)

    name, signed_in = get_user_data(user_id)

    match name:
        case None:
            print(
                "This card is not linked to a name.  If you want to add this card to the database, add it into the "
                "spreadsheet.")

        case _:
            name = str(name)
            print("Hello " + name)

            match signed_in:
                case False:
                    print("You are now signed in")
                case True:
                    print("You are now signed out")

    log_input(user_id)



SAVE_SPACE_SECONDS = 5 


def run_input():
    print("Program running --- press ESC to quit")

    saving = {"val": False}
    remote_recorder.start_saving(saving, SAVE_SPACE_SECONDS)

    while True:
        
        instr = ""

        got_input = False

        while not got_input:

            try:
                instr = input()
                got_input = True
            except KeyboardInterrupt:
                print("Quitting program")
                exit()

        while saving["val"]:
            try:
                pass
            except KeyboardInterrupt:
                print("Quitting program")
                exit()

        handle_card_input(str(instr))

if __name__ == "__main__":
    run_input()
