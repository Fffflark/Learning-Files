# tool function
import os
from pathlib import Path
from langchain.tools import tool
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage


base_dir = Path("./test")

@wrap_tool_call
def handle_tool_errors(request,handler)-> ToolMessage:
    # request: ToolCallRequest,handler: Callable[[ToolCallRequest], ToolMessage]
    """Handle tool execution errors with custom message"""
    try: return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({str(e)})",
            tool_call_id = request.tool_call["id"]
        )
    

@tool
def read_file(name:str) -> str:
    """Return file content. If not exist, return error message."""
    print(f"read file {name}")
    try:
        with open(base_dir/name,"r") as f:
            content: str = f.read()
        return content
    except Exception as e:
        return f"An error occurred: {e}"

@tool
def list_file() -> list[str]:
    """List the relative dirs for all the file"""
    print("list file")
    file_list: list[Any] = []
    for item in base_dir.rglob("*"):
        if item.is_file():
            file_list.append(str(item.relative_to(base_dir)))
    return file_list

@tool
def rename_file(name:str,new_name:str) -> str:
    """Rename original file with new name"""
    print(f"rename {name} to {new_name}")
    try:
        new_path: Path = base_dir/new_name
        if not str(new_path).startswith(str(base_dir)):
            return "Error: new_name is outside the base_dir"
        
        os.makedirs(new_path.parent, exist_ok = True)
        os.rename(base_dir/name,new_path)
        return f"Successful rename {name} to {new_name}"
    except Exception as e:
        return f"An error occurred: {e}"
        