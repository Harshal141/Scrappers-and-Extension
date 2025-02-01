import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

input_file = "impacked/suppliers_uniq.json"
output_file = "impacked/DATA_317_suppliers.json"

# Load supplier data
try:
    with open(input_file, "r") as file:
        suppliers = json.load(file)
except FileNotFoundError:
    print("Input file not found!")
    suppliers = []

# Setup Selenium WebDriver
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Run in headless mode (no GUI)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Initialize list for storing extracted URLs
extracted_data = []

# Scrape each supplier page for external website URL
for supplier in suppliers:
    name = supplier["name"]
    supplier_url = supplier["link"]

    print(f"Visiting: {supplier_url}")
    driver.get(supplier_url)
    time.sleep(5)  # Allow page to load

    try:
        # Find the "Learn more at" text
        learn_more_element = driver.find_element(By.XPATH, "//div[contains(text(), 'Learn more at')]")

        # Find the next <a> tag (which contains the external URL)
        external_link_element = learn_more_element.find_element(By.XPATH, "./following-sibling::a")
        external_url = external_link_element.get_attribute("href")

        # Store extracted data
        extracted_data.append({"name": name, "url": external_url})
        print(f"Extracted: {name} - {external_url}")

        # Save after each successful extraction
        with open(output_file, "w") as file:
            json.dump(extracted_data, file, indent=4)

    except Exception as e:
        print(f"Error extracting data from {supplier_url}: {e}")

# Close the browser
driver.quit()

print(f"Scraping completed! Data saved to {output_file}.")
