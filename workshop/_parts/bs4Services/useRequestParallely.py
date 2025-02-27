import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Thread lock for safe file access
lock = threading.Lock()
data = []
batch_size = 5  # Number of URLs processed before writing to file

urls = [
    "https://www.example.com/page1",
    "https://www.example.com/page2",]

OUTPUT_JSON = 'workshop/buyersguide/company_data.json'

# Function to append data to JSON file in a thread-safe manner
def appendJsonDataToFile(new_data, OUTPUT_JSON):
    with lock:
        try:
            with open(OUTPUT_JSON, 'r') as f:
                existing = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing = []

        existing.extend(new_data)

        with open(OUTPUT_JSON, 'w') as f:
            json.dump(existing, f, indent=4)

# Function to process a single URL
def process_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        #  Add code to extract data from the page

    except requests.RequestException as e:
        print(f"[❌] Request failed for URL {url}: {e}")
        return None

def main(urls):
    global data
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(process_url, url): url for url in urls}
        
        for count, future in enumerate(as_completed(futures), 1):
            result = future.result()
            if result:
                data.append(result)

            # Write data in batches
            if count % batch_size == 0 and data:
                print("[💾] Appending batch to JSON.")
                appendJsonDataToFile(data, OUTPUT_JSON)
                data = []

    # Append remaining data
    if data:
        print("[💾] Appending final batch to JSON.")
        appendJsonDataToFile(data)

if __name__ == "__main__":
    main(urls)
