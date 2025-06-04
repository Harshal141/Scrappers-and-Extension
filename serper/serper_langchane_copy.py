from langchain.chat_models import init_chat_model
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import Tool
from langgraph.prebuilt import create_react_agent
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY_V2")

llm = init_chat_model("gpt-4o-mini", model_provider="openai", temperature=0)
search = GoogleSerperAPIWrapper()
tools = [
    Tool(
        name="Intermediate_Answer",
        func=search.run,
        description="useful for when you need to ask with search",
    )
]
agent = create_react_agent(llm, tools)

events = agent.stream(
    {
        "messages": [
            ("user", "Official website of 1 DSD LLC"),
        ]
    },
    stream_mode="values",
)

for event in events:
    event["messages"][-1].pretty_print()