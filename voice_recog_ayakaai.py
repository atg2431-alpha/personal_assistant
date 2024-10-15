import speech_recognition as sr
import os
import webbrowser
import pyttsx3

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Function to convert text to speech and speak it
def say(text):
    engine.say(text)
    engine.runAndWait()

# Function to capture voice command
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.5
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            query = "Sorry, I could not understand you"
            return query
        except sr.RequestError:
            query = "Sorry, there was an issue with the speech recognition service"
            return query

# Main loop for listening and responding
say("Hello Anshuman, I am Jarvis AI")
while True:
    print("Listening...")
    s = takeCommand()
    if "Open YouTube".lower() in s.lower():
        say("Opening YouTube, Sir")
        webbrowser.open("https://www.youtube.com")
    elif "Open Spotify".lower() in s.lower():
        say("Opening Spotify, Sir")
        webbrowser.open("https://www.spotify.com")
    elif "Open WhatsApp".lower() in s.lower():
        say("Opening WhatsApp, Sir")
        webbrowser.open("https://web.whatsapp.com")
    else:
        say("You said: " + s)
