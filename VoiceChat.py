import win32com.client
import speech_recognition as sr

speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Voice = speaker.GetVoices().Item(1)


def say(w):
    speaker.Speak(w)


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as mic:
        r.pause_threshold = 1
        audio = r.listen(mic)
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        return query


# takeCommand()

if __name__ == "__main__":
    say("Initiating Script")
    while True:
        print("Listening..")
        text = takeCommand()
        say(text)
