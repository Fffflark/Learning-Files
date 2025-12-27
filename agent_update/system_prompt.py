from typing import TypedDict
from langchain.agents.middleware import dynamic_prompt,ModelRequest
from langchain.messages import SystemMessage

class Context(TypedDict):
    user_role: str



@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> SystemMessage:
    """Generate system prompt based on user role"""
    user_role = request.runtime.context.get("user_role","user")
    content_parts= [
    {
        "type":"text",
        "text":"You are an experienced programmer"
    },
    {
        "type": "text",
        "text": "You are an AI assistant tasked with analyzing codes."
    }]

    
    if user_role == "expert":
        content_parts.append({
            "type": "text", 
            "text": "Provide detailed technical responses with advanced concepts and best practices."
        })
    elif user_role == "beginner":
        content_parts.append({
            "type": "text", 
            "text": "Explain concepts simply and avoid jargon. Use analogies and examples."
        })
    
    return SystemMessage(content=content_parts)
