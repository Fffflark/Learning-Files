import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
import tools
from typing import NoReturn
from openai import AsyncOpenAI


load_dotenv()

api_key = os.getenv("SILICONFLOW_API_KEY")

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://api.siliconflow.cn/v1"
)

provider = OpenAIProvider(openai_client=client)

model = OpenAIModel(
    'Qwen/Qwen3-8B',
    provider=provider
)

system_prompt = "You are an experienced programmer"

agent = Agent(
    model,
    system_prompt = system_prompt,
    tools = [tools.read_file,tools.list_file,tools.rename_file]
)

def main() -> NoReturn:
    history: list[Any] = []
    while True:
        user_input: str = input("Input: (input byebye to kill it)")
        if user_input == "byebye":
            break
        resp: AgentRunResult[str] = agent.run_sync(user_input,message_history=history)
        history = list(resp.all_messages())
        print(resp.output)
        
if __name__ == "__main__":
    main()