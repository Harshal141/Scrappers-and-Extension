import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from utility import cleanDomain

file_name = "DNB_sheet_1.json"

# Load the JSON file
with open("./dnb/" + file_name, 'r') as file:
    data = json.load(file)

driver = webdriver.Chrome()

output_data = []
seen_domains = set()  # To track unique domains
index = 1
slip = 0

# Loop through each entry in the JSON
for entry in data:
    slip += 1
    if slip == 3:
        break
    url = entry.get("url_src")
    if not url:
        continue

    # Visit the URL
    driver.get(url)
    time.sleep(3)  # Wait for the page to load completely

    # Extract the "Doing Business As" name
    try:
        business_as_element = driver.find_element(
            By.XPATH,
            '//span[@class="company_data_point" and @name="company_name"]/span'
        )
        business_as_name = business_as_element.text
    except Exception as e:
        business_as_name = "Not Found"
        print(f"Error finding 'Doing Business As': {e}")

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
    except Exception as e:
        print(f"Error finding domain: {e}")

# Close the browser
driver.quit()

# Save the output data to a file
with open("./dnb/src_"+ file_name, "w") as file:
    json.dump(output_data, file, indent=4)
