
import streamlit as st
from streamlit_mic_recorder import speech_to_text
import os
import tempfile
from gtts import gTTS
from langchain_openai import ChatOpenAI


#LLM Initialization
llm = ChatOpenAI(model="gpt-4o", api_key=st.secrets["OPENAI_API_KEY"])
if "OPENAI_API_KEY" not in st.secrets:
    st.error("OpenAI API key not found in secrets. Please configure it in the Streamlit Cloud settings.")
    st.stop()




import base64

# Function: Text-to-Speech (TTS) with Autoplay
def text_to_speech(text):
    try:
        # Convert text to speech and save to a temporary MP3 file
        tts = gTTS(text)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            temp_file = fp.name  # Save the file path

        # Encode the audio file to Base64
        with open(temp_file, "rb") as audio_file:
            audio_bytes = audio_file.read()
            encoded_audio = base64.b64encode(audio_bytes).decode("utf-8")

        # Create autoplay HTML audio element
        autoplay_audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{encoded_audio}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        """
        # Render the audio in Streamlit
        st.markdown(autoplay_audio_html, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred during text-to-speech conversion: {e}")

    finally:
        # Clean up the temporary file after use
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception as cleanup_error:
                st.warning(f"Temporary file cleanup failed: {cleanup_error}")


st.title("Conversation Tester")
st.markdown("Press the TALK button below and say something.")

# Test speech-to-text functionality
s2t_output = speech_to_text(
    language='en',
    start_prompt="⭕ TALK",
    stop_prompt="🟥 LISTENING...PRESS TO STOP",
    just_once=True,
    use_container_width=True
)

if s2t_output:
    st.write(f"Detected Speech: {s2t_output}")
    #Exit condition
    if "exit" in s2t_output.lower() or "stop" in s2t_output.lower():
        st.write("Ending conversation. Goodbye!")
        #text_to_speech("Ending conversation. Goodbye!")
    else:
        #Query the LLM and get the bot's reply
        response = llm.predict(s2t_output)
        st.write(f"**Assistant says:** {response}")
        text_to_speech(response)
else:
    st.warning("No input detected. Please try again.")

