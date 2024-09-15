import streamlit as st
import torch
import torchaudio
from transformers import VitsTokenizer, VitsModel, set_seed
import soundfile as sf
from pydub import AudioSegment


tokenizer = VitsTokenizer.from_pretrained("facebook/mms-tts-lao")
model = VitsModel.from_pretrained("facebook/mms-tts-lao")
sampling_rate = model.config.sampling_rate


st.title("Makerbox - Lao TTS Demo")

def text_to_speech(text):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        speech = model(**inputs)
    waveform = speech.waveform[0]

    return waveform


model.speaking_rate = st.slider("Speaking Rate", min_value=0.5, max_value=2.0, value=1.5, step=0.1)
model.noise_scale = st.slider("Noise scale", min_value=0.0, max_value=1.0, value=0.8, step=0.1)
model.vocab_size = st.slider("Vocab Size", min_value=0, max_value=100, value=51, step=1)


text_input = st.text_area("Enter the text you want to convert to speech:")

if st.button("Generate Speech"):
    if text_input:
        speech_waveform = text_to_speech(text_input)
        speech_waveform = speech_waveform.squeeze().numpy()
        st.audio(speech_waveform, format="audio/wav", sample_rate=sampling_rate)
    else:
        st.warning("Please enter some text.")





