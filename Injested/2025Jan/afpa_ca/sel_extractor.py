from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
import time

# Initialize WebDriver
driver = webdriver.Chrome()

# Base URL
base_url = "https://www.afpa.com/member-directory/page/{}/?wpbdp_view=all_listings"

# Data storage
data = []

# Loop through pages 1 to 33
for page in range(1, 34):
    url = base_url.format(page)
    driver.get(url)

    # Allow the page to load completely
    time.sleep(2)

    # Find all divs with class name 'listing-title'
    divs = driver.find_elements(By.CLASS_NAME, "listing-title")

    for div in divs:
        try:
            # Get the anchor tag inside the div
            a_tag = div.find_element(By.TAG_NAME, "a")
            name = a_tag.text  # Get the text inside the anchor tag
            link = a_tag.get_attribute("href")  # Get the URL from the href attribute

            # Append to data list
            data.append({"name": name, "domain": link})
        except Exception as e:
            print(f"Error processing div: {e}")

# Close the WebDriver
driver.quit()

# Save data to a JSON file
output_file = "./afpa_ca/afpa_listings.json"
with open(output_file, "w") as f:
    json.dump(data, f, indent=4)

print(f"Data saved to {output_file}")