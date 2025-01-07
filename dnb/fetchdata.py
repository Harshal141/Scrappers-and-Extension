import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

base_url = "https://www.dnb.com/business-directory/company-information.animal_slaughtering_and_processing.ca.html?page="
output_file = "./dnb/DNB_list.json"
startIndex = 1
endIndex = 20

# # TODO: remove this if already a json file 
# with open(output_file, "w", encoding="utf-8") as file:
#     file.write("[]")

try:
    for page in range(startIndex, endIndex +1):  # Loop through pages 21 to 180
        # Construct the URL for the current page
        url = f"{base_url}{page}"
        driver.get(url)
        
        # Wait for the page to load completely
        time.sleep(2)

        # Temporary data storage for this page
        page_data = []

        # Locate the div containing the results
        try:
            company_results_div = driver.find_element(By.ID, "companyResults")
            a_tags = company_results_div.find_elements(By.TAG_NAME, "a")
            
            # Extract company name and domain from each <a> tag
            for a in a_tags:
                company_name = a.text.strip()  # Get the text (company name)
                domain = a.get_attribute("href")  # Get the href attribute (domain)
                
                # Skip if either value is missing
                if company_name and domain:
                    page_data.append({
                        "name": company_name,
                        "domain": domain
                    })

        except Exception as e:
            print(f"Error processing page {page}: {e}")

        with open(output_file, "r+", encoding="utf-8") as file:
            existing_data = json.load(file)
            existing_data.extend(page_data)
            file.seek(0)
            json.dump(existing_data, file, indent=4)

        print(f"Completed page {page}, added {len(page_data)} companies.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
