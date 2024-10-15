import speech_recognition as sr
import webbrowser
import pyttsx3

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech and speak it."""
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    """Capture voice command and recognize it."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.5
        print("Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I could not understand you")
            return ""
        except sr.RequestError:
            print("Sorry, there was an issue with the speech recognition service")
            return ""

def start_speech_recognition():
    """Main loop for listening and responding to commands."""
    speak("Hello Anshuman, I am Jarvis AI")
    while True:
        s = takeCommand()
        if "open youtube" in s.lower():
            speak("Opening YouTube, Sir")
            webbrowser.open("https://www.youtube.com")
        elif "open spotify" in s.lower():
            speak("Opening Spotify, Sir")
            webbrowser.open("https://www.spotify.com")
        elif "open whatsapp" in s.lower():
            speak("Opening WhatsApp, Sir")
            webbrowser.open("https://web.whatsapp.com")
        elif s:  # Only respond if there's a command
            speak("You said: " + s)

def stop_speech_recognition():
    """Logic to stop speech recognition (currently a placeholder)."""
    pass  # Implement stopping logic if needed

# Example of starting the speech recognition
if __name__ == "__main__":
    start_speech_recognition()
