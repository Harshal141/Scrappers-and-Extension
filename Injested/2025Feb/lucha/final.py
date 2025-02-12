import json
import os
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# Input file (from previous run) and output file for the new extracted data
input_file = os.path.join(os.getcwd(), "urlList.json")
output_file = os.path.join(os.getcwd(), "extractedData.json")

# Load the list of companies from urlList.json
with open(input_file, "r", encoding="utf-8") as f:
    companies_list = json.load(f)

# Setup Chrome options (including a custom user-agent)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/114.0.0.0 Safari/537.36"
)
# Uncomment the following line to run Chrome in headless mode if desired
chrome_options.add_argument("--headless")

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Settings for retries (to handle potential rate limiting)
max_retries = 5   # Maximum number of attempts per URL
base_delay = 5    # Base delay in seconds for exponential backoff

extracted_data = []  # This will hold our final extracted results

for company in companies_list:
    # Use the Lusha business URL from your input file
    lusha_url = company.get("domain")
    if not lusha_url:
        continue

    attempt = 0
    success = False

    # Retry loop in case the page fails to load
    while attempt < max_retries and not success:
        try:
            print(f"Loading {lusha_url} (Attempt {attempt + 1})...")
            driver.get(lusha_url)
            # Wait until the hero section loads (adjust the timeout if needed)
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.company-hero-info"))
            )
            success = True  # The page loaded successfully
        except (TimeoutException, WebDriverException) as e:
            attempt += 1
            wait_time = base_delay * attempt  # Exponential backoff delay
            print(f"Error loading {lusha_url}: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)

    if not success:
        print(f"Skipping {lusha_url} after {max_retries} failed attempts.")
        continue

    try:
        # Extract the company name from the h1 element with class "company-hero-title"
        name_element = driver.find_element(By.CSS_SELECTOR, "div.company-hero-info h1.company-hero-title")
        company_name = name_element.text.strip()

        # Extract the domain link from the first valid <a> tag inside the company hero section
        # (Skip any <a> with href="#" such as "Read more")
        anchor_elements = driver.find_elements(By.CSS_SELECTOR, "div.company-hero-info a")
        domain_link = None
        for a in anchor_elements:
            href = a.get_attribute("href")
            if href and href != "#":
                domain_link = href.strip()
                break

        if not domain_link:
            print(f"No valid domain link found for {lusha_url}.")
            continue

        extracted_data.append({
            "name": company_name,
            "domain": domain_link
        })
        print(f"Extracted: {company_name} - {domain_link}")

    except Exception as extraction_error:
        print(f"Error extracting data from {lusha_url}: {extraction_error}")

    # Random delay before processing the next URL to help avoid rate limiting
    sleep_time = random.uniform(2, 6)
    print(f"Sleeping for {sleep_time:.2f} seconds...\n")
    time.sleep(sleep_time)

# Write the extracted results to a new JSON file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(extracted_data, f, indent=4)

print(f"Data extraction complete. Extracted data saved to {output_file}")

driver.quit()
