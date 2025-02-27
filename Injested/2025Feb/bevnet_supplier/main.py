import time
import logging
import os
import json
from bs4 import BeautifulSoup
from CloudlfareBypasser import CloudflareBypasser
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
    
    :param browser_path: Path to the Chromium browser executable.
    :param arguments: List of arguments for the Chromium browser.
    :return: Configured ChromiumOptions instance.
    """
    options = ChromiumOptions().auto_port()
    options.set_paths(browser_path=browser_path)
    for argument in arguments:
        options.set_argument(argument)
    return options

def extract_links_from_json(file_path):
    """
    Extracts URLs from the JSON file.
    
    :param file_path: Path to the JSON file.
    :return: List of URLs.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
        categories = data.get("FoodMaster", {}).get("Categories", [])
        urls = [category["URL"] for category in categories]
        return urls

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
    
    website= "https://www.bevnet.com/supplierfinder/suppliers-ingredients"
    
    try:
        logging.info('Navigating to the page.')
        driver.get(website)
        logging.info('Page loaded successfully.')
        logging.info('Attempting to bypass Cloudflare.')
        cf = CloudflareBypasser(driver)
        cf.bypass()
        logging.info('Cloudflare bypassed.')
        logging.info("Enjoy the content of the website" , driver.title)
        time.sleep(5)
        html_content = driver.html
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        content_tables = soup.find_all('table', class_='table-listings')
        data = []
        seen_url = set()
        for content_table in content_tables:
            domain_contents = content_table.find_all('a' ,class_='accented')
            for domain_content in domain_contents:
                domain_name = domain_content.text
                domain_url = domain_content['href']
                full_domain_url = f'https://www.bevnet.com{domain_url}'
                if full_domain_url in seen_url:
                    continue
                seen_url.add(full_domain_url)
                data.append({
                    "name": domain_name,
                    "url": full_domain_url
                })
        
        
        output_file = 'bevnet_supplier.json'
        
        with open(output_file,'w') as f:
            json.dump(data, f, indent=4)
            logging.info(f'Data extracted and saved to {output_file}')
            
        
        
    except Exception as e:
        logging.error(f'Error navigating to the page: {e}')
    finally:
        logging.info('Closing the browser.')
        driver.quit()
        

    

if __name__ == '__main__':
    main()
