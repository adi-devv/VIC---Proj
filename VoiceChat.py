import win32com.client
import speech_recognition as sr
from predefined import Predefined
from gemapi import GemChat


class VoiceAssistant:
    def __init__(self):
        self.speaker = win32com.client.Dispatch('SAPI.SpVoice')
        self.speaker.Voice = self.speaker.GetVoices().Item(1)
        self.recognizer = sr.Recognizer()
        self.vic = Predefined()
        self.gem = GemChat()
        self.kw = 'hp'

        self.languages = {
            'en-in': 'English (India)',
            'es-es': 'Spanish',
            'fr-fr': 'French',
            'de-de': 'German',
            'hi-in': 'Hindi'
        }
        self.current_language = 'en-in'

    def say(self, w):
        print(w)
        self.speaker.Speak(w[:50])

    def take_command(self):
        with sr.Microphone(device_index=None) as mic:
            self.recognizer.pause_threshold = 0.6
            self.recognizer.adjust_for_ambient_noise(mic, duration=1)

            try:
                audio = self.recognizer.listen(mic, timeout=5, phrase_time_limit=5)
                print('Recognizing...')
                for lang_code, lang_name in self.languages.items():
                    try:
                        query = self.recognizer.recognize_google(audio, language=lang_code)
                        print(f'User Said: {query}')
                        self.current_language = lang_code
                        self.say(f"I detected {lang_name}.")
                        return query.lower()
                    except sr.UnknownValueError:
                        continue  # Try next language
                self.say("Sorry, I couldn't understand the language.")
                return None
            except sr.WaitTimeoutError:
                print("Timed out waiting for speech. Retrying...")
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

    def process(self, q):
        if not q:
            return

        if self.kw in q and 'lock' in q:
            self.vic.initiate_lock()
            return

        actions = {
            'search': lambda txt: self.vic.search(txt.strip()) if txt else None,
            'start': lambda site: self.vic.open_app(site.strip()) if site else None,
            'open': lambda site: self.vic.search(site.strip(), True) if site else None,
        }

        for action, func in actions.items():
            if action in q:
                t = q.split(action, 1)[1].strip()
                if t:
                    self.say(f"{action.capitalize()}ing: {t}")
                    func(t)
                return

        # If no specific action matched, use the Gemini API
        self.say(self.gem.sendmsg(q))

    def change_language(self, lang_query):
        lang_map = self.languages
        for lang_code, lang_name in lang_map.items():
            if lang_name.lower() in lang_query or lang_code.split('-')[0] in lang_query:
                self.current_language = lang_code
                self.say(f"Language set to {lang_name} manually.")
                return True
        self.say("Sorry, I don't support that language yet.")
        return False

    def run(self):
        self.say('Initiating Script')
        while True:
            print('Listening..')
            query = self.take_command()
            if query:
                self.process(query.lower())


if __name__ == '__main__':
    assistant = VoiceAssistant()
    assistant.run()
