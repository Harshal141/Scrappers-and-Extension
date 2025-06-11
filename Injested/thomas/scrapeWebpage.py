import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

website = "https://www.thomasnet.com/suppliers/search?cov=NA&heading=96007083&searchsource=suppliers&searchterm=beauty+care&what=Beauty+Care+Products"
output_file = "./Injested/thomas/urlList.json"
total_pages = 16

# Ensure the output file exists and is valid JSON
if not os.path.exists(output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("[]")

# Initialize WebDriver
driver = webdriver.Chrome()

try:
    print("You have 70 seconds to log in manually.")
    # Before login visit a random website, 
    # open a new tab and add rubish into it. 
    # thenn visit the home tage thomasnet.com
    # log in using credentials and wait to get all the pagginated outputs scraped.
    time.sleep(70)
    for page in range(1, total_pages + 1):  # Adjust range to fit the desired pages
        url = f"{website}{page}/"
        print(f"Processing page {page}...")
        driver.get(url)

        # Wait until the supplier container is present
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "search-results_supplierListContainer__tD4DJ"))
        )

        # Find all company divs
        showcase = driver.find_element(By.CLASS_NAME, "search-results_supplierListContainer__tD4DJ")
        companies = showcase.find_elements(By.CLASS_NAME, "search-result-supplier_searchResultSupplierPanel__HdR9H")

        page_data = []
        for coman in companies:
            try:
                # Use a scoped XPath relative to the current `coman`
                supplier_link = coman.find_element(By.XPATH, ".//h2[@class='mar-r-1 txt-medium']//a")

                # Extract link text and href
                link_url = supplier_link.get_attribute("href")
                link_text = supplier_link.text.strip()

                if link_url and link_text:
                    page_data.append({
                        "name": link_text,
                        "relDomain": link_url
                    })

            except Exception as inner_e:
                print(f"Error extracting data from a company element: {inner_e}")

        # Append new data to the JSON file
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
