import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Use the default microphone as the audio source
with sr.Microphone() as source:
    print("Listening...")
    audio = recognizer.listen(source)  # Capture the audio from the mic

    try:
        # Recognize speech using Google Web Speech API
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio.")
    except sr.RequestError:
        print("Request error. Check your internet connection.")
