import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from utility import cleanDomain
import os

# File directory and naming
input_dir = "./dnb/"
output_prefix = "src_"
file_base_name = "DNB_sheet_"

# Initialize WebDriver
driver = webdriver.Chrome()

# Helper function to read existing data from a JSON file
def read_json_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return []

# Helper function to append data to a JSON file
def append_to_json_file(file_path, new_data):
    current_data = read_json_file(file_path)
    updated_data = current_data + new_data
    with open(file_path, 'w') as file:
        json.dump(updated_data, file, indent=4)

# Process all files (DNB_sheet_1.json to DNB_sheet_8.json)
for i in range(5, 6):  # Loop through 3 to 5
    file_name = f"{file_base_name}{i}.json"
    print(f"Processing {file_name}...")
    input_path = os.path.join(input_dir, file_name)
    output_path = os.path.join(input_dir, f"{output_prefix}{file_name}")
    
    # Load the JSON file
    with open(input_path, 'r') as file:
        data = json.load(file)

    output_data = []
    seen_domains = set()
    index = 1

    # Loop through each entry in the JSON
    for entry in data:
        url = entry.get("url_src")
        if not url:
            continue

        # Visit the URL
        driver.get(url)
        time.sleep(5)  # Wait for the page to load completely

        # Extract the "Doing Business As" name
        try:
            business_as_element = driver.find_element(
                By.XPATH,
                '//span[@class="company_data_point" and @name="company_name"]/span'
            )
            business_as_name = business_as_element.text
        except Exception as e:
            business_as_name = entry.get("name")
            print(f"Error finding 'Doing Business As': {url}")

        # Extract the domain
        try:
            domain_element = driver.find_element(
                By.XPATH,
                '//span[@class="company_data_point" and @name="company_website"]//a'
            )
            domain = domain_element.get_attribute("href")
            domain = cleanDomain(domain)

            # Check for duplicate domains
            if domain not in seen_domains:
                output_data.append({
                    "index": index,
                    "name": business_as_name,
                    "url": domain
                })
                seen_domains.add(domain)
                index += 1

                # Write to file every 100 completions
                if len(output_data) >= 100:
                    append_to_json_file(output_path, output_data)
                    output_data = []  # Clear the batch after saving
        except Exception as e:
            print(f"Error finding domain: {url}")

    # Append remaining data to the file
    if output_data:
        append_to_json_file(output_path, output_data)

# Close the browser
driver.quit()
