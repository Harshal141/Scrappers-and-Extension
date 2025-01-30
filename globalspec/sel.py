from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json


# Define the number of pages to scrape
page_max = 39  # Adjust if needed

# Base URL
a_url = "https://www.globalspec.com/SpecSearch/SuppliersByName/AllSuppliers/A/"

data = []

for i in range(1, page_max + 1):

    # Initialize WebDriver
    driver = webdriver.Chrome()
    url = f"{a_url}{i}"  # Construct URL dynamically
    print(f"Fetching: {url}")

    driver.get(url)

    # Wait until table rows are loaded (adjust timeout if needed)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tr.result-item"))
        )
    except Exception as e:
        print("Timeout waiting for elements:", e)

    # Find all supplier rows
    table_rows = driver.find_elements(By.CSS_SELECTOR, "tr.result-item")

    for row in table_rows:
        location = row.find_element(By.CSS_SELECTOR, ".hq").text.strip()
        if "United States" in location or "Canada" in location:
            info_element = row.find_element(By.CSS_SELECTOR, ".name")
            info_child = info_element.find_element(By.CSS_SELECTOR, "a")
            name = info_child.text.strip()
            url = info_child.get_attribute("href")
            print(f"Found: {name} - {location} - {url}")

            data.append({"name": name, "url": url})
            
    # Close browser
    driver.quit()
    

# store to json file
with open("./globalspec/output_1.json", "w") as f:
    json.dump(data, f, indent=4)

