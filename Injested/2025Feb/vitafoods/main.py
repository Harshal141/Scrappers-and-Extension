import time
import logging
import os
import json
from bs4 import BeautifulSoup
from CloudflareBypasser import CloudflareBypasser
from DrissionPage import ChromiumPage, ChromiumOptions

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('cloudflare_bypass.log', mode='w')
    ]
)

def get_chromium_options(browser_path: str, arguments: list) -> ChromiumOptions:
    """
    Configures and returns Chromium options.
    """
    options = ChromiumOptions().auto_port()
    options.set_paths(browser_path=browser_path)
    for argument in arguments:
        options.set_argument(argument)
    return options

def save_data_incrementally(data, file_name='companies.json'):
    """
    Saves data incrementally to the JSON file.
    """
    # Check if the file already exists
    if os.path.exists(file_name):
        # Load existing data
        with open(file_name, 'r') as json_file:
            existing_data = json.load(json_file)
    else:
        existing_data = []

    # Append new data
    existing_data.append(data)

    # Save the updated data
    with open(file_name, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)
        logging.info('Data saved incrementally to companies.json')

def main():
    # Chromium Browser Path
    isHeadless = os.getenv('HEADLESS', 'false').lower() == 'true'
    
    if isHeadless:
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(1920, 1080))
        display.start()

    browser_path = os.getenv('CHROME_PATH', "/usr/bin/google-chrome")
    
    # Arguments to make the browser better for automation and less detectable.
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
    driver = ChromiumPage(addr_or_opts=options)
    
    website = "https://exhibitors.vitafoods.eu.com/vfe24/"
    
    try:
        logging.info('Navigating to the page.')
        driver.get(website)
        logging.info('Page loaded successfully.')
        logging.info('Attempting to bypass Cloudflare.')
        cf = CloudflareBypasser(driver)
        cf.bypass()
        logging.info('Cloudflare bypassed.')
        logging.info(f"Website Title: {driver.title}")
        
        # Click "Show more results" until no more results
        show_more_button = driver.ele('text=Show more results')
        counter = 0
        for i in range(0,34):
            show_more_button.click()
            time.sleep(1)
        
        logging.info('Extracting data from the page.')
        # Loop through the IDs from 10000 to 8900
        for i in range(10000, 8900, -1):
            target_id = f"result{i}"
            logging.info(f"Looking for ID: {target_id}")
            
            try:
                # Check if the element with the target ID exists
                target_element = driver.ele(f'#{target_id}')
                if target_element:
                    logging.info(f"Element found: {target_id}")
                    
                    # Parse the content using BeautifulSoup
                    html_content = target_element.html
                    soup = BeautifulSoup(html_content, 'html.parser')
                    
                    # Extract Company Name
                    name_tag = soup.find('h4')
                    company_name = name_tag.get_text(strip=True) if name_tag else 'N/A'
                    
                    # Extract Company Location
                    location_tag = soup.find('span', class_='country')
                    company_location = location_tag.get_text(strip=True) if location_tag else 'N/A'
                    
                    # Extract Company URL
                    additional_tag = soup.find('div', class_='additional')
                    url_tag = additional_tag.find('a', class_='button button-secondary exhibitorlist-profilelink') if additional_tag else None
                    company_url = url_tag.get('href') if url_tag else 'N/A'
                    
                    logging.info(f"Extracted Name: {company_name}")
                    logging.info(f"Extracted Location: {company_location}")
                    logging.info(f"Extracted URL: {company_url}")
                    
                    # Save incrementally
                    data = {
                        "name": company_name,
                        "location": company_location,
                        "domain": company_url
                    }
                    save_data_incrementally(data)
                    
                else:
                    logging.info(f"No element found with ID: {target_id}")

            except Exception as e:
                logging.error(f"Error processing ID {target_id}: {str(e)}")

        time.sleep(5)
        
    except Exception as e:
        logging.error(f'Error navigating to the page: {e}')
    finally:
        logging.info('Closing the browser.')
        driver.quit()
        if isHeadless:
            display.stop()

if __name__ == '__main__':
    main()
