import logging
import os
import json
import time
from bs4 import BeautifulSoup
from CloudflareBypasser import CloudflareBypasser
from DrissionPage import ChromiumPage, ChromiumOptions

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('extract_data.log', mode='w')
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

def extract_urls_from_json(file_path):
    """
    Extracts URLs from the JSON file.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
        urls = [item["url"] for item in data]
        return urls

def extract_data_from_html(html):
    """
    Extracts the required data (Name and Domain) from the HTML content.
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Initialize the data dictionary
    data = {
        "name": None,
        "domain": None
    }

    # Find all the text-secondary elements (labels)
    labels = soup.find_all('div', class_='text-secondary')

    # Loop through the labels to find the corresponding values
    for label in labels:
        label_text = label.get_text(strip=True)

        if "Name" in label_text:
            name_value = label.find_next('div', class_='profileResponse')
            if name_value:
                data["name"] = name_value.get_text(strip=True)

        elif "Website" in label_text:
            website_value = label.find_next('a')
            if website_value:
                data["domain"] = website_value.get('href')

    return data

def save_data_immediately(data, output_file):
    """
    Saves each entry immediately to avoid data loss.
    """
    if data:
        # Load existing data
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        else:
            existing_data = []

        # Append the new data
        existing_data.append(data)

        # Save updated data
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4)

        logging.info(f"Saved data: {data}")

def main():
    # Chromium Browser Path
    isHeadless = os.getenv('HEADLESS', 'false').lower() == 'true'
    
    if isHeadless:
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(1920, 1080))
        display.start()

    browser_path = os.getenv('CHROME_PATH', "/usr/bin/google-chrome")
    
    # Arguments for Chromium
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
    
    # Load URLs from JSON
    json_file_path = 'output.json'  
    urls = extract_urls_from_json(json_file_path)

    # Output file
    output_file = 'extracted_name_domain.json'

    try:
        driver = ChromiumPage(addr_or_opts=options)
        
        for url in urls:
            try:
                logging.info(f"Opening URL: {url}")
                driver.get(url)
                time.sleep(3)  # Wait for the page to load
                
                # Attempt Cloudflare bypass
                logging.info('Attempting Cloudflare bypass.')
                cf_bypasser = CloudflareBypasser(driver)
                cf_bypasser.bypass()
                logging.info('Cloudflare bypassed successfully.')

                # Extract data from the page
                html = driver.html
                extracted_data = extract_data_from_html(html)
                logging.info(f"Extracted Data: {extracted_data}")
                
                # Save immediately to avoid data loss
                save_data_immediately(extracted_data, output_file)

            except Exception as e:
                logging.error(f"Error while processing URL {url}: {str(e)}")

    except Exception as e:
        logging.error(f"Critical error: {str(e)}")

    finally:
        logging.info('Closing the browser.')
        driver.quit()
        if isHeadless:
            display.stop()

if __name__ == '__main__':
    main()
