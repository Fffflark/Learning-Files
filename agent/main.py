import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
import tools
from typing import NoReturn


load_dotenv()

api_key = os.getenv("SILICONFLOW_API_KEY")



model = ChatOpenAI(
    model = 'Qwen/Qwen3-8B',
    api_key=api_key,
    base_url="https://api.siliconflow.cn/v1"
)

system_prompt = "You are an experienced programmer"

agent = create_agent(
    model,
    system_prompt = system_prompt,
    tools = [tools.read_file,tools.list_file,tools.rename_file]
)

def main() -> NoReturn:
    history: list[Any] = []
    while True:
        user_input: str = input("Input: (input byebye to kill it)")
        if "byebye" in user_input.lower():
            break
        messages:list[Any] = history + [{"role": "user", "content": user_input}]
        agent_input = {"messages": messages}
        resp: AgentRunResult[str] = agent.invoke(agent_input)
        history: str = resp.get("messages",[])
        first_sentence: str =history[-1].content
        print(first_sentence)
        
if __name__ == "__main__":
    main()