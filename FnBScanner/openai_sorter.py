import os
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
import subprocess

# Load environment variables
load_dotenv()

# OpenAI Client
client = OpenAI(api_key=os.getenv('OPENAI_KEY'))

# File Paths
INPUT_FILE = "serper/DATA_332/120_/starting_2000_fnb_result.json"  # Input JSON File
DATA_FILE = "serper/DATA_332/120_/starting_2000_fnb_result_ai.json"  # Output JSON File

# Read input JSON data
with open(INPUT_FILE, "r", encoding="utf-8") as file:
    jsonData = json.load(file)

def read_data_file():
    """Reads the output file if it exists; otherwise, returns an empty list."""
    try:
        if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        else:
            return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def store_data(new_data):
    """Stores updated data in the output JSON file."""
    try:
        current_data = read_data_file()
        updated_data = current_data + new_data
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(updated_data, file, indent=2)
        print("Data stored successfully.")
    except Exception as err:
        print(f"Failed to store data: {err}")


def check_food_and_beverage_manufacturing(coman):
    """Checks if a domain is related to food and beverage manufacturing."""
    if "error" in coman or "error" in coman.get("extractedData", {}):
        return {**coman, "isRelated": False} # If there is an error, mark as False

    domain = coman["url"]
    textual_content = coman["extractedData"]["textData"]
    print(f"Processing {domain}")

    prompt = (
        f"I have the textual content of this website {domain}. I want you to tell me "
        "whether this website belongs to or is directly associated with food and beverage manufacturing. "
        "Only reply with 'true' or 'false' without any extra detail. "
        "If the website is a manufacturer, co-packer, packaging supplier, ingredient supplier, food service provider, or supplement manufacturer, "
        "consider it as related and return 'true'. "
        "However, if the website only lists manufacturers without itself being a manufacturer or supplier, return 'false'. "
        f"Here is the textual content: {textual_content}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        ai_result = response.choices[0].message.content.lower()
        return {**coman, "isRelated": ai_result == "true"}

    except OpenAIError as e:
        print(f"Error processing {domain}: {e}")
        return {**coman, "isRelated": None}  # Mark as None if error occurs


def main():
    """Main function to process all items in parallel using ThreadPoolExecutor."""
    final_data = []
    batch_size = 1000  # Store data in batches
    max_workers = 20  # Number of parallel threads

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_data = {executor.submit(check_food_and_beverage_manufacturing, coman): coman for coman in jsonData}

        for index, future in enumerate(as_completed(future_to_data)):
            result = future.result()
            final_data.append(result)

            # Store data every batch_size records
            if (index + 1) % batch_size == 0:
                store_data(final_data)
                final_data.clear()

    # Store any remaining data
    if final_data:
        store_data(final_data)

    print("All tasks completed.")


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"Execution completed in {time.time() - start_time:.2f} seconds")
