# tool function
import os
from pathlib import Path
from langchain.tools import tool

base_dir = Path("./agent")

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
    print("list file")
    file_list: list[Any] = []
    for item in base_dir.rglob("*"):
        if item.is_file():
            file_list.append(str(item.relative_to(base_dir)))
    return file_list

@tool
def rename_file(name:str,new_name:str) -> str:
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
        