import json
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from utility import cleanDomain

# Initialize WebDriver
driver = webdriver.Chrome()

# Input JSON file
input_file = "./afpa_ca/afpa_listings.json"
output_csv_file = "./afpa_ca/DATA-267.csv"

# Load data from the JSON file
with open(input_file, "r") as f:
    data = json.load(f)

# New data structure for updated domains
updated_data = []

for entry in data:
    name = entry.get("name")
    domain = entry.get("domain")

    if not domain:
        continue

    try:
        # Visit the domain URL
        driver.get(domain)

        # Allow the page to load completely
        time.sleep(2)

        # Look for the div with class name 'listing-details'
        try:
            listing_details_div = driver.find_element(By.CLASS_NAME, "listing-details")

            # Search for the <a> tag within the div
            a_tag = listing_details_div.find_element(By.TAG_NAME, "a")
            if a_tag:
                new_domain = a_tag.get_attribute("href")  # Extract the real domain
                cleaned_domain = cleanDomain(new_domain)
                updated_data.append({"Name": name, "Domain": cleaned_domain})
        except Exception:
            # Skip if 'listing-details' or <a> tag not found
            print(f"No valid 'listing-details' or <a> tag found for {domain}")

    except Exception as e:
        print(f"Error visiting {domain}: {e}")

# Close the WebDriver
driver.quit()


# Save updated data to a CSV file
with open(output_csv_file, "w", newline="") as csvfile:
    fieldnames = ["Name", "Domain"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for entry in updated_data:
        writer.writerow(entry)

print(f"Updated data saved to {output_csv_file}")