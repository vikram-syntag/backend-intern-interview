from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, ValidationError
from app.models.schemas import ConversationModel, ServerAndUserMessageModel, SingleRequestModel
from app.utils import callback_helper
from services.gpts_client import get_gpts_client

router = APIRouter(prefix="/ws/gpts")

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
        
        handler = callback_helper(websocket)
                
        gpts_client = get_gpts_client()
        assistant_id = request_model.assistant_id  
        prompt = request_model.prompt
        
        result = await gpts_client.single_response(assistant_id, prompt, handler)

        await websocket.send_json(
            {
                "type": "result",
                "result": result
            }
        )

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close(code=1000)  # Normal closure


#################################
# SERVER AND USER MESSAGE ROUTE #
#################################
    
@router.post("/server-and-user")
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
        
        handler = callback_helper(websocket)

        server_prompt = request_model.server_prompt
        user_prompt = request_model.user_prompt

        gpts_client = get_gpts_client() 

        await gpts_client.server_and_user_message_response(
            server_prompt, user_prompt, handler
        )

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close(code=1000)
        
        
######################
# CONVERSATION ROUTE #
######################
    
@router.psot("/conversation")
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

        handler = callback_helper(websocket)

        messages = request_model.messages

        gpts_client = get_gpts_client() 

        await gpts_client.conversation_response(messages, handler)

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close(code=1000)
        