import pyttsx3
import speech_recognition as sr
from loguru import logger


# Initialize the voice engine globally
engine = pyttsx3.init()

# Set Female Voice
voices = engine.getProperty("voices")
for voice in voices:
    if "female" in voice.name.lower():
        engine.setProperty("voice", voice.id)
        break  # Use the first female voice found

# Adjust Pitch (Only for eSpeak)
engine.setProperty("rate", 200)  # Speech speed
engine.setProperty("volume", 0.50)  # Full volume
engine.setProperty("pitch", 200)  # Higher pitch for a more feminine sound (only works in eSpeak)

def assistant_voice(message):
    """Speaks the given message using text-to-speech."""
    engine.say(message)
    engine.runAndWait()
    logger.info(f"Spoke: {message}")

def listen_instruction():
    """Listens for a voice command and returns the recognized text."""
    rec_voice = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Ready for instruction...")
        try:
            audio = rec_voice.listen(source, timeout=3, phrase_time_limit=5)
            instruction = rec_voice.recognize_google(audio)
            print(f"🗣 Identified instruction: {instruction}")
            logger.info(f"Recognized command: {instruction}")
            return instruction.lower()

        except sr.UnknownValueError:
            assistant_voice("I did not understand the instruction. Please try again.")
            logger.warning("Could not understand audio")
            return None

        except sr.WaitTimeoutError:
            assistant_voice("No instruction detected.")
            logger.warning("No instruction detected")
            return None
