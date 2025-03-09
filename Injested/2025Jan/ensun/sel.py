import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome = webdriver.Chrome()

# paths = [
#     {"name": "FNB_US_SP", "pageSize": 6, "url": "https://ensun.io/search?threshold=VERY_LOW&q=Food%20and%20Beverage&page=&locations=United%20States%2Cnull%2Cnull&categories=SERVICE_PROVIDER"},
#     {"name": "FNB_US_MF", "pageSize": 6, "url": "https://ensun.io/search?threshold=VERY_LOW&q=Food%20and%20Beverage&page=&locations=United%20States%2Cnull%2Cnull&categories=MANUFACTURER"},
#     {"name": "FNB_US_D", "pageSize": 2, "url": "https://ensun.io/search?threshold=VERY_LOW&q=Food%20and%20Beverage&page=&locations=United%20States%2Cnull%2Cnull&categories=DISTRIBUTOR"},
#     {"name": "FNB_CA_SP", "pageSize": 6, "url": "https://ensun.io/search?threshold=VERY_LOW&q=Food%20and%20Beverage&page=&locations=Canada%2Cnull%2Cnull&categories=SERVICE_PROVIDER"},
#     {"name": "FNB_CA_MF", "pageSize": 6, "url": "https://ensun.io/search?threshold=VERY_LOW&q=Food%20and%20Beverage&page=&locations=Canada%2Cnull%2Cnull&categories=MANUFACTURER"},
#     {"name": "PAC_US_SP", "pageSize": 6, "url": "https://ensun.io/search?threshold=VERY_LOW&q=Packaging&page=&locations=United%20States%2Cnull%2Cnull&categories=SERVICE_PROVIDER"},
#     {"name": "PAC_US_MF", "pageSize": 6, "url": "https://ensun.io/search?threshold=VERY_LOW&q=Packaging&page=&locations=United%20States%2Cnull%2Cnull&categories=MANUFACTURER"},
#     {"name": "PAC_US_D", "pageSize": 2, "url": "https://ensun.io/search?threshold=VERY_LOW&q=Packaging&page=&locations=United%20States%2Cnull%2Cnull&categories=DISTRIBUTOR"},
#     {"name": "PAC_CA_SP", "pageSize": 6, "url": "https://ensun.io/search?threshold=VERY_LOW&q=Packaging&page=&locations=Canada%2Cnull%2Cnull&categories=SERVICE_PROVIDER"},
#     {"name": "PAC_CA_MF", "pageSize": 6, "url": "https://ensun.io/search?threshold=VERY_LOW&q=Packaging&page=&locations=Canada%2Cnull%2Cnull&categories=MANUFACTURER"},
#     {"name": "PAC_CA_D", "pageSize": 1, "url": "https://ensun.io/search?threshold=VERY_LOW&q=Packaging&locations=Canada%2Cnull%2Cnull&categories=DISTRIBUTOR"},
# ]
paths = [
    {"name": "FNB_US_SP", "pageSize": 6, "url": "https://ensun.io/search?threshold=VERY_LOW&q=Private%20Label%20Food&page=&locations=United%20States%2Cnull%2Cnull&categories=SERVICE_PROVIDER"},
    {"name": "FNB_US_MF", "pageSize": 6, "url": "https://ensun.io/search?threshold=VERY_LOW&q=Private%20Label%20Food&page=&locations=United%20States%2Cnull%2Cnull&categories=MANUFACTURER"},
    {"name": "FNB_US_D", "pageSize": 3, "url": "https://ensun.io/search?threshold=VERY_LOW&q=Private%20Label%20Food&page=&locations=United%20States%2Cnull%2Cnull&categories=DISTRIBUTOR"},
    {"name": "FNB_CA_SP", "pageSize": 6, "url": "https://ensun.io/search?threshold=VERY_LOW&q=Private%20Label%20Food&page=&locations=Canada%2Cnull%2Cnull&categories=SERVICE_PROVIDER"},
    {"name": "FNB_CA_MF", "pageSize": 6, "url": "https://ensun.io/search?threshold=VERY_LOW&q=Private%20Label%20Food&page=&locations=Canada%2Cnull%2Cnull&categories=MANUFACTURER"},
    {"name": "PAC_US_SP", "pageSize": 6, "url": "https://ensun.io/search?threshold=VERY_LOW&q=Food%20Ingredient&page=&locations=United%20States%2Cnull%2Cnull&categories=SERVICE_PROVIDER"},
    {"name": "PAC_US_MF", "pageSize": 6, "url": "https://ensun.io/search?threshold=VERY_LOW&q=Food%20Ingredient&page=&locations=United%20States%2Cnull%2Cnull&categories=MANUFACTURER"},
    {"name": "PAC_US_D", "pageSize": 3, "url": "https://ensun.io/search?threshold=VERY_LOW&q=Food%20Ingredient&page=&locations=United%20States%2Cnull%2Cnull&categories=DISTRIBUTOR"},
    {"name": "PAC_CA_SP", "pageSize": 6, "url": "https://ensun.io/search?threshold=VERY_LOW&q=Food%20Ingredient&page=&locations=Canada%2Cnull%2Cnull&categories=SERVICE_PROVIDER"},
    {"name": "PAC_CA_MF", "pageSize": 6, "url": "https://ensun.io/search?threshold=VERY_LOW&q=Food%20Ingredient&page=&locations=Canada%2Cnull%2Cnull&categories=MANUFACTURER"},
    {"name": "PAC_CA_D", "pageSize": 1, "url": "https://ensun.io/search?threshold=VERY_LOW&q=Food%20Ingredient&locations=Canada%2Cnull%2Cnull&categories=DISTRIBUTOR"},
]

def generate_url(name, page_number):
    for path in paths:
        if path["name"] == name:
            return path["url"].replace("page=", f"page={page_number}")
    return None

def scrape_companies(name, max_page):
    records = []
    for page in range(1, max_page + 1):
        url = generate_url(name, page)
        if not url:
            continue

        chrome.get(url)
        time.sleep(5)  # Wait for the page to load

        while True:
            try:
                company_elements = WebDriverWait(chrome, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation1.mui-1vj0kx"))
                )
                break
            except:
                print("Retrying to load elements...")
                time.sleep(3)

        total_companies = len(company_elements)
        print(f"Total companies on page {page}: {total_companies}")

        for i in range(total_companies):
            try:
                # Re-find the elements after navigation
                company_elements = WebDriverWait(chrome, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation1.mui-1vj0kx"))
                )
                company = company_elements[i].find_element(By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-body1.mui-vpiwmb")
                company_name = company.text
                print(f"Scraping {company_name}")

                # Click on the company element
                company.click()
                time.sleep(3)

                try:
                    # Extract the company URL
                    link_element = WebDriverWait(chrome, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//a[.//button[contains(text(), 'Go to website')]]"))
                    )
                    if link_element:
                        company_url = link_element.get_attribute("href")
                        records.append({"name": company_name, "url": company_url})
                        print(f"Scraped {company_name}: {company_url}")
                except:
                    print(f"No website found for {company_name}")

                # Navigate back to the list page
                chrome.back()

                # Wait for elements to reload before clicking the next one
                WebDriverWait(chrome, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation1.mui-1vj0kx"))
                )

            except Exception as e:
                print(f"Error scraping company {i + 1}: {e}")
                continue

    return records

# Scrape data for all paths
all_records = []
for path in paths:
    all_records += scrape_companies(path["name"], path["pageSize"])

# Save to a JSON file
with open("company_data.json", "w") as json_file:
    json.dump(all_records, json_file, indent=4)

chrome.quit()
