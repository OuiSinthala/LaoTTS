import streamlit as st
import torch
from transformers import (VitsTokenizer, VitsModel, BatchEncoding, PreTrainedModel, PreTrainedTokenizer)
import string
from modules.preprocessing.lao_number_sounds.lao_number_sounds import preprocess_numbers

class LaoTTS:    
    
    def __init__(
                self, tts_model, 
                tokenizer:PreTrainedTokenizer
    ) -> None:
        self.tts_model = tts_model
        self.tokenizer = tokenizer
        self.device:torch.device = torch.device('cpu')
        self.number_sounds:dict = {
                                '1':'ຫນຶ່ງ','2':"ສອງ", "3":"ສາມ", 
                                "4":"ສີ່", '5':'ຫ້າ','6':"ຫົກ", 
                                '7':"ເຈັດ", '8':'ແປດ', '9':'ເກົ້າ'
                                }
        
        # Use available hardware or specified hardware:
        if torch.cuda.is_available():
            self.device = torch.device('cuda')
        elif torch.backends.mps.is_available():
            self.device = torch.device('mps')
            
    def preprocess_input_text(self, input_text:str) -> str:
        # Remove puntuation:
        # Use string.punctuation.replace(',', '') for leaving only ','
        text:str = input_text.translate(str.maketrans('','', string.punctuation))
        # Convert numbers to correspondin number sounds:
        # Replace Number with Lao number sound
        text:str = preprocess_numbers(text)
        
        return text
            
    def tokenization(self, input_text:str) -> BatchEncoding:
        '''
        Turn normal text into tokens(encoded numbers of the text)
        * BatchEncoding is like encoded version of input text
        * pt means pytorch
        '''
        text = self.preprocess_input_text(input_text)
        print('recieved text:',text)
        text_tokens:BatchEncoding = self.tokenizer(text=text, return_tensors='pt') # return torch tensor
        # Prepare tensors for specific device(CUDA, APPLE GPU, CPU):
        text_tokens.to(self.device)
        return text_tokens
    
    def prepare_model(self) -> None:
        '''
        Prepare model to run on available hardware (GPU, CPU)
        '''
        self.tts_model.eval()
        self.tts_model.to(self.device)
    
    def convert_text_to_speech(self, text_input:str) -> torch.Tensor:        
        # Tokenization:
        text_tokens:BatchEncoding = self.tokenization(text_input)
        
        # Inferring(producing output):
        with torch.no_grad():
            self.prepare_model()
            speech = self.tts_model(text_tokens['input_ids'], text_tokens['attention_mask'])
        
        # Get waveform of the speech:
        waveform = speech.waveform[0]
        
        return waveform


if __name__ == "__main__":
    
    # Speech processors:
    tokenizer:PreTrainedTokenizer= VitsTokenizer.from_pretrained("facebook/mms-tts-lao")
    model:PreTrainedModel = VitsModel.from_pretrained("facebook/mms-tts-lao")
    
    # Model's hyper-parameter:
    model.speaking_rate = torch.tensor(0.86)
    model.noise_scale = torch.tensor(0.5)
    model.noise_scale_duration = torch.tensor(0.2)
    
    
    # Create LaoTTS object
    lao_tts = LaoTTS(tts_model=model, tokenizer=tokenizer)
    print('Using: ',lao_tts.device)
    
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