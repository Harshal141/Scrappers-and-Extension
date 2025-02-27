import logging
import os
import json
from bs4 import BeautifulSoup
from CloudflareBypass import CloudflareBypasser
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
        urls = [item["website"] for item in data]
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
    json_file_path = 'companies.json'  
    urls = extract_urls_from_json(json_file_path)

    # Output file
    output_file = 'total_ift.json'
    data = []

    try:
        
        driver = ChromiumPage(addr_or_opts=options)
        
        driver.get("https://ift25.mapyourshow.com/8_0/explore/exhibitor-gallery.cfm?featured=false")
        
        time.sleep(2)

        data=[]
        for url in urls:
            try:
                logging.info(f"Opening URL: {url}")
                driver.get(url)
                time.sleep(2)
                
                
                logging.info('Attempting Cloudflare bypass.')
                cf_bypasser = CloudflareBypasser(driver)
                cf_bypasser.bypass()
                logging.info('Cloudflare bypassed successfully.')

                # Parse HTML Content
                soup = BeautifulSoup(driver.html, 'html.parser')
                
                company_name = soup.find('h1', class_="exhibitor-name").text
                logging.info(f"Company Name: {company_name}")
                company_url = soup.select_one('.column.contact-info ul.list__icons.f4 a')['href']
                logging.info(f"Company URL: {company_url}")
                address_block = soup.select_one('address.column.address.dynamicColumnBorder')
                if address_block:
                    address_lines = [p.get_text(strip=True) for p in address_block.find_all('p')]
                    full_address = ", ".join(address_lines)
                    logging.info(f"Company Address: {full_address}")
                else:
                    print("No address found.")
                
                data.append({
                    "name": company_name,
                    "domain": company_url,
                    "address": full_address
                })
                
                save_data_to_file(data, output_file)
                

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
