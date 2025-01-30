import urllib.parse
import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load input JSON file
input_file = "./globalspec/output_1.json"
output_file = "./globalspec/output_2.json"

# Read input data
with open(input_file, "r") as f:
    json_data = json.load(f)

# Load existing output data (to avoid duplicates if script is interrupted)
if os.path.exists(output_file):
    with open(output_file, "r") as f:
        data_out = json.load(f)
else:
    data_out = []

# Track progress
batch_size = 500
batch_count = len(data_out)  # Start from the last saved index

# Initialize WebDriver once (reduces overhead)
driver = webdriver.Chrome()

try:
    for company in json_data[batch_count:]:  # Resume from last batch
        try:
            company_name = company["name"]
            profile_url = company["url"]

            # Open the supplier profile page
            print(f"Fetching: {profile_url}")
            driver.get(profile_url)

            # Wait for the supplier website button
            try:
                supplier_link_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a.icon-accompanying-link.blue-arrow-left"))
                )

                # Extract tracking URL
                tracking_url = supplier_link_element.get_attribute("href")

                # Parse and decode actual supplier site URL
                parsed_url = urllib.parse.parse_qs(urllib.parse.urlparse(tracking_url).query)
                actual_url = parsed_url.get("gotoUrl", [""])[0]  # Extract first element
                decoded_url = urllib.parse.unquote(actual_url)

                print(f"✅ Extracted: {company_name} -> {decoded_url}")

                # Store extracted data
                data_out.append({"name": company_name, "url": decoded_url})

            except Exception as e:
                print(f"❌ Could not extract URL for {company_name}: {e}")

            # Slow down requests to prevent detection
            time.sleep(3)

            # Save in batches of 500
            if len(data_out) % batch_size == 0:
                print("💾 Saving batch progress...")
                with open(output_file, "w") as f:
                    json.dump(data_out, f, indent=4)

        except Exception as e:
            print(f"🚨 Error processing company {company_name}: {e}")

finally:
    # Save any remaining data
    print("💾 Final save...")
    with open(output_file, "w") as f:
        json.dump(data_out, f, indent=4)

    # Close the browser
    driver.quit()

print("✅ Script finished successfully.")
