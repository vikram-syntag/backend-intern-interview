# Load .env file if it exists in development
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from routes.generate import router as text_generation_router
from routes.ws.generate import router as text_generation_ws_router
from routes.ws.gpts import router as gpts_ws_router
from routes.chat import router as chat_router

app = FastAPI()

# Include the routes from the routes directory
app.include_router(text_generation_router, tags=["Text Generation"])
app.include_router(text_generation_ws_router, tags=["Text Generation (WebSockets)"])
app.include_router(gpts_ws_router, tags=["GPT Assistants (WebSockets)"])
app.include_router(chat_router, tags=["Chat"])
