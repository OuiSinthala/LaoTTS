import torch
from transformers import (VitsTokenizer, VitsModel, BatchEncoding, PreTrainedModel, PreTrainedTokenizer)
import string
from modules.preprocessing.lao_number_sounds.lao_number_sounds import preprocess_numbers

class LaoTTS:    
    
    def __init__(
                self, 
    ) -> None:
        # Processing device: 
        self.device:torch.device = torch.device('cpu')
        # Use available hardware or specified hardware:
        if torch.cuda.is_available():
            self.device = torch.device('cuda')
        # Load a model and a tokenizer:
        self.tts_model:PreTrainedModel = VitsModel.from_pretrained("facebook/mms-tts-lao")
        self.tokenizer:PreTrainedTokenizer = VitsTokenizer.from_pretrained("facebook/mms-tts-lao")
        # Model's hyper-parameter:
        self.tts_model.speaking_rate = torch.tensor(0.86)
        self.tts_model.noise_scale = torch.tensor(0.5)
        self.tts_model.noise_scale_duration = torch.tensor(0.2)

            
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
    
    def convert_text_to_speech(self, text_input:str) -> torch.Tensor:        
        # Tokenization:
        text_tokens:BatchEncoding = self.tokenization(text_input)
        
        # Inferring(producing output):
        with torch.no_grad():
            speech = self.tts_model(text_tokens['input_ids'], text_tokens['attention_mask'])
        
        # Get waveform of the speech:
        waveform = speech.waveform[0]
        
        return waveform

