from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import json

# Load URLs from JSON
input_file = "./WFF/urls.json"
base_url = "https://wff2025.mapyourshow.com"

with open(input_file, "r", encoding="utf-8") as f:
    urls = json.load(f)

driver = webdriver.Chrome()

# Extracted data
results = []

for item in urls:
    full_url = base_url + item["url"]
    print(f"Visiting: {full_url}")
    driver.get(full_url)

    try:
        # Extract Address
        address = driver.find_element(By.CSS_SELECTOR, "p.showcase-address").text.strip()
    except NoSuchElementException:
        address = None

    try:
        domain = driver.find_element(By.CSS_SELECTOR, "ul.showcase-web-phone a").get_attribute("href").strip()
    except NoSuchElementException:
        domain = None

    try:
        # Extract Domain and Phone
        phone = driver.find_element(By.CSS_SELECTOR, "ul.showcase-web-phone li span.muted").find_element(By.XPATH, "..").text.strip()
    except NoSuchElementException:
        phone = None

    try:
        # Extract Product Categories
        product_section = driver.find_element(By.ID, "scroll-products")
        headings = [
            h4.text.strip()
            for h4 in product_section.find_elements(By.CSS_SELECTOR, "h4.color-brand-02")
        ]
    except NoSuchElementException:
        headings = None

    # Check if essential data is missing
    if not (domain):
        print(f"Data missing for: {full_url}")

    data = {
        "name" : item["name"],
        "url": full_url,
        "address": address,
        "domain": domain,
        "phone": phone,
        "product_categories": headings
    }
    print(data)
    results.append(data)

# Save results to JSON
output_file = "./WFF/extracted_data.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

print(f"Extraction complete. Results saved to {output_file}.")

# Close the WebDriver
driver.quit()
