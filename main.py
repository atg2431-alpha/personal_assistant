import voice_recognition  # Your voice recognition module
import finger_control  # Your finger control module
import threading

# Initialize flags for the functionalities
finger_active = False
speech_recognition_active = True  # Keep it active by default


def voice_command_handler():
    global finger_active, speech_recognition_active

    while True:
        command = voice_recognition.takeCommand()  # Function to get voice command
        if "activate finger" in command.lower():
            if not finger_active:
                finger_control.start_finger_control()  # Start finger control
                finger_active = True
                voice_recognition.speak("Finger control activated")
        elif "deactivate finger" in command.lower():
            if finger_active:
                finger_control.stop_finger_control()  # Stop finger control
                finger_active = False
                voice_recognition.speak("Finger control deactivated")
        elif "activate speech recognition" in command.lower():
            if not speech_recognition_active:
                voice_recognition.start_speech_recognition()  # Start speech recognition
                speech_recognition_active = True
                voice_recognition.speak("Speech recognition activated")
        elif "deactivate speech recognition" in command.lower():
            if speech_recognition_active:
                voice_recognition.stop_speech_recognition()  # Stop speech recognition
                speech_recognition_active = False
                voice_recognition.speak("Speech recognition deactivated")


# Run the voice command handler in a separate thread
threading.Thread(target=voice_command_handler, daemon=True).start()

# Keep the main program running
while True:
    pass  # Or perform other tasks
