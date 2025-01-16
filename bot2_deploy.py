# import os
# import tempfile
# import streamlit as st
# from gtts import gTTS
# from streamlit_mic_recorder import speech_to_text  # For speech-to-text functionality
# from langchain_openai import ChatOpenAI

# # Ensure OpenAI API Key
# if "OPENAI_API_KEY" not in st.secrets:
#     st.error("OpenAI API key not found in secrets. Please configure it in the Streamlit Cloud settings.")
#     st.stop()

# # Initialize the LLM
# llm = ChatOpenAI(model="gpt-4o", api_key=st.secrets["OPENAI_API_KEY"])

# # Function: Text-to-Speech (TTS)
# def text_to_speech(text):
#     tts = gTTS(text)
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
#         tts.save(fp.name)
#         st.audio(fp.name, format="audio/mp3")

# # Streamlit App UI
# st.title("Voice-Enabled AI Assistant")
# st.markdown("### Speak to the assistant and receive voice responses.")

# # Continuous conversation loop
# if st.button("Start Voice Conversation"):
#     st.write("**Voice Conversation Started! Speak your question now.**")

#     # Record and transcribe speech using streamlit_mic_recorder
#     user_input = speech_to_text()
#     if user_input:
#         st.write(f"**You said:** {user_input}")

#         # Exit condition
#         if "exit" in user_input.lower() or "stop" in user_input.lower():
#             st.write("Ending conversation. Goodbye!")
#             text_to_speech("Ending conversation. Goodbye!")
#         else:
#             # Query the LLM and get the bot's reply
#             response = llm.predict(user_input)
#             st.write(f"**Assistant says:** {response}")

#             # Play bot's response as audio
#             text_to_speech(response)

import os
import tempfile
import streamlit as st
from gtts import gTTS
from streamlit_mic_recorder import speech_to_text  # For speech-to-text functionality
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

# Continuous conversation loop
if st.button("Start Voice Conversation"):
    st.write("**Voice Conversation Started! Speak your question now.**")

    # Record and transcribe speech using streamlit_mic_recorder
    s2t_output = speech_to_text(
        language='en',
        start_prompt="⭕ TALK",
        stop_prompt="🟥 LISTENING...PRESS TO STOP",
        just_once=True,
        use_container_width=True,
        callback=None,
        args=(),
        kwargs={},
        key=None
    )

    if s2t_output:
        st.write(f"**You said:** {s2t_output}")

        # Exit condition
        if "exit" in s2t_output.lower() or "stop" in s2t_output.lower():
            st.write("Ending conversation. Goodbye!")
            text_to_speech("Ending conversation. Goodbye!")
        else:
            # Query the LLM and get the bot's reply
            response = llm.predict(s2t_output)
            st.write(f"**Assistant says:** {response}")

            # Play bot's response as audio
            text_to_speech(response)
