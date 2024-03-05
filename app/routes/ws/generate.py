import asyncio
from enum import Enum
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, ValidationError
from app.models.schemas import ConversationModel, ServerAndUserMessageModel, SingleRequestModel
from services.openai_client import get_openai_client

router = APIRouter(prefix="/ws/generate")

########################
# SINGLE REQUEST ROUTE #
########################

@router.websocket("/single")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        
        try:
            request_model = SingleRequestModel.model_validate(data)
        except ValidationError as e:

            await websocket.send_text(f"Error: Invalid data format. {e.json()}")
            await websocket.close(code=1002)  # 1002 indicates a protocol error
            return

        prompt = request_model.prompt

        openai_client = get_openai_client() 

        for chunk in openai_client.single_response_stream(prompt):
            await websocket.send_text(chunk)
            await asyncio.sleep(0.01)
            
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close(code=1000)  # Normal closure


#################################
# SERVER AND USER MESSAGE ROUTE #
#################################


@router.websocket("/server-and-user")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        data = await websocket.receive_json()
        
        try:
            request_model = ServerAndUserMessageModel.model_validate(data)
        except ValidationError as e:
            await websocket.send_text(f"Error: Invalid data format. {e.json()}")
            await websocket.close(code=1002)  # 1002 indicates a protocol error
            return

        server_prompt = request_model.server_prompt
        user_prompt = request_model.user_prompt

        openai_client = get_openai_client() 

        for chunk in openai_client.server_and_user_message_response_stream(
            server_prompt, user_prompt
        ): 
            await websocket.send_text(chunk)

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close(code=1000)
        
        
######################
# CONVERSATION ROUTE #
######################


    
@router.websocket("/conversation")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        
        try:
            request_model = ConversationModel.model_validate(data)
        except ValidationError as e:
            await websocket.send_text(f"Error: Invalid data format. {e.json()}")
            await websocket.close(code=1002)  # 1002 indicates a protocol error
            return

        messages = request_model.messages

        openai_client = get_openai_client() 

        for chunk in openai_client.conversation_response_stream(messages):
            await websocket.send_text(chunk)

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close(code=1000)
        