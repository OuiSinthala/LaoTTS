import streamlit as st
from tts_engine import LaoTTS

if __name__ == "__main__":    
    lao_tts_engine = LaoTTS()
    
    # App info
    st.title("Makerbox - Lao TTS Demo")
    
    # Core process:
    text_input = st.text_area("Enter the text you want to convert to speech:")
    if st.button("Generate Speech"):
        if text_input:
            speech_waveform_tensor = lao_tts_engine.convert_text_to_speech(text_input)
            speech_waveform = speech_waveform_tensor.cpu().squeeze().numpy()
            st.audio(
                    speech_waveform, 
                    format="audio/wav",
                    sample_rate=lao_tts_engine.tts_model.config.sampling_rate
            )
        else:
            st.warning("Please enter some text.")