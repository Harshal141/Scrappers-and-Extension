import os
import json
import asyncio
from openai import AsyncOpenAI, OpenAIError
from dotenv import load_dotenv
load_dotenv()

client = AsyncOpenAI(api_key=os.getenv('OPENAI_KEY'))
DATA_FILE = "./FnBScanner/DATA_300_pacGlobal_ai.json" # OUTPUT FILE

with open("./FnBScanner/DATA_300_pacGlobal.json", "r", encoding="utf-8") as file:
    jsonData = json.load(file)

def read_data_file():
    try:
        if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        else:
            return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def store_data(new_data):
    try:
        # Read current data from the file
        current_data = read_data_file()

        # Merge new data into current data
        updated_data = current_data + new_data

        # Write updated data back to the file
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(updated_data, file, indent=2)

        print("Data stored successfully.")
    except Exception as err:
        print(f"Failed to store data: {err}")

async def check_food_and_beverage_manufacturing(domain, textual_content):
    prompt = (
        f"I have the textual content of this website {domain}. I want you to tell me "
        "whether this is related to food and beverage manufacturing or not. Just reply with 'true' or 'false' without any extra detail. "
        f"If there are chances that it may be food and beverages related, such as involving packaging, packaging suppliers, "
        f"co-packers, ingredients supplier, food service, supplement manufacturers, or other types of manufacturers, consider it as related. "
        f"Here is the textual content: {textual_content}"
    )
    
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",  # Use the correct GPT-4 model
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        ai_result = response.choices[0].message.content

        if(ai_result == "true"):
            return True
        return False

    except OpenAIError as e:
        print(f"Error: {e}")
        return None




async def main():

    final_data = []

    # counter = 0
    for index, coman in enumerate(jsonData):
        # counter +=1
        # if(counter == 13):
        #     break

        if "error" in coman:
            final_data.append({**coman, "isRelated" : True})
            continue
        if "error" in coman["extractedData"]:
            final_data.append({**coman, "isRelated" : True})
            continue

        domain = coman["url"]
        print("Processing "+ domain )
        textualContent = coman["extractedData"]["textData"]

        isRelated = await check_food_and_beverage_manufacturing(domain, textualContent)

        if isRelated:
            final_data.append({**coman, "isRelated" : True})
        else:
            final_data.append({**coman, "isRelated" : False})
        
        if (index + 1) % 1000 == 0:
            store_data(final_data)
            final_data.clear()

    store_data(final_data)

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
