import time
import logging
import os
import json
import math
from urllib.parse import urlparse, parse_qs, unquote
from service.CloudflareBypasser import CloudflareBypasser
from DrissionPage import ChromiumPage, ChromiumOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('final_job.log', mode='w')
    ]
)

def get_chromium_options(browser_path: str, arguments: list) -> ChromiumOptions:
    """
    Configures and returns Chromium options.
    
    :param browser_path: Path to the Chromium browser executable.
    :param arguments: List of arguments for the Chromium browser.
    :return: Configured ChromiumOptions instance.
    """
    options = ChromiumOptions().auto_port()
    options.set_paths(browser_path=browser_path)
    for argument in arguments:
        options.set_argument(argument)
    return options

def extract_suppliers(driver):
    """
    Extracts supplier data from the current page.
    Returns a list of dictionaries with keys:
      - supplier_name
      - supplier_website
    """
    suppliers = []
    # Locate all supplier result divs.
    supplier_divs = driver.eles("css:div.supplier-result")
    
    for div in supplier_divs:
        try:
            # Extract supplier name from the anchor inside .supplier-info .name
            name_elem = div.ele("css:.supplier-info .name .name-link")
            supplier_name = name_elem.text.strip() if name_elem else ""
            supplier_HeadQuarter = div.ele("css:.supplier-info .name p.headquarters").text.strip() if div.ele("css:.supplier-info .name p.headquarters") else ""

            # Find the supplier website by looking for a link with "website" in its text within .supplier-result-buttons
            website_url = None
            btn_links = div.eles("css:.supplier-result-buttons a")
            for link in btn_links: 
                if "website" in link.text.lower():
                    raw_url = link.link
                    # Parse the URL to extract the gotourl parameter if present.
                    parsed = urlparse(raw_url)
                    qs = parse_qs(parsed.query)
                    target_url = qs.get("gotourl", [None])[0]
                    if target_url:
                        website_url = unquote(target_url)
                    else:
                        website_url = raw_url
                    break

            if supplier_name and website_url:
                suppliers.append({
                    "supplier_name": supplier_name,
                    "supplier_website": website_url,
                    "supplier_HeadQuarter": supplier_HeadQuarter
                })
        except Exception as e:
            logging.error("Error extracting supplier info: %s", e)
    return suppliers

def write_backup(data, output_file="suppliers_output.json"):
    """
    Writes the current backup of supplier data to a JSON file.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    logging.info("Backup written to %s (total %d supplier(s))", output_file, len(data))

def main():
    # Determine if running headless
    isHeadless = os.getenv('HEADLESS', 'false').lower() == 'true'
    if isHeadless:
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(1920, 1080))
        display.start()
    
    # Set browser executable path (adjust for your OS)
    browser_path = os.getenv('CHROME_PATH', "/usr/bin/google-chrome")
    # For Windows, you might use:
    # browser_path = os.getenv('CHROME_PATH', r"C:/Program Files/Google/Chrome/Application/chrome.exe")
    
    # Browser arguments for stealth and automation
    arguments = [
        "-no-first-run",
        "-force-color-profile=srgb",
        "-metrics-recording-only",
        "-password-store=basic",
        "-use-mock-keychain",
        "-export-tagged-pdf",
        "-no-default-browser-check",
        "-disable-background-mode",
        "-enable-features=NetworkService,NetworkServiceInProcess,LoadCryptoTokenExtension,PermuteTLSExtensions",
        "-disable-features=FlashDeprecationWarning,EnablePasswordsAccountStorage",
        "-deny-permission-prompts",
        "-disable-gpu",
        "-accept-lang=en-US",
    ]
    
    options = get_chromium_options(browser_path, arguments)
    
    # Initialize the browser using DrissionPage.
    driver = ChromiumPage(addr_or_opts=options)
    
    try:
        # *** Perform the Login First ***
        login_website = "https://www.globalspec.com/MyGlobalSpec/Login"
        logging.info("Navigating to login page: %s", login_website)
        driver.get(login_website)
        
        # Bypass Cloudflare challenge on the login page.
        cf_bypasser = CloudflareBypasser(driver)
        cf_bypasser.bypass()
        time.sleep(5)
        
        # Fill in login form
        email_input = driver.ele("css:form[name='relogin'] input[name='email']")
        logging.info("Email input found: %s", email_input)
        email_input.click()
        email_input.input("herculeswarrior.in@gmail.com")
        time.sleep(4)
        
        password_input = driver.ele("css:form[name='relogin'] input[name='password']")
        logging.info("Password input found: %s", password_input)
        password_input.input("$M1kw$li")
        time.sleep(4)
        
        # Click login button
        login_button = driver.ele("css:form[name='relogin'] input[type='submit']")
        logging.info("Login button found: %s", login_button)
        login_button.click()
        time.sleep(10)  # Wait for login to process
        
        logging.info("Login successful. Current page title: %s", driver.title)
        
        # Now process category pages from output.json
        input_file = "output.json"
        with open(input_file, "r", encoding="utf-8") as f:
            categories = json.load(f)
        
        all_supplier_data = []
        for cat in categories:
            cat_href = cat.get("href")
            cat_text = cat.get("text")
            num_suppliers_str = cat.get("num_suppliers", "0")
            try:
                num_suppliers = int(num_suppliers_str.replace(",", ""))
            except Exception:
                num_suppliers = 0
            
            if not cat_href or num_suppliers == 0:
                logging.warning("Skipping category '%s' due to missing URL or supplier count.", cat_text)
                continue
            
            # Calculate total pages (15 suppliers per page)
            total_pages = math.ceil(num_suppliers / 15)
            logging.info("Category '%s': %d suppliers → %d page(s).", cat_text, num_suppliers, total_pages)
            
            # Iterate through each page for this category.
            for pg in range(1, total_pages + 1):
                page_url = f"{cat_href}?pg={pg}"
                logging.info("Loading page %d: %s", pg, page_url)
                driver.get(page_url)
                time.sleep(4)  # Allow page to load
                
                # Bypass Cloudflare if needed.
                cf_bypasser = CloudflareBypasser(driver)
                cf_bypasser.bypass()
                
                logging.info("Page title: %s", driver.title)
                
                # Extract supplier data from the current page.
                suppliers = extract_suppliers(driver)
                logging.info("Found %d supplier(s) on page %d.", len(suppliers), pg)
                for s in suppliers:
                    s["category"] = cat_text
                    s["page"] = pg
                all_supplier_data.extend(suppliers)
                
                # Write backup after processing each page.
                write_backup(all_supplier_data)
        
        logging.info("Final backup complete. Total supplier(s) extracted: %d", len(all_supplier_data))
    
    except Exception as e:
        logging.error("An error occurred: %s", e)
    
    finally:
        logging.info("Closing the browser.")
        driver.quit()
        if isHeadless:
            display.stop()

if __name__ == '__main__':
    main()
