import streamlit as st
import torch
from transformers import (VitsTokenizer, VitsModel, BatchEncoding, PreTrainedModel)



class LaoTTS:    
    
    def __init__(
                self, tts_model:PreTrainedModel, 
                tokenizer:PreTrainedModel,
                device:torch.device = torch.device('cpu'),
    ) -> None:
        self.tts_model:PreTrainedModel = tts_model
        self.tokenizer:PreTrainedModel = tokenizer
        self.device:torch.device = device
        
        # Use available hardware or specified hardware:
        if torch.cuda.is_available():
            self.device = torch.device('cuda')
        elif torch.backends.mps.is_available():
            self.device = torch.device('mps')
        elif device == torch.device('cpu'):
            self.device = torch.device('cpu')
            
    def tokenization(self, input_text:str) -> BatchEncoding:
        '''
        Turn normal text into tokens(encoded numbers of the text)
        * BatchEncoding is like encoded version of input text
        * pt means pytorch
        '''
        text_tokens:BatchEncoding = self.tokenizer(text=input_text, return_tensors='pt') 
        # Prepare tensors for specific device(CUDA, APPLE GPU, CPU):
        text_tokens.to(self.device)
        return text_tokens
    
    def prepare_model(self) -> None:
        '''
        Prepare model to run on available hardware (GPU, CPU)
        '''
        self.tts_model.to(self.device) # type: ignore
    
    def convert_text_to_speech(self, text_input:str) -> torch.Tensor:        
        # Tokenization:
        text_tokens:BatchEncoding = self.tokenization(text_input)
        
        # Inferring(producing output):
        with torch.no_grad():
            self.prepare_model()
            speech = self.tts_model(text_tokens['input_ids'])
        
        # Get waveform of the speech:
        waveform = speech.waveform[0]
        
        return waveform

if __name__ == "__main__":
    
    # Speech processors:
    tokenizer = VitsTokenizer.from_pretrained("facebook/mms-tts-lao")
    model = VitsModel.from_pretrained("facebook/mms-tts-lao")
    
    # Model's hyper-parameter:
    model.vocab_size = torch.tensor(20,dtype=torch.float16)
    model.speaking_rate = torch.tensor(0.9)
    model.noise_scale = torch.tensor(0.8)
    model.noise_scale_duration = torch.tensor(0.7, dtype=torch.float16)
    
    
    # Create LaoTTS object
    lao_tts = LaoTTS(tts_model=model, tokenizer=tokenizer)
    print(lao_tts.device)
    
    # App info
    st.title("Makerbox - Lao TTS Demo")
    
    # Core process:
    text_input = st.text_area("Enter the text you want to convert to speech:")
    if st.button("Generate Speech"):
        if text_input:
            speech_waveform_tensor = lao_tts.convert_text_to_speech(text_input)
            speech_waveform = speech_waveform_tensor.cpu().squeeze().numpy()
            st.audio(speech_waveform, format="audio/wav", sample_rate=model.config.sampling_rate)
        else:
            st.warning("Please enter some text.")