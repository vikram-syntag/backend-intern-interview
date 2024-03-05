from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import ChatCompletionResponse, ConversationModel, ServerAndUserMessageModel, SingleRequestModel
from services.openai_client import OpenAIClient, get_openai_client

router = APIRouter(prefix="/generate")


########################
# SINGLE REQUEST ROUTE #
########################


@router.post("/single", response_model=ChatCompletionResponse)
async def single_response(
    request: SingleRequestModel, 
    openai_client: OpenAIClient = Depends(get_openai_client)
) -> ChatCompletionResponse:
    try:
        generated_text = openai_client.single_response(prompt=request.prompt)
        return ChatCompletionResponse(response=generated_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#################################
# SERVER AND USER MESSAGE ROUTE #
#################################


@router.post("/server-and-user", response_model=ChatCompletionResponse)
async def server_and_user_message_response(
    request: ServerAndUserMessageModel,
    openai_client: OpenAIClient = Depends(get_openai_client)
) -> ChatCompletionResponse:
    try:
        generated_text = openai_client.server_and_user_message_response(
            server_prompt=request.server_prompt, 
            user_prompt=request.user_prompt
        )
        return ChatCompletionResponse(response=generated_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
######################
# CONVERSATION ROUTE #
######################
    
    
@router.post("/conversation", response_model=ChatCompletionResponse)
async def conversation_response(
    request: ConversationModel,
    openai_client: OpenAIClient = Depends(get_openai_client)
) -> ChatCompletionResponse:
    try:
        generated_text = openai_client.conversation_response(messages=request.messages)
        return ChatCompletionResponse(response=generated_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))