import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# List of website IDs and their corresponding URLs
websites = {
    "OFM_CA": "https://www.dnb.com/business-directory/company-information.other_fabricated_metal_product_manufacturing.ca.html",
}


output_file = "./dnb/DNB_sheet_8.json"

# Ensure the output file exists and initialize as an empty list if not already present
try:
    with open(output_file, "r", encoding="utf-8") as file:
        pass
except FileNotFoundError:
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("[]")

driver = webdriver.Chrome()

try:
    for website_id, base_url in websites.items():
        print(f"Processing {website_id}: {base_url}")

        # Access the first page to determine the total number of results
        driver.get(base_url)
        time.sleep(2)
        
        try:
            # Extract the total results from the <div class="results-summary">
            results_summary_div = driver.find_element(By.CLASS_NAME, "results-summary")
            total_results_text = results_summary_div.text.split()[-1].replace(",", "")
            total_results = int(total_results_text)
            total_pages = min((total_results + 49) // 50, 20)  # Divide by 50 and cap at 20

            print(f"Total results: {total_results}, Total pages: {total_pages}")
        except Exception as e:
            print(f"Error retrieving total results for {website_id}: {e}")
            continue

        # Loop through the pages
        for page in range(1, total_pages + 1):
            url = f"{base_url}?page={page}"
            driver.get(url)
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
                            "id": website_id,
                            "name": company_name,
                            "domain": domain
                        })

            except Exception as e:
                print(f"Error processing page {page} of {website_id}: {e}")
            
            # Append page data to the JSON file
            with open(output_file, "r+", encoding="utf-8") as file:
                existing_data = json.load(file)
                existing_data.extend(page_data)
                file.seek(0)
                json.dump(existing_data, file, indent=4)

            print(f"Completed page {page} of {website_id}, added {len(page_data)} companies.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
