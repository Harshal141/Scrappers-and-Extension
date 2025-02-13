import json
import os
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


website = "https://www.lusha.com/company-search/food-and-beverage-manufacturing/37c596cb49/canada/193/page"
output_file = os.path.join(os.getcwd(), "urlList.json")
total_pages = 14


max_retries = 5      
base_delay = 5        


if not os.path.exists(output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("[]")


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/114.0.0.0 Safari/537.36"
)
chrome_options.add_argument("--headless")


driver = webdriver.Chrome(options=chrome_options)

try:
    for page in range(1, total_pages + 1):
        page_url = f"{website}/{page}/"
        attempt = 0
        success = False
        
        
        while attempt < max_retries and not success:
            try:
                print(f"Loading page {page}, attempt {attempt + 1}...")
                driver.get(page_url)

                
                WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "directory-content-box-col"))
                )
                success = True  # If we get here, the page loaded successfully.
            except (TimeoutException, WebDriverException) as e:
                attempt += 1
                wait_time = base_delay * attempt  # exponential backoff
                print(f"Error loading page {page} (attempt {attempt}): {e}")
                print(f"Waiting for {wait_time} seconds before retrying...")
                time.sleep(wait_time)
        
        if not success:
            print(f"Skipping page {page} after {max_retries} failed attempts.")
            continue

        # Extract data from the page
        try:
            showcase = driver.find_element(By.CLASS_NAME, "directory-content")
            companies = showcase.find_elements(By.CLASS_NAME, "directory-content-box-col")
        except Exception as e:
            print(f"Could not find company elements on page {page}: {e}")
            continue

        page_data = []
        for company_div in companies:
            try:
                # Locate the <a> tag inside the company div
                link = company_div.find_element(By.TAG_NAME, "a")
                company_name = link.text.strip()  # Get the company name
                domain = link.get_attribute("href")  # Get the domain (URL)

                if company_name and domain:
                    page_data.append({
                        "name": company_name,
                        "domain": domain
                    })
            except Exception as inner_e:
                print(f"Error extracting data from an element on page {page}: {inner_e}")

        # Append page data to the JSON file
        try:
            with open(output_file, "r+", encoding="utf-8") as file:
                try:
                    existing_data = json.load(file)
                except json.JSONDecodeError:
                    existing_data = []

                existing_data.extend(page_data)
                file.seek(0)
                json.dump(existing_data, file, indent=4)
        except Exception as file_e:
            print(f"Error writing data to JSON file: {file_e}")

        print(f"Completed page {page}, added {len(page_data)} companies.")

        # Wait a random amount of time before moving to the next page to avoid rate limiting
        sleep_time = random.uniform(2, 6)
        print(f"Sleeping for {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)

except Exception as e:
    print(f"An error occurred in the main loop: {e}")

finally:
    driver.quit()
