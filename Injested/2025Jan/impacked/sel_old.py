from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json
import os

# Setup Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Open in maximized mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-popup-blocking")
# chrome_options.add_argument("--headless")  # Uncomment to run in background mode

driver = webdriver.Chrome(options=chrome_options)

# Base URL for pagination
base_url = "https://www.impackedpackaging.com/products?page={}&unit=ml&manufacturing_locations=USA%2CCanada&favoriteSupplier=all"

# CSS Selector for product divs
product_selector = ".bg-white.h-full.active\\:bg-primaryActive"

# Output file path
output_path = "./impacked/output_1.json"

# Load existing output data (resumes from last completed page)
if os.path.exists(output_path):
    with open(output_path, "r") as f:
        saved_data = json.load(f)
else:
    saved_data = {}

driver.get("https://www.impackedpackaging.com/")
time.sleep(10)  # Allow time for the page to load

# Start scraping from the last completed page
for page in range(1, 100):
    print(f"\n🟢 Processing Page {page}...")

    # **Skip already processed pages**
    if str(page) in saved_data:
        print(f"✅ Page {page} already processed. Skipping...")
        continue

    page_urls = []  # Store URLs per page

    # Load the paginated URL
    driver.get(base_url.format(page))
    
    # Wait for the page to load
    wait = WebDriverWait(driver, 15)
    try:
        product_divs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, product_selector)))
        print(f"🔹 Found {len(product_divs)} products on page {page}.")
    except:
        print(f"⚠️ No products found on page {page}. Skipping...")
        continue  # Skip to the next page if no products are found

    # Process each product on the current page
    for index in range(len(product_divs)):  
        try:
            # **Re-fetch product list after navigation** to avoid stale references
            product_divs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, product_selector)))
            product = product_divs[index]  # Get the current product element

            print(f"➡️ Processing product {index + 1} of {len(product_divs)} on page {page}")

            # Scroll into view to avoid click issues
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", product)
            time.sleep(1)  # Allow time for stabilization

            # Click on the product to open its page
            product.click()
            time.sleep(4)  # Increased time to ensure full page load

            # Extract the product page URL
            product_url = driver.current_url
            page_urls.append(product_url)
            print(f"✅ Extracted: {product_url}")

            # Navigate back to the main page
            driver.back()
            time.sleep(5)  # Allow page to reload properly

        except Exception as e:
            print(f"⚠️ Error processing product {index + 1} on page {page}: {e}")
            continue  

    # **Save page-wise data incrementally**
    if page_urls:
        saved_data[str(page)] = page_urls
        with open(output_path, "w") as f:
            json.dump(saved_data, f, indent=4)
        print(f"💾 Page {page} saved successfully.")

# Close the browser
driver.quit()

print("\n✅ Scraping completed successfully! 🚀")
print(f"Total Pages Processed: {len(saved_data)}")
print(f"Data saved to: {output_path}")
