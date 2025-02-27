import json
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Setup headless Chrome browser
def setup_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Function to get the final redirected URL
def get_redirected_url(driver, url):
    try:
        driver.get(url)
        time.sleep(5)  # Allow time for redirects
        return driver.current_url
    except Exception as e:
        print(f"[❌] Failed to fetch redirect for {url}: {e}")
        return "N/A"

# Clean the domain
def clean_domain(domain_name):
    website = domain_name.strip().lower()
    if website.endswith("/"):
        website = website[:-1]
    website = website.replace("http://", "").replace("https://", "").replace("www.", "")
    website = website.split("/")[0]
    return website

# Load existing JSON data
with open('workshop/buyersguide/company_data.json', 'r') as f:
    data = json.load(f)

driver = setup_driver()
output_data = []

# Process each entry
for entry in data:
    redirected_url = get_redirected_url(driver, entry["Domain"])
    cleaned_domain = clean_domain(redirected_url)
    output_data.append({'Title': entry['Title'], 'OriginalDomain': cleaned_domain})
    print(f"[✅] {entry['Title']} | Cleaned Domain: {cleaned_domain}")

driver.quit()

# Save to CSV
csv_file = 'workshop/buyersguide/company_data_cleaned.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Title', 'OriginalDomain'])
    writer.writeheader()
    writer.writerows(output_data)

print(f"[💾] Data saved to CSV: {csv_file}")
