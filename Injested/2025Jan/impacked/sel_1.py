import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

urls = [
  "https://www.impackedpackaging.com/suppliers/products/bottle",
  "https://www.impackedpackaging.com/suppliers/products/jar",
  "https://www.impackedpackaging.com/suppliers/products/tube",
  "https://www.impackedpackaging.com/suppliers/products/sachet",
  "https://www.impackedpackaging.com/suppliers/products/pouch",
  "https://www.impackedpackaging.com/suppliers/products/stick",
  "https://www.impackedpackaging.com/suppliers/products/airless_bottle",
  "https://www.impackedpackaging.com/suppliers/products/airless_jar",
  "https://www.impackedpackaging.com/suppliers/products/tottle",
  "https://www.impackedpackaging.com/suppliers/products/compact",
  "https://www.impackedpackaging.com/suppliers/products/lip_gloss_tube",
  "https://www.impackedpackaging.com/suppliers/products/lip_stick",
  "https://www.impackedpackaging.com/suppliers/products/mascara",
  "https://www.impackedpackaging.com/suppliers/products/sprayer",
  "https://www.impackedpackaging.com/suppliers/products/dropper",
  "https://www.impackedpackaging.com/suppliers/products/flip_top_cap",
  "https://www.impackedpackaging.com/suppliers/products/push_pull_cap",
  "https://www.impackedpackaging.com/suppliers/products/pump",
  "https://www.impackedpackaging.com/suppliers/products/disc_top_cap",
  "https://www.impackedpackaging.com/suppliers/products/nail_polish_cap",
  "https://www.impackedpackaging.com/suppliers/products/threaded_closure",
  "https://www.impackedpackaging.com/suppliers/products/plug",
  "https://www.impackedpackaging.com/suppliers/products/twist_open_cap",
  "https://www.impackedpackaging.com/suppliers/products/tube_cap",
  "https://www.impackedpackaging.com/suppliers/products/overcap"
]


# JSON file to store results
output_file = "./impacked/suppliers.json"

# Setup ChromeDriver
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# Initialize an empty list for storing extracted data
scraped_data = []

# Load existing data if the JSON file already exists
try:
    with open(output_file, "r") as file:
        scraped_data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    scraped_data = []

# Function to extract all supplier names and links from a page
def extract_suppliers():
    suppliers = []
    try:
        # Find all supplier name elements
        name_elements = driver.find_elements(By.CSS_SELECTOR, "div.text-lg.lg\\:text-2xl")

        # Find all supplier link elements
        link_elements = driver.find_elements(By.CSS_SELECTOR, "a.text-greenTwo")

        # Ensure name and link counts match
        for name_elem, link_elem in zip(name_elements, link_elements):
            supplier_name = name_elem.text.strip()
            supplier_link = link_elem.get_attribute("href")
            suppliers.append({"name": supplier_name, "link": supplier_link})

    except Exception as e:
        print(f"Error extracting suppliers: {e}")

    return suppliers

# Scrape each URL
for url in urls:
    print(f"Visiting: {url}")
    driver.get(url)
    time.sleep(5)  # Allow time for the page to load

    suppliers = extract_suppliers()
    if suppliers:
        scraped_data.extend(suppliers)
        # Save to JSON file        
        with open(output_file, "w") as file:
            json.dump(scraped_data, file, indent=4)

# Close the browser
driver.quit()

print("Scraping completed! Data saved to suppliers.json.")

