import os
import wave
from enum import Enum
from time import sleep
import sys
import contextlib
from pydub import AudioSegment
from gtts import gTTS
from threading import Thread
import pyaudio
from playsound3 import playsound3


@contextlib.contextmanager
def ignoreStderr():
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_stderr, 2)
        os.close(old_stderr)


class Flag:
    state: bool

    def __init__(self, state: bool):
        self.state = state

    def get_state(self) -> bool:
        return self.state

    def set_state(self, state: bool):
        self.state = state



class Sound:

    class SoundType(Enum):
        TTS = 0
        SFX = 1

    sound_type: SoundType
    text: str

    def __init__(self, sound_type: SoundType, text: str):
        self.sound_type = sound_type
        self.text = text

    def __eq__(self, other) -> bool:
        if type(self) is not type(other):
            return False

        return self.sound_type == other.sound_type and self.text == other.text



class AudioInterface:

    audio_thread: Thread

    p: pyaudio.PyAudio

    def __init__(self):
        # audio_queue = Thread(target=play_sounds, args=[self.sound_queue])

        # audio_queue.daemon = True
        # audio_queue.start()

        # We do this to ignore all of the error messages that are generated.
        # The object works, but it gives as a bunch of notifications about bluetooth, etc, unless we do this.
        with ignoreStderr():
            self.p = pyaudio.PyAudio()


    def play_wav(self, filename: str, end: Flag):
        wf = wave.open(filename, 'rb')
        stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(1024)

        while data and not end.get_state():
            stream.write(data)
            data = wf.readframes(1024)
            #print(f"Flag: {end.get_state()}")

        stream.stop_stream()
        stream.close()
        return


def play_sound(audio: AudioInterface, sound: Sound, end: Flag):

        match sound.sound_type:
            case Sound.SoundType.SFX:
                if len(sound.text) == 0:
                    print("WARNING: The name of the sound effect inputted to the SoundEffect object is empty")
                    return

                sound_path = './sfx/' + sound.text + '.wav'
                if not os.path.exists(sound_path):
                    print(f"WARNING: The sound effect \"{sound_path}\" does not exist")
                    return

                try:
                    audio.play_wav(sound_path, end)
                except Exception as e:
                    print("WARNING: The sound effect player doesn't seem to be working.  Try restarting the program to get audio.")
                    print(e)

            case Sound.SoundType.TTS:

                if len(sound.text) == 0:
                    print("The input text to the TTS object is empty")
                    return

                filename = sound.text.encode('UTF-8').hex()

                path = f"./tts/{filename}"

                if os.path.exists(path):
                    pass
                else:
                    try:
                        tts = gTTS(sound.text, lang='en', slow=False, tld='com.au')

                        tts.save(path + ".mp3")

                        sound = AudioSegment.from_mp3(path + ".mp3")
                        sound.export(path + ".wav", format="wav")
                        os.remove(path + ".mp3")
                    except:
                        print("WARNING: Text to speech is not working.  It might need internet, or something else might be broken.")
                        print(sound.text)

                try:
                    audio.play_wav(path + ".wav", end)
                except:
                    print("WARNING: The audio player doesn't seem to be working. Try restarting the program to get audio.")


def play_sounds_thread(audio: AudioInterface, sounds: list[Sound]):
        sound_thread: Thread | None = None
        current_sound: Sound | None = None
        end: Flag = Flag(False)

        while True:
            if len(sounds) > 0 and not current_sound == sounds[0]:
                if sound_thread is not None:
                    end.set_state(True)
                    sound_thread.join()
                    end.set_state(False)
                    print("Interrupted sound")

                current_sound = sounds[0]
                sound_thread = Thread(target=play_sound, args=[audio, current_sound, end])
                sound_thread.start()
                print("Started sound")

            if len(sounds) > 0 and end.get_state() == False and sound_thread is not None and not sound_thread.is_alive():
                print("Finished sound")
                sounds.pop(0)


class SoundPlayer:
    audio: AudioInterface

    sounds: list[Sound]

    sound_thread: Thread


    def __init__(self):
        self.audio = AudioInterface()
        self.sounds = list[Sound]()

        def sound_thread_target():
            play_sounds_thread(self.audio, self.sounds)

        self.sound_thread = Thread(target=sound_thread_target)
        self.sound_thread.daemon = True
        self.sound_thread.start()

    def queue_sound(self, sound: Sound):
        self.sounds.append(sound)

    def push_sound(self, sound: Sound):
        self.sounds.clear()
        self.sounds.append(sound)



def audio_test():
    player = SoundPlayer()

    player.push_sound(Sound(Sound.SoundType.TTS, "hellohellohellohellohellohello"))
    sleep(2)
    player.push_sound(Sound(Sound.SoundType.TTS, "world"))
    sleep(8)

