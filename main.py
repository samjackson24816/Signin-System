import time
from datetime import datetime

import keyboard

import remote_data
import remote_recorder
from local_data import get_user_data, log_input
from sounds import SoundPlayer, Sound

player = SoundPlayer()

player.push_sound(Sound(Sound.SoundType.TTS, "Signin System Activated"))


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
            player.push_sound(Sound(Sound.SoundType.SFX, "noname"))

            player.queue_sound(Sound(Sound.SoundType.TTS,
                "This card is not linked to a name.  If you want to add this card to the database, add it into the "
                "spreadsheet."))

        case _:
            name = str(name)
            print("Hello " + name)
            text_to_say = "Hello " + name + "! "

            match signed_in:
                case False:
                    print("You are now signed in")
                    player.push_sound(Sound(Sound.SoundType.SFX, 'signin'))
                    text_to_say += "You are now signed in"
                case True:
                    print("You are now signed out")
                    player.push_sound(Sound(Sound.SoundType.SFX, 'signout'))
                    text_to_say += "You are now signed out"

            player.queue_sound(Sound(Sound.SoundType.TTS, text_to_say))

    log_input(user_id)


SAVE_SPACING_SECONDS = 10

def run_input():
    print("Program running --- press ESC to quit")

    saving = {"val": False}
    remote_recorder.start_saving(saving)

    while True:
        instr = ""
        '''
        while True:

            try:
                event = keyboard.read_event()
                print(event.name)


                if event.name == 'esc' or event.name == 'caps lock':
                    print("Pressed ESC --- quitting immediately")
                    quit(0)


                if event.event_type == 'down' or None: continue

                char = event.name

                if char is None: continue

                if char == "enter" and len(instr) > 0: break

                if len(char) > 1: continue
                if not char.isalnum(): continue

                instr += char

            except KeyboardInterrupt as e:
                print("Keyboard Interrupt --- quitting immediately")
                quit(0)

        '''

        # Once we get a full input
        instr = input()

        while saving["val"]:
            pass

        handle_card_input(str(instr))


if __name__ == "__main__":
    run_input()
