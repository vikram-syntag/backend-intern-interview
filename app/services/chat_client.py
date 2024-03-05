# chat_client.py

from enum import Enum
import os
from typing import List, Optional, Tuple
from app.models.schemas import ConversationModel, Issue, Role

from app.services.openai_client import get_openai_client

def get_chat_client():
    return ChatClient()

class OpenAIModel(str, Enum):
    GPT_3 = "gpt-3.5-turbo"
    GPT_3_5 = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"
    
FIND_ISSUE_PROMPT = """
NO MATTER WHAT, YOUR ONLY JOB IS TO OUTPUT THE ISSUE ID OF THE ISSUE THAT MOST CLOSELY MATCHES THE CONVERSATION. \
IF NO ISSUE MATCHES, THEN YOU SHOULD OUTPUT "NONE". DO NOT OUTPUT ANY OTHER INFORMATION. JUST A SINGLE STRING. \
You are in the middle of a multiple choice test. You are presented with the following question: \
Which issue most closely matches the following conversation? \
{conversation}

Here are your options. Remember to pick the one that most closely matches the conversation. If none match, then output "NONE". \
{issues}

Which issueID will you pick? Remember, NONE is an option as well. 
"""

DEFAULT_ISSUES = [
    Issue(
        issue_id="1",
        issue_name="Delayed Order Pick-ups",
        issue_description="Customers are complaining that their orders are not being picked up on time."
    ),
    Issue(
        issue_id="2",
        issue_name="Kit Processing",
        issue_description="Customers are complaining that their kits are not being processed correctly."
    ),
    Issue(
        issue_id="3",
        issue_name="Account Balance problems",
        issue_description="Customers want to know about their account balance, or it's not showing up correctly or being updated correctly."
    ),
    Issue(
        issue_id="4",
        issue_name="Order Status",
        issue_description="Customers want to know the status of their orders."
    ),
]

class ChatClient:
    
    def __init__(self, issues: List[Issue] = None, conversation: ConversationModel = None, model: OpenAIModel = OpenAIModel.GPT_3_5):
    
        self.issues = issues or DEFAULT_ISSUES
        self.conversation = conversation or ConversationModel(messages=[])
        self.model = model
        self.openai_client = get_openai_client(model=self.model)
        
    def find_issue(self, issues: List[Issue] = None, conversation: ConversationModel = None) -> Tuple[bool, Optional[str]]:
        """
        This function aims to identify if a user's reported issue matches any known issues from a predefined list. 
        It takes two arguments:
        - issues: a list of Issue objects. Each Issue object contains an 'issue_id', 'issue_name', and 'issue_description'.
        - conversation: a ConversationModel object representing the conversation history with the user. 
                        The ConversationModel includes a list of messages, where each message has a 'role' 
                        (either SYSTEM or user) and 'content'.

        The function should perform the following steps:
        1. Format the conversation into a string, where system messages are prefixed with 'ASSISTANT:' 
           and converted to uppercase, and user messages are prefixed with 'user:' and converted to lowercase.
        2. Format the list of issues into a string, where each issue is represented by its 'issue_id', 'issue_name', 
           and 'issue_description' in a specific format.
        3. Use the formatted conversation and issues to generate a prompt for the OpenAI client to determine if the 
           user's issue matches any known issues.
        4. Analyze the OpenAI client's response to identify if any 'issue_id' from the known issues is mentioned. 
           If so, that issue is considered found.
        5. Return a tuple containing a boolean indicating whether the issue was found, and the 'issue_id' of the 
           found issue (if any). If no issue is found, the 'issue_id' should be None.

        Returns:
        - A tuple (bool, Optional[str]) where the boolean indicates if a matching issue was found, 
          and the Optional[str] is the 'issue_id' of the found issue or None if no match was found.
        """
        pass # Replace this pass statement with your implementation.

    
    def conversation_response(self, conversation: ConversationModel = None) -> str:
        """
        This function processes a conversation with a user, identifies if the user's issue matches any known issues, 
        and generates an appropriate response based on the conversation context.

        Parameters:
        - conversation: a ConversationModel object representing the current conversation history with the user. 
                        The ConversationModel includes a list of messages, where each message has a 'role' (either 
                        SYSTEM or USER) and 'content'. This parameter is optional; if not provided, the function 
                        should use the default conversation (self.conversation).

        Steps:
        1. If a 'conversation' argument is provided, update the instance's conversation to the new conversation.
        2. Use the 'find_issue' method to determine if the user's reported issue matches any from a predefined 
           list of known issues. This method should return a tuple indicating whether a matching issue was found and 
           the ID of the found issue (if any).
        3. If no matching issue is found, use the 'openai_client.conversation_response' method
           to generate a response based on the conversation's messages.
        4. If a matching issue is found, append a system-generated message to the conversation indicating that 
           the issue has been identified, using the issue's name. Then, generate a response using the 
           'openai_client.conversation_response' method, incorporating this additional context.
        5. Append the generated response as a new system message to the conversation.
        6. Return the generated response.

        The goal is to dynamically respond to the user by either addressing their specific issue directly, if recognized,
        or by generating a conversational response that fits the flow of the conversation if the issue is not identified.

        Returns:
        - A string containing the generated response to the user's messages, incorporating recognition of the user's issue if applicable.
        """
        pass # Replace this pass statement with your implementation.

    