import os
import tempfile
import streamlit as st
from gtts import gTTS
from langchain_openai import ChatOpenAI
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import numpy as np
import soundfile as sf
import speech_recognition as sr

# Ensure OpenAI API Key
if "OPENAI_API_KEY" not in st.secrets:
    st.error("OpenAI API key not found in secrets. Please configure it in the Streamlit Cloud settings.")
    st.stop()

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o", api_key=st.secrets["OPENAI_API_KEY"])

# Function: Text-to-Speech (TTS)
def text_to_speech(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3")

# Class: Audio Processor for WebRTC
class SpeechProcessor(AudioProcessorBase):
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recv(self, frame):
        audio_data = np.frombuffer(frame.to_ndarray().tobytes(), dtype=np.int16)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as fp:
            sf.write(fp.name, audio_data, samplerate=frame.sample_rate, subtype="PCM_16")
            try:
                with sr.AudioFile(fp.name) as source:
                    audio = self.recognizer.record(source)
                    return self.recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                return "Sorry, I couldn't understand that."
            except sr.RequestError as e:
                return f"Speech recognition service error: {e}"
            except Exception as e:
                return f"An error occurred: {e}"

# Streamlit App UI
st.title("Voice Conversation with LLM")
st.markdown("### Speak to the bot and have a fully voice-based conversation!")

# WebRTC for microphone input
webrtc_ctx = webrtc_streamer(
    key="speech-to-text",
    mode="recvonly",
    client_settings={
        "rtcConfiguration": {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        "media_stream_constraints": {"audio": True, "video": False},
    },
    audio_processor_factory=SpeechProcessor,
)

if webrtc_ctx and webrtc_ctx.state.playing:
    st.info("Listening... Please speak into your microphone.")
    user_input = webrtc_ctx.audio_processor.recv()
    if user_input:
        st.write(f"**You said:** {user_input}")

        # Exit condition
        if "exit" in user_input.lower() or "stop" in user_input.lower():
            st.write("Ending conversation. Goodbye!")
            text_to_speech("Ending conversation. Goodbye!")

        # Query the LLM and respond
        bot_reply = llm.predict(user_input)
        st.write(f"**Bot says:** {bot_reply}")

        # Play bot's response as audio
        text_to_speech(bot_reply)
