from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"

class Message(BaseModel):
    role: Role
    content: str
class Issue(BaseModel):
    issue_id: str
    issue_name: str
    issue_description: str
    
class ConversationModel(BaseModel):
    messages: List[Message]

    
class FindIssueRequest(BaseModel):
    conversation: ConversationModel
    issues: List[Issue]
    
class FindIssueResponse(BaseModel):
    found_issue: bool
    issue_id: str = None
    
class SingleRequestModel(BaseModel):
    prompt: str
    
class ChatCompletionResponse(BaseModel):
    response: str
    
class ServerAndUserMessageModel(BaseModel):
    server_prompt: str
    user_prompt: str
    

class Assistant(BaseModel):
    id: str = Field(..., alias='id')
    object: str
    created_at: int
    name: str
    description: Optional[str] = None
    model: str
    instructions: str
    tools: List[Any]
    file_ids: List[str]
    metadata: Dict[str, Any]
    
class DeletionResponse(BaseModel):
    id: str = Field(..., alias='id')
    object: str
    deleted: bool
    
class FileObject(BaseModel):
    id: str = Field(..., alias='id')
    object: str
    created_at: int
    assistant_id: str
    
