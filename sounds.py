import os
import playsound3
from gtts import gTTS
from threading import Thread


class Sound:
    """
    A base class meant to be overridden by actual sound types
    """

    def play(self):
        pass


class TextToSpeech(Sound):
    """
    A sound type that says text with the Google TTS api
    """

    text: str

    def __init__(self, tts_text: str):
        self.text = str(tts_text)

    def play(self):
        if len(self.text) == 0:
            print("The input text to the TTS object is empty")
            return

        filename = self.text.encode('UTF-8').hex()
        if os.path.exists(f'./tts/{filename}.mp3'):
            pass
        else:
            try:
                tts = gTTS(self.text, lang='en', slow=False)
                tts.save(f'./tts/{filename}.mp3')
            except:
                print("Text to speech is not working.  It might need internet, or something else might be broken.")
                print(text)

        playsound3.playsound(f'./tts/{filename}.mp3', True)


class SoundEffect(Sound):
    """
    A sound type that plays an mp3 file in the \"sfx\" folder by name
    """
    sound_name: str

    def __init__(self, sound_name):
        self.sound_name = sound_name

    def play(self):
        if len(self.sound_name) == 0:
            print("WARNING: The name of the sound effect inputted to the SoundEffect object is empty")
            return

        sound_path = './sfx/' + self.sound_name + '.mp3'
        if not os.path.exists(sound_path):
            print(f"WARNING: The sound effect \"{sound_path}\" does not exist")
            return

        try:
            playsound3.playsound(sound_path, True)
        except:
            print("The sound effect player doesn't seem to be working.  Try restarting the program to get audio.")


def play_sounds(sound_queue: list[Sound]):
    """
    An endless loop meant to be run on a separate thread that continuously looks for new elements on the sound queue
    and plays them one by one.
    :param sound_queue: a list of sounds, which will be removed and played through starting at the end
    """
    while True:
        if len(sound_queue) > 0:
            sound = sound_queue.pop()
            sound.play()


class Audio:
    """
    An Audio object manages a queue of Sound objects, playing them one at a time asynchronously in another thread. To
    add a sound to be played after the current sounds finish, call the queue_sound() method.  Once all the other
    sounds ahead in the queue have been played, one after another, your sound will be played.
    """

    audio_thread: Thread

    sound_queue = list[Sound]()

    def __init__(self):
        audio_queue = Thread(target=play_sounds, args=[self.sound_queue])

        audio_queue.start()

    def queue_sound(self, sound: Sound):
        self.sound_queue.insert(0, sound)


def test_audio():
    audio = Audio()

    text = TextToSpeech("Hello world")

    audio.queue_sound(text)
    print("Will say 'how are you?' after hello world is done")

    text2 = TextToSpeech("How are you?")

    audio.queue_sound(text2)

    audio.queue_sound(SoundEffect("noname"))

    audio.queue_sound(SoundEffect("broken"))
    audio.queue_sound(SoundEffect(""))

    audio.queue_sound(TextToSpeech("yo"))
    audio.queue_sound(TextToSpeech(""))
