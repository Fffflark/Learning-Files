import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_openai import ChatOpenAI
from typing import NoReturn, Any
from langchain.messages import HumanMessage
import datetime
import tools
import system_prompt
import memory
import retrieval
import structured_output
import constant

load_dotenv()

api_key = os.getenv("SILICONFLOW_API_KEY")

DEFAULT_LOG_FILE = f"{constant.agent_name}_log.txt"
memory.create_txt_file(DEFAULT_LOG_FILE, "Agent运行日志\n==============\n创建时间: " + 
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")

memory.init_memory_system()
retrieval.init_retrieval()

model = ChatOpenAI(
    model = constant.model_name,
    api_key=api_key,
    base_url="https://api.siliconflow.cn/v1"
)

agent = create_agent(
    model,
    tools = [],
    middleware = [system_prompt.user_role_prompt,tools.handle_tool_errors],
    context_schema = system_prompt.Context,
    #response_format=ToolStrategy(structured_output.FileInfo)
)


def main() -> NoReturn:
    history: list[Any] = []
    i: int = 0
    while True:
        user_input: str = input("Input: (input byebye to kill it)")
        retriever_msg = retrieval.similarity_search_with_reranking(query=user_input, k=constant.similarity)
        human_msg = HumanMessage(content=user_input)
        
        if "byebye" in user_input.lower():
            break
        messages:list[Any] = history+ retriever_msg+ [human_msg]
        agent_input = {"messages": messages}
        resp: AgentRunResult[str] = agent.invoke(
            agent_input,
            context={"user_role":constant.user_role}
            )
        i += 1
        history = resp.get("messages",[])
        memory.append_to_file(DEFAULT_LOG_FILE, history)
        memory.update_db(history, i)
        first_sentence: str =history[-1].content
        print(first_sentence)
        
if __name__ == "__main__":
    main()