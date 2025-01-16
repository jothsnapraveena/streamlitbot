import os
import tempfile
import pygame
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables


os.environ['OPENAI_API_KEY'] = st.secrets["OPENAI_API_KEY"]

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o")  

# Function: Speech-to-Text (STT)
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak.")
        try:
            audio = recognizer.listen(source, timeout=10)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that. Please try again."
        except sr.RequestError as e:
            return f"Error with the speech recognition service: {e}"
        except Exception as e:
            return f"An error occurred: {e}"

# Function: Text-to-Speech (TTS) with Auto Playback
def text_to_speech(text):
    # Convert text to speech and save to a temporary MP3 file
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        temp_file = fp.name  # Save the file path for later use

    try:
        # Initialize pygame mixer
        pygame.mixer.init()
        # Load and play the audio file
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()

        # Wait until playback is finished
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # Prevent busy looping

        # Properly stop and quit the mixer after playback
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    finally:
        # Ensure file is deleted after it is no longer in use
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except PermissionError:
                st.warning(f"Could not delete temporary file: {temp_file}. It might still be in use.")

# Streamlit App UI
st.title("Voice Conversation with LLM")
st.markdown("### Speak to the bot and have a fully voice-based conversation!")

# Continuous conversation loop
if st.button("Start Voice Conversation"):
    st.write("**Voice Conversation Started! Speak your question now.**")
    while True:
        # User speaks
        user_input = recognize_speech()
        if user_input:
            st.write(f"**You said:** {user_input}")

            # Exit condition for the loop
            if "exit" in user_input.lower() or "stop" in user_input.lower():
                st.write("Ending conversation. Goodbye!")
                text_to_speech("Ending conversation. Goodbye!")
                break

            # Query the LLM directly
            bot_reply = llm.predict(user_input)
            st.write(f"**Bot says:** {bot_reply}")

            # Bot responds with voice
            text_to_speech(bot_reply)
