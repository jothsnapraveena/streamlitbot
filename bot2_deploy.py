import os
import tempfile
import streamlit as st
from gtts import gTTS
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from langchain_openai import ChatOpenAI

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

# Streamlit App UI
st.title("Voice-Enabled AI Assistant")
st.markdown("### Speak to the assistant and receive voice responses.")

# Implement WebRTC for capturing audio
if st.button("Start Voice Conversation"):
    st.write("**Voice Conversation Started! Speak your question now.**")
    
    webrtc_ctx = webrtc_streamer(
        key="speech-to-text",
        mode=WebRtcMode.RECVONLY,
        client_settings={
            "rtcConfiguration": {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            "media_stream_constraints": {"audio": True, "video": False},
        },
    )

    if webrtc_ctx and webrtc_ctx.state.playing:
        st.info("Listening... Please speak into your microphone.")
        # Simulate transcription for now (integrate proper transcription logic here)
        user_input = "This is a test transcription."

        if user_input:
            st.write(f"**You said:** {user_input}")
            if "exit" in user_input.lower() or "stop" in user_input.lower():
                st.write("Ending conversation. Goodbye!")
                text_to_speech("Ending conversation. Goodbye!")
            else:
                response = llm.predict(user_input)
                st.write(f"**Assistant says:** {response}")
                text_to_speech(response)
