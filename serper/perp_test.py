import requests
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

PPLX_KEY = os.getenv("PPLX_KEY")

url = "https://api.perplexity.ai/chat/completions"

payload = {
    "model": "sonar",
    "messages": [
        {
            "role": "system",
            "content": "Be precise and concise."
        },
        {
            "role": "user",
            "content": "How many stars are there in our galaxy?"
        }
    ]
}
headers = {
    "Authorization": f"Bearer {PPLX_KEY}",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)