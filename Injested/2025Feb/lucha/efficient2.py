import json
import os
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

def load_proxies():
    """
    Load proxies from 'free_proxy_list.json' and return a list of proxy strings.
    Each proxy string is built as: "<protocol>://<ip>:<port>".
    """
    proxies_file = os.path.join(os.getcwd(), "Free_Proxy_List.json")
    try:
        with open(proxies_file, "r", encoding="utf-8") as f:
            proxies_data = json.load(f)
    except Exception as e:
        print(f"Error loading proxy file: {e}")
        return []

    proxies_list = []
    for record in proxies_data:
        # Use the first protocol if available, otherwise default to "http"
        protocol = (record.get("protocols", ["http"])[0]).lower()
        ip = record.get("ip")
        port = record.get("port")
        if ip and port:
            proxy_str = f"{protocol}://{ip}:{port}"
            proxies_list.append(proxy_str)
    print(f"Loaded {len(proxies_list)} proxies.")
    return proxies_list

def get_random_proxy(proxies):
    """Return a random proxy string from the given list."""
    if proxies:
        return random.choice(proxies)
    return None

def create_driver(proxy=None):
    """
    Initialize a headless Chrome WebDriver with images disabled.
    Optionally uses the specified proxy.
    """
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    # Disable images to speed up loading
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    if proxy:
        chrome_options.add_argument(f"--proxy-server={proxy}")
        print(f"Driver will use proxy: {proxy}")
    return webdriver.Chrome(options=chrome_options)

def process_company(driver, company):
    """
    Using the provided driver, process one company URL and extract data.
    Returns a dict with the company name and domain, or None on failure.
    """
    lusha_url = company.get("domain")
    if not lusha_url:
        return None

    max_retries = 5
    base_delay = 3  # seconds for exponential backoff
    attempt = 0
    result = None

    while attempt < max_retries:
        try:
            print(f"Loading {lusha_url} (Attempt {attempt + 1})...")
            driver.get(lusha_url)
            # Wait until the hero section is present
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.company-hero-info"))
            )
            break  # Successfully loaded the page
        except (TimeoutException, WebDriverException) as e:
            attempt += 1
            wait_time = base_delay * attempt
            print(f"Error loading {lusha_url}: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    else:
        print(f"Skipping {lusha_url} after {max_retries} failed attempts.")
        return None

    try:
        # Extract company name from the h1 element
        name_element = driver.find_element(By.CSS_SELECTOR, "div.company-hero-info h1.company-hero-title")
        company_name = name_element.text.strip()

        # Extract the first valid domain link from the hero section
        anchor_elements = driver.find_elements(By.CSS_SELECTOR, "div.company-hero-info a")
        domain_link = None
        for a in anchor_elements:
            href = a.get_attribute("href")
            if href and href != "#":
                domain_link = href.strip()
                break

        if company_name and domain_link:
            result = {"name": company_name, "domain": domain_link}
            print(f"Extracted: {company_name} - {domain_link}")
        else:
            print(f"Data not found on {lusha_url}")
    except Exception as e:
        print(f"Error extracting data from {lusha_url}: {e}")

    # Short random delay to mimic human behavior
    time.sleep(random.uniform(0.5, 1.5))
    return result

def write_batch_to_file(batch, output_file):
    """
    Append each result as a newline-delimited JSON object to the output file.
    """
    with open(output_file, "a", encoding="utf-8") as f:
        for item in batch:
            json.dump(item, f)
            f.write("\n")

def main():
    # File paths (assumed to be in the project root)
    input_file = os.path.join(os.getcwd(), "urlList.json")
    output_file = os.path.join(os.getcwd(), "extractedData_parallel.jsonl")
    
    # Clear the output file at the start
    open(output_file, "w", encoding="utf-8").close()

    # Load companies from urlList.json
    with open(input_file, "r", encoding="utf-8") as f:
        companies_list = json.load(f)

    total = len(companies_list)
    processed_count = 0
    batch_results = []
    batch_size = 500  # Write to file after every 500 successful extractions

    # Load proxies from file and prepare to rotate them
    proxies = load_proxies()
    
    driver = None
    for company in companies_list:
        # If there's no driver (or after finishing a batch), start a new one with a random proxy.
        if driver is None:
            proxy = get_random_proxy(proxies)
            driver = create_driver(proxy=proxy)
        
        result = process_company(driver, company)
        processed_count += 1

        if result:
            batch_results.append(result)
        remaining = total - processed_count
        print(f"Progress: {processed_count}/{total} processed, {remaining} remaining.")

        # When the batch size is reached, write to file and rotate the driver/proxy.
        if len(batch_results) >= batch_size:
            write_batch_to_file(batch_results, output_file)
            batch_results = []  # Reset batch
            print("Batch written to file. Rotating driver/proxy...")
            driver.quit()
            driver = None  # Next iteration will start a new driver with a new proxy

    # Write any remaining records in the batch to the file.
    if batch_results:
        write_batch_to_file(batch_results, output_file)
        print("Final batch written to file.")

    print(f"Data extraction complete. Final results saved to {output_file}")
    if driver:
        driver.quit()

if __name__ == "__main__":
    main()
