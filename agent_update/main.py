import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
import tools
import system_prompt
from typing import NoReturn
from langchain.messages import HumanMessage, SystemMessage


load_dotenv()

api_key = os.getenv("SILICONFLOW_API_KEY")



model = ChatOpenAI(
    model = 'Qwen/Qwen3-8B',
    api_key=api_key,
    base_url="https://api.siliconflow.cn/v1"
)

agent = create_agent(
    model,
    tools = [tools.read_file,tools.list_file,tools.rename_file],
    middleware = [system_prompt.user_role_prompt,tools.handle_tool_errors],
    context_schema = system_prompt.Context
)

def main() -> NoReturn:
    history: list[Any] = []
    while True:
        user_input: str = input("Input: (input byebye to kill it)")
        human_msg = HumanMessage(content=user_input)
        if "byebye" in user_input.lower():
            break
        messages:list[Any] = history + [human_msg]
        agent_input = {"messages": messages}
        resp: AgentRunResult[str] = agent.invoke(agent_input,context={"user_role":"expert"})
        history: str = resp.get("messages",[])
        first_sentence: str =history[-1].content
        print(first_sentence)
        
if __name__ == "__main__":
    main()