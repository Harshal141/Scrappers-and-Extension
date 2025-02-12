import json
import os
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

def create_driver():
    """Initialize a headless Chrome WebDriver with images disabled for efficiency."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Run in headless mode for speed
    chrome_options.add_argument("--disable-gpu")
    # Disable image loading to speed up page loads
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(options=chrome_options)

def process_company(company):
    """
    Process a single company URL from the input file and extract the desired info.
    Returns a dictionary with the company name and domain if successful, or None.
    """
    lusha_url = company.get("domain")
    if not lusha_url:
        return None

    max_retries = 5
    base_delay = 3  # seconds for exponential backoff
    attempt = 0
    result = None
    driver = create_driver()

    while attempt < max_retries:
        try:
            print(f"Loading {lusha_url} (Attempt {attempt + 1})...")
            driver.get(lusha_url)
            # Wait for the hero section to be present; adjust the timeout if needed
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.company-hero-info"))
            )
            break  # Success; exit retry loop
        except (TimeoutException, WebDriverException) as e:
            attempt += 1
            wait_time = base_delay * attempt  # Exponential backoff
            print(f"Error loading {lusha_url}: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    else:
        # Exhausted all retries; skip this URL.
        print(f"Skipping {lusha_url} after {max_retries} failed attempts.")
        driver.quit()
        return None

    try:
        # Extract the company name from the <h1> element with class "company-hero-title"
        name_element = driver.find_element(By.CSS_SELECTOR, "div.company-hero-info h1.company-hero-title")
        company_name = name_element.text.strip()

        # Extract the domain link from the first valid <a> element (skip anchors with href="#")
        anchor_elements = driver.find_elements(By.CSS_SELECTOR, "div.company-hero-info a")
        domain_link = None
        for a in anchor_elements:
            href = a.get_attribute("href")
            if href and href != "#":
                domain_link = href.strip()
                break

        if company_name and domain_link:
            result = {
                "name": company_name,
                "domain": domain_link
            }
            print(f"Extracted: {company_name} - {domain_link}")
        else:
            print(f"Data not found on {lusha_url}")
    except Exception as e:
        print(f"Error extracting data from {lusha_url}: {e}")

    driver.quit()
    # Short random delay to mimic human behavior and avoid being too "robotic"
    time.sleep(random.uniform(0.5, 1.5))
    return result

def write_batch_to_file(batch, output_file):
    """
    Append each result (a JSON object) as a new line in the output file.
    Using JSON Lines minimizes file I/O overhead.
    """
    with open(output_file, "a", encoding="utf-8") as f:
        for item in batch:
            json.dump(item, f)
            f.write("\n")

def main():
    # Define the input and output file paths (assumed to be in the project root)
    input_file = os.path.join(os.getcwd(), "urlList.json")
    # We use the .jsonl extension for newline-delimited JSON objects.
    output_file = os.path.join(os.getcwd(), "extractedData_parallel.json")

    # Ensure the output file exists and is empty.
    open(output_file, "w", encoding="utf-8").close()

    # Load the list of companies from urlList.json
    with open(input_file, "r", encoding="utf-8") as f:
        companies_list = json.load(f)

    total = len(companies_list)
    processed_count = 0
    batch_results = []
    batch_size = 500  # Write to file after every 500 successful extractions

    # Process companies sequentially
    for company in companies_list:
        result = process_company(company)
        processed_count += 1
        if result:
            batch_results.append(result)

        remaining = total - processed_count
        print(f"Progress: {processed_count}/{total} processed, {remaining} remaining.")

        # Once the batch reaches 500 items, write them to the file and reset the batch.
        if len(batch_results) >= batch_size:
            write_batch_to_file(batch_results, output_file)
            batch_results = []  # Clear the batch after writing
            print("Batch of 500 written to file.")

    # Write any remaining items in the batch to the file.
    if batch_results:
        write_batch_to_file(batch_results, output_file)
        print("Final batch written to file.")

    print(f"Data extraction complete. Final results saved to {output_file}")

if __name__ == "__main__":
    main()
