import requests
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

PPLX_KEY = os.getenv("PPLX_KEY")

def safe_str(val, default=""):
    """Safely convert any value to a clean string or fallback."""
    if pd.isna(val):
        return default
    val = str(val).strip()
    return val if val else default

def build_prompt(name: str, address: str, contact_name: str, contact_email: str) -> str:
    return f"""
You will be provided with the name of a manufacturing company, along with optional supporting details. Your task is to use web search to identify what appears to be the company's **official website domain**.

Instructions:
- Return your response in the following JSON format:
  {{
    "domain": "<the official domain or 'No official website found'>",
    "confidence": "<high | medium | low>"
  }}

- The "domain" should be the official website of the company, such as `example.com`.
- Avoid returning third-party listings, directories, social media profiles, sponsored content, or reseller pages.
- If you are unsure but still believe a site may be official, provide the domain with a **medium or low confidence** rating.
- If you cannot find any official site, or are highly uncertain, use:
  {{
    "domain": "No official website found",
    "confidence": "low"
  }}

Here are the company details to assist your search:
- Company Name: {name}
- Address: {address}
- Contact Person: {contact_name}
- Contact Email: {contact_email}
""".strip()


def ask_perplexity(prompt: str) -> str:
    url = "https://api.perplexity.ai/chat/completions"

    payload = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": prompt}
        ]
    }

    headers = {
        "Authorization": f"Bearer {PPLX_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()["choices"][0]["message"]["content"].strip()

def main(input_csv: str, output_csv: str = "serper/agent_perplex_result_1000.csv"):
    df = pd.read_csv(input_csv)
    df["domain_perp"] = ""

    seen = set()

    for idx, row in df.iterrows():
        name = safe_str(row.get("name"), "No name provided")
        address = safe_str(row.get("address"), "No address provided")
        first_name = safe_str(row.get("first_name"), "")
        last_name = safe_str(row.get("last_name"), "")
        contact_name = ", ".join(filter(None, [first_name, last_name])) or "No contact name"
        contact_email = safe_str(row.get("email"), "No contact email")

        print(f"Processing: {name} | {address} | {contact_name} | {contact_email}")

        if not name or name.lower() in seen:
            continue

        key = (name.lower(), address.lower())
        if key in seen:
            continue
        seen.add(key)

        prompt = build_prompt(name, address, contact_name, contact_email)

        try:
            domain = ask_perplexity(prompt)
        except Exception as e:
            print(f"❌ Error fetching domain for {name}: {e}")
            domain = "Error fetching domain"

        df.at[idx, "domain_perp"] = domain
        print(f"{name} → {domain}")

    df.to_csv(output_csv, index=False)
    print(f"✅ Saved to {output_csv}")

if __name__ == "__main__":
    main("serper/sampled_1000_rows_organic.csv")

#TODO: schema define and pydatic