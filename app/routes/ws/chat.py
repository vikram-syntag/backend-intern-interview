from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, ValidationError
from app.models.schemas import ConversationModel, ServerAndUserMessageModel, SingleRequestModel
from app.services.chat_client import get_chat_client
from app.utils import callback_helper

router = APIRouter(prefix="/ws/chat")

########################
# SINGLE REQUEST ROUTE #
########################

from fastapi import WebSocket, WebSocketDisconnect
from pydantic import ValidationError

@router.websocket("/")
async def chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:  # Start the loop immediately after accepting the connection
            try:
                # Move the data receiving part inside the while loop
                data = await websocket.receive_json()

                # Check if the message type is 'close'
                if data.get('type') == 'close':
                    print("Received close command")
                    break  # Exit the loop to close the websocket

                try:
                    request_model = ConversationModel.model_validate(data)
                except ValidationError as e:
                    await websocket.send_text(f"Error: Invalid data format. {e.json()}")
                    break  # Optionally break or continue based on your preference

                handler = callback_helper(websocket)
                chat_client = get_chat_client()
                messages = request_model.messages

                # Process the chat client's conversation as before
                result = chat_client.conversation(messages, handler)
                await websocket.send_json(
                    {
                        "type": "result",
                        "result": result
                    }
                )

            except WebSocketDisconnect:
                print("Client disconnected")
                break  # Exit the loop if the client disconnects
            except Exception as e:
                await websocket.send_text(f"Error: {str(e)}")
                break  # Optionally break or continue based on your preference

    finally:
        await websocket.close(code=1000)  # Close the websocket connection with a normal closure code
