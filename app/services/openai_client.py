# openai_client.py

import os
import openai
from enum import Enum

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class OpenAIModel(str, Enum):
    GPT_3 = "gpt-3.5-turbo"
    GPT_3_5 = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"

def get_openai_client(model: OpenAIModel = OpenAIModel.GPT_3_5, temperature: float = 0.7, max_tokens: int = 250):
    return OpenAIClient(api_key=OPENAI_API_KEY, model=model, temperature=temperature, max_tokens=max_tokens)


class OpenAIClient:
    
    def __init__(self, api_key: str, model: OpenAIModel = OpenAIModel.GPT_3_5, temperature: float = 0.7, max_tokens: int = 250):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        openai.api_key = self.api_key
    
    def single_response(self, prompt: str):
        messages = [{"role": "user", "content": prompt}]
        
        response = openai.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        return response.choices[0].message["content"]
    
    def server_and_user_message_response(self, server_prompt: str, user_prompt: str):
        messages = [{"role": "system", "content": server_prompt}, {"role": "user", "content": user_prompt}]
        
        response = openai.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        return response.choices[0].message["content"]
    
    def conversation_response(self, messages: list):
                
        response = openai.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        return response.choices[0].message["content"]

    def single_response_stream(self, prompt: str):
        messages = [{"role": "user", "content": prompt}]
        
        # Initiates the stream and specifies a callback function to handle the stream's output
        stream = openai.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream=True
        )
        
        for response in stream:
            message_content = response.choices[0].delta.content
            if message_content:
                yield message_content
                
    async def server_and_user_message_response_stream(self, server_prompt: str, user_prompt: str):
        messages = [{"role": "system", "content": server_prompt}, {"role": "user", "content": user_prompt}]
        
        # Initiates the stream and specifies a callback function to handle the stream's output
        stream = openai.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream=True
        )
        
        for response in stream:
            message_content = response.choices[0].delta.content
            if message_content:
                yield message_content
                
    async def conversation_response_stream(self, messages: list):
                    
        # Initiates the stream and specifies a callback function to handle the stream's output
        stream = openai.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream=True
        )
        
        for response in stream:
            message_content = response.choices[0].delta.content
            if message_content:
                yield message_content
