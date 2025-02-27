import logging
import os
import json
from bs4 import BeautifulSoup
from CloudlfareBypasser import CloudflareBypasser
from DrissionPage import ChromiumPage, ChromiumOptions
import time

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

def extract_urls_from_json(file_path):
    """
    Extracts URLs from the JSON file.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
        urls = [item["url"] for item in data]
        return urls

def save_data_to_file(data, output_file):
    """
    Saves the data to a JSON file and clears the in-memory list.
    """
    if data:
        with open(output_file, 'a', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        logging.info(f"Saved {len(data)} entries to {output_file}")
        data.clear()

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
    json_file_path = 'bevnet_supplier.json'  
    urls = extract_urls_from_json(json_file_path)

    # Output file
    output_file = 'total_bevnet.json'
    data = []

    try:
        # Initialize Browser Session
        driver = ChromiumPage(addr_or_opts=options)

        # Iterate through URLs
        for url in urls:
            try:
                logging.info(f"Opening URL: {url}")
                driver.get(url)
                time.sleep(5)
                
                # Cloudflare Bypass
                logging.info('Attempting Cloudflare bypass.')
                cf_bypasser = CloudflareBypasser(driver)
                cf_bypasser.bypass()
                logging.info('Cloudflare bypassed successfully.')

                # Parse HTML Content
                soup = BeautifulSoup(driver.html, 'html.parser')
                
                main_contents = soup.find('aside', class_="jobs-aside")
                if main_contents:
                    logging.info('Main contents found.')
                    company_name_tag = main_contents.find("strong", text="Company Name:")
                    company_name = company_name_tag.find_next_sibling(text=True).strip() if company_name_tag else None
                    company_website = main_contents.find('a')["href"]
                    
                    data.append({
                        "name": company_name,
                        "domain": company_website
                    })

                    # Write data in batches of 10
                    if len(data) >= 10:
                        save_data_to_file(data, output_file)
                
                else:
                    logging.warning('Main contents not found.')

            except Exception as e:
                logging.error(f"An error occurred while processing {url}: {str(e)}")

        # Final save for any remaining data
        save_data_to_file(data, output_file)

    except Exception as e:
        logging.error(f"Critical error: {str(e)}")

    finally:
        logging.info('Closing the browser.')
        driver.quit()
        if isHeadless:
            display.stop()

if __name__ == '__main__':
    main()
