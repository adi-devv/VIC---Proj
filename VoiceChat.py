import win32com.client
import speech_recognition as sr
import VIC, os

speaker = win32com.client.Dispatch('SAPI.SpVoice')
speaker.Voice = speaker.GetVoices().Item(1)


def say(w):
    print(w)
    speaker.Speak(w)


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone(
            device_index=sr.Microphone.list_microphone_names().index('Headset (realme Buds T300)')) as mic:
        r.pause_threshold = 1
        audio = r.listen(mic)
        try:
            print('Recognizing...')
            q = r.recognize_google(audio, language='en-in')
            print(f'User said: {q}')
            return q
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None


def process(q):
    if kw in q:
        if 'lock' in q:
            VIC.lock_windows()

    if 'search' in q:
        txt = q.split('search', 1)[1].strip()
        if txt == '': return
        say("Searching: " + txt)
        VIC.search(txt)

    if 'start' in q:
        app = q.split('start', 1)[1].strip()
        if app == '': return
        say("Starting: " + app)
        os.system(f'start {app}')

    if 'open' in q:
        site = q.split('open', 1)[1].strip()
        if site == '': return
        say("Opening: " + site)
        VIC.searchw(site)


if __name__ == '__main__':
    say('Initiating Script')
    kw = 'hp '
    while True:
        print('Listening...')
        query = takeCommand()
        if not query: continue
        process(query.lower())
