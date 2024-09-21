import win32com.client
import speech_recognition as sr
import os
from predefined import Predefined
from gemapi import GemChat


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
            print("Google Speech Recogni tion could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
    return None


class VoiceAssistant:
    def __init__(self):
        self.speaker = win32com.client.Dispatch('SAPI.SpVoice')
        self.speaker.Voice = self.speaker.GetVoices().Item(1)
        self.vic = Predefined()
        self.gem = GemChat()
        self.kw = 'hp'

    def say(self, w):
        print(w)
        self.speaker.Speak(w[:50])

    def process(self, q):
        if self.kw in q and 'lock' in q:
            self.vic.initiate_lock()
            return

        actions = {
            'search': lambda txt: self.vic.search(txt.strip()) if txt else None,
            'start': lambda app: os.system(f'start {app.strip()}') if app else None,
            'open': lambda site: self.vic.search(site.strip(), True) if site else None
        }

        for action, func in actions.items():
            if action in q:
                t = q.split(action, 1)[1].strip()
                if t:
                    self.say(f"{action.capitalize()}ing: {t}")
                    func(t)
                return
        else:
            self.say(self.gem.sendmsg(q))

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
