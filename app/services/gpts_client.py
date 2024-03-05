# gpts_client.py

import asyncio
import json
import os
import time
from typing import Any, Dict, List, Optional
import openai
from enum import Enum

from pydantic import BaseModel, Field

from app.models.schemas import Assistant, DeletionResponse, FileObject

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_gpts_client():
    return GPTSClient(api_key=OPENAI_API_KEY)

class OpenAIModel(str, Enum):
    GPT_3 = "gpt-3.5-turbo"
    GPT_3_5 = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"

class GPTSClient:
    
    def __init__(self, api_key: str, model: OpenAIModel = OpenAIModel.GPT_3_5, temperature: float = 0.7, max_tokens: int = 250):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        openai.api_key = self.api_key
        
    def create_assistant(self, name: str, model: OpenAIModel = OpenAIModel.GPT_3_5, instructions: str = None, tools: list = None, file_ids: list = None, metadata: dict = None) -> Assistant:
        
        if name is None:
            raise ValueError("Name is required")
        
        new_assistant = openai.beta.assistants.create(
            instructions=instructions,
            name=name,
            tools=tools or [],
            model=model,
            file_ids=file_ids or [],
            metadata=metadata or {}
        )
        
        return GPTSClient.Assistant(**new_assistant)
    
    def get_assistant(self, assistant_id: str) -> Assistant:
        assistant = openai.beta.assistants.retrieve(assistant_id)
        if assistant is None:
            raise ValueError(f"Assistant with id {assistant_id} does not exist")
        return GPTSClient.Assistant(**assistant)
    
    def update_assistant(self,  assistant_id: str, overwrite: bool = False, name: str = None, instructions: str = None, tools: list = None, file_ids: list = None, metadata: dict = None) -> Assistant:
        
        if not overwrite:
            existing_assistant = self.get_assistant(assistant_id)
            
            if existing_assistant is None:
                raise ValueError(f"Assistant with id {assistant_id} does not exist")
            
            tools = list(set(existing_assistant.tools + (tools or [])))
            file_ids = list(set(existing_assistant.file_ids + (file_ids or [])))
            metadata = {**existing_assistant.metadata, **(metadata or {})}
        
        updated_assistant = openai.beta.assistants.update(
            assistant_id,
            instructions=instructions,
            name=name,
            tools=tools,
            file_ids=file_ids,
            metadata=metadata
        )
        
        if updated_assistant is None:
            raise ValueError(f"Assistant with id {assistant_id} does not exist")
        
        return GPTSClient.Assistant(**updated_assistant)
    
    def delete_assistant(self, assistant_id: str) -> DeletionResponse:
        
        deleted_object = openai.beta.assistants.delete(assistant_id)
        
        if deleted_object is None:
            raise ValueError(f"Assistant with id {assistant_id} does not exist")
        
        return GPTSClient.DeletionResponse(**deleted_object)
        
    def list_assistants(self, order: str) -> List[Assistant]:
        
        if order not in ["asc", "desc"]:
            raise ValueError("Order must be 'asc' or 'desc'")
        
        assistants = openai.beta.assistants.list(order=order)
        
        return [GPTSClient.Assistant(**assistant) for assistant in assistants]
    
    def attach_file(self, assistant_id: str, file_id: str) -> FileObject:
        
        assistant = self.get_assistant(assistant_id)
        
        if assistant is None:
            raise ValueError(f"Assistant with id {assistant_id} does not exist")
        
        created_file = openai.beta.assistants.files.create(assistant_id, file_id)
        
        if created_file is None:
            raise ValueError(f"File with id {file_id} does not exist")
        
        return GPTSClient.FileObject(**created_file)
    
    def retrieve_file(self, assistant_id: str, file_id: str) -> FileObject:
        
        assistant = self.get_assistant(assistant_id)
        
        if assistant is None:
            raise ValueError(f"Assistant with id {assistant_id} does not exist")
        
        file = openai.beta.assistants.files.retrieve(assistant_id, file_id)
        
        if file is None:
            raise ValueError(f"File with id {file_id} does not exist")
        
        return GPTSClient.FileObject(**file)
    
    def delete_file(self, assistant_id: str, file_id: str) -> DeletionResponse:
        
        assistant = self.get_assistant(assistant_id)
        
        if assistant is None:
            raise ValueError(f"Assistant with id {assistant_id} does not exist")
        
        deleted_file = openai.beta.assistants.files.delete(assistant_id, file_id)
        
        if deleted_file is None:
            raise ValueError(f"File with id {file_id} does not exist")
        
        return GPTSClient.DeletionResponse(**deleted_file)
    
    async def run_thread(thread_id: str, assistant_id: str, callback: Any) -> str:
        # Create a run with specific instructions
        run = openai.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )

        # Check for run completion and stream responses using a callback
        while run.status != "completed":
            
            time.sleep(0.1)
            run = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            
            if run.status in ["failed", "cancelled", "expired"]:
                raise ValueError("Run failed with status: " + run.status)

            if run.status == "requires_action":
                tool_outputs = []

                for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                    functionName = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    
                    # Dynamically call the function with arguments
                    output = await callback(functionName, args)
                                            
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": output,
                    })

                # Submit tool outputs
                openai.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread_id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
        
                            
        # Assuming `messages` is a response object from the OpenAI API that contains message data in a list
        messages = openai.beta.threads.messages.list(
            thread_id=thread_id
        )

        # Sort messages by their creation time
        sorted_messages = sorted(messages.data, key=lambda x: x.created_at)

        # Iterate through the sorted messages (skipping the first one), 
        # find those of type "text", and join their text values into a final string
        final_message = "\n".join([
            ", ".join(blurb.text.value for blurb in message.content if blurb.type == "text")
            for message in sorted_messages[1:]
        ])

        return final_message

    
    async def single_response(self, assistant_id: str, prompt: str, callback) -> str:
        try:
            # Create a new thread
            thread = openai.beta.threads.create()

            # Post the initial user message to the thread
            initial_message = openai.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=prompt
            )
            
            return await GPTSClient.run_thread(thread.id, assistant_id, callback)

            
        except ValueError as e:
            print(f"Error during streaming: {e}")

        
    async def server_and_user_message_response(self, assistant_id: str, server_prompt: str, user_prompt: str, callback) -> str:
        
        thread = openai.beta.threads.create()
        
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="system",
            content=server_prompt
        )
        
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_prompt
        )
        
        return await GPTSClient.run_thread(thread.id, assistant_id, callback)

        
    async def conversation_response(self, assistant_id: str, messages: list, callback) -> str:
        
        thread = openai.beta.threads.create()
        
        for message in messages:
            openai.beta.threads.messages.create(
                thread_id=thread.id,
                role=message["role"],
                content=message["content"]
            )
        
        return await GPTSClient.run_thread(thread.id, assistant_id, callback)
