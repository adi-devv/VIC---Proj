import win32com.client
import speech_recognition as sr
import os
from predefined import Predefined  # Assuming 'Predefined' class is in a file named 'predefined.py'


def take_command():
    r = sr.Recognizer()
    mic_index = sr.Microphone.list_microphone_names().index('Headset (realme Buds T300)')
    with sr.Microphone(device_index=mic_index) as mic:
        r.pause_threshold = .6
        audio = r.listen(mic)
        try:
            print('Recognizing...')
            q = r.recognize_google(audio, language='en-in')
            print(f'User said: {q}')
            return q
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
    return None


class VoiceAssistant:
    def __init__(self):
        self.speaker = win32com.client.Dispatch('SAPI.SpVoice')
        self.speaker.Voice = self.speaker.GetVoices().Item(1)
        self.vic = Predefined()
        self.kw = 'hp'

    def say(self, w):
        print(w)
        self.speaker.Speak(w)

    def process(self, q):
        if self.kw in q:
            if 'lock' in q:
                self.vic.initiate_lock()

        elif 'search' in q:
            txt = q.split('search', 1)[1].strip()
            if txt:
                self.say("Searching: " + txt)
                self.vic.search(txt)

        elif 'start' in q:
            app = q.split('start', 1)[1].strip()
            if app:
                self.say("Starting: " + app)
                os.system(f'start {app}')

        elif 'open' in q:
            site = q.split('open', 1)[1].strip()
            if site:
                self.say("Opening: " + site)
                self.vic.search(site, True)

    def run(self):
        self.say('Initiating Script')
        while True:
            print('Listening...')
            query = take_command()
            if query:
                self.process(query.lower())


if __name__ == '__main__':
    assistant = VoiceAssistant()
    assistant.run()
