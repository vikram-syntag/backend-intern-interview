# utils.py

########################
# GENERATION HELPER FN #
########################

import asyncio
import uuid


def callback_helper(websocket):
    request_id_to_future = {}  # Maps request IDs to asyncio Future objects

    async def listen_for_responses():
        while True:
            response = await websocket.receive_json()
            request_id = response.get("requestId")
            future = request_id_to_future.get(request_id)
            if future and not future.done():
                future.set_result(response)

    asyncio.create_task(listen_for_responses())  # Start listening for responses in a separate task

    async def callback(functionName, functionArgs):
        request_id = str(uuid.uuid4())  # Generate a unique request ID
        future = asyncio.Future()
        request_id_to_future[request_id] = future  # Store the future with the request ID

        await websocket.send_json({
            "type": "callback",
            "functionName": functionName,
            "functionArgs": functionArgs,
            "requestId": request_id,
        })

        response = await future  # Wait for the future to have a result set by listen_for_responses
        return response.get("result")
            
    return callback