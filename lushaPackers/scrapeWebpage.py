import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# URL and Output Settings
website = "https://www.lusha.com/company-search/packaging-and-containers-manufacturing/e06d5facdd/united-states/11/page"
output_file = "./lushaPackers/urlList.json"
total_pages = 37

# Ensure the output file exists and is valid JSON
if not os.path.exists(output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("[]")

# Initialize WebDriver
driver = webdriver.Chrome()

try:
    for page in range(31, total_pages + 1):
        url = f"{website}/{page}/"
        driver.get(url)

        # Wait until the desired elements are present on the page
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "directory-content-box-col"))
        )

        # Find all company divs
        showcase = driver.find_element(By.CLASS_NAME, "directory-content")
        companies = showcase.find_elements(By.CLASS_NAME, "directory-content-box-col")
        page_data = []

        for coman in companies:
            try:
                # Locate the <a> tag inside the company div
                link = coman.find_element(By.TAG_NAME, "a")
                company_name = link.text.strip()  # Get the company name
                domain = link.get_attribute("href")  # Get the domain (URL)

                if company_name and domain:
                    page_data.append({
                        "name": company_name,
                        "domain": domain
                    })
            except Exception as inner_e:
                print(f"Error extracting data from an element: {inner_e}")

        # Append page data to the JSON file
        with open(output_file, "r+", encoding="utf-8") as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []

            existing_data.extend(page_data)
            file.seek(0)
            json.dump(existing_data, file, indent=4)

        print(f"Completed page {page}, added {len(page_data)} companies.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
