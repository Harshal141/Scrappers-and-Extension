from openai import OpenAI
import os
from dotenv import load_dotenv
import pandas as pd
import time
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

def build_search_query(name: str, address: str) -> str:
    return f"""
    You will receive the name of a manufacturing company, along with optional supporting details. Please use your web search capabilities to find the official domain (URL) of that website.

    Your task:
    - Return **only** the **main domain name**, such as `example.com`.
    - Do **not** return search results, listings, directories, fan pages, third-party links, or sponsored content.
    - The result should be the **official** website of the entity in question.
    - Only return the domain. No description or commentary.

    Name: {name}
    Address: {address}
    If the company has multiple domains, return the most relevant one.
    If the company has no official website, return "No official website found".
    """

def find_company_domain(name: str, address: str) -> str:
    response = client.responses.create(
        model="gpt-4.1",
        tools=[{
            "type": "web_search_preview",
            "user_location": {
                "type": "approximate",
                "country": "US",
            }
        }],
    
        input=build_search_query(name, address),
    )
    for item in response.output:
        if getattr(item, "type", None) == "message":
            for part in item.content:
                if hasattr(part, "text"):
                    return part.text.strip()

    return "No response found"

def runner():
    df = pd.read_csv("serper/organic_data_300.csv")
    df = df[df["name"].notna()]
    df["domain"] = ""

    seen = set()

    for idx, row in df.iterrows():
        name = row["name"]
        address = row["address"] if "address" in row else ""
        if name in seen:
            continue
        seen.add(name)

        try:
            domain = find_company_domain(name, address)
            print(f"{name} → {domain}")
            df.at[idx, "domain"] = domain
            time.sleep(0.2)
        except Exception as e:
            print(f"❌ Failed for {name}: {e}")
            df.at[idx, "domain"] = "ERROR"

    df.to_csv("serper/agent_gpt_result.csv", index=False)
    print("✅ Saved to serper/domains_output.csv")


if __name__ == "__main__":
    runner()