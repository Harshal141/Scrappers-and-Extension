import os
import pandas as pd
from dotenv import load_dotenv
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.chat_models import init_chat_model
from langchain_core.tools import Tool
from langgraph.prebuilt import create_react_agent

load_dotenv()

# Environment setup
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY_V2")

# LangChain components
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

# Utility functions
def safe_str(val, default=""):
    if pd.isna(val):
        return default
    val = str(val).strip()
    return val if val else default

def build_prompt(name: str, address: str, contact_name: str, contact_email: str) -> str:
    return f"""
You will receive the name of a manufacturing company, along with optional supporting details. Please use your web search capabilities to find the official domain (URL) of that website.

Your task:
- You can only return two things: the official domain of the company or "No official website found".
- Make sure you do not send any other information, just the domain. I am using you in a script that expects only the domain name.
- Do **not** return search results, listings, directories, fan pages, third-party links, or sponsored content.
- The result should be the **official** website of the entity in question.
- If the company has no official website or you have any doubt, return "No official website found"

Here is the information you will use to find the official website:
Name: {name}
Address: {address}
Contacts Name: {contact_name}
Contacts Email: {contact_email}
""".strip()

def run_agent_for_prompt(prompt: str) -> str:
    try:
        events = agent.stream(
            {
                "messages": [("user", prompt)],
            },
            stream_mode="values",
            config={"recursion_limit": 30},
        )
        last_message = None
        for event in events:
            last_message = event["messages"][-1]
        return last_message.content.strip() if last_message else "No official website found"
    
    except Exception as e:
        err_msg = str(e)
        if "recursion limit" in err_msg.lower():
            print("⚠️ Recursion limit exceeded, using fallback.")
        else:
            print(f"❌ Agent error: {err_msg}")
        return "No official website found"


# Main loop
def main(input_csv: str):
    df = pd.read_csv(input_csv)
    df["domain_serper"] = ""

    for idx, row in df.iterrows():
        name = safe_str(row.get("name"), "No name provided")
        address = safe_str(row.get("address"), "No address provided")
        first_name = safe_str(row.get("first_name"), "")
        last_name = safe_str(row.get("last_name"), "")
        contact_name = ", ".join(filter(None, [first_name, last_name])) or "No contact name"
        contact_email = safe_str(row.get("email"), "No contact email")

        print(f"\n🔍 Processing: {name}")
        prompt = build_prompt(name, address, contact_name, contact_email)
        result = run_agent_for_prompt(prompt)
        print(f"✅ {name} → {result}")

        df.at[idx, "domain_serper"] = result

        # Optional: break after one for quick test
        # break

    df.to_csv("serper/agent_serper_result.csv", index=False)
    print("✅ Results saved to serper/agent_serper_result.csv")

if __name__ == "__main__":
    main("serper/organic_data_300.csv")
