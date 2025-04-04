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

def save_data_incrementally(data, file_name='companies.json'):
    """
    Saves data incrementally to the JSON file.
    
    :param data: A dictionary containing the company name and domain.
    :param file_name: The name of the JSON file.
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
    
    website= "https://www.nombase.com/companies?categorySlugs=flavors-ingredients,product-development,branding-packaging,co-packer-co-manufacturer&sortBy=RecentlyAdded"
    
    try:
        logging.info('Navigating to the page.')
        driver.get(website)
        logging.info('Page loaded successfully.')
        logging.info('Attempting to bypass Cloudflare.')
        cf = CloudflareBypasser(driver)
        cf.bypass()
        logging.info('Cloudflare bypassed.')
        logging.info("Enjoy the content of the website" , driver.title)
        logging.info('Looking for "View More Button" button.')
        max_clicks = 100
        clicks = 0
        while clicks < max_clicks:
            see_more_button = driver.ele('@class:btn btn--secondary')

            if see_more_button:
                see_more_button.click()
                clicks += 1
                logging.info(f'"View More" button clicked ({clicks})')
            else:
                logging.info('"View More" button not found or no longer visible.')
                break

        html_content = driver.html
        soup = BeautifulSoup(html_content, 'html.parser')

        articles = soup.find_all("article", class_="search-list-item")
        logging.info(f"Found {len(articles)} company entries.")

        for article in articles:
            link_tag = article.find("a", class_="search-list-item-image")
            name_tag = article.find("span")

            if link_tag and link_tag.get("href") and name_tag:
                relative_url = link_tag["href"]
                full_url = "https://www.nombase.com" + relative_url
                company_name = name_tag.get_text(strip=True)

                save_data_incrementally({
                    "name": company_name,
                    "website": full_url
                })
        
    except Exception as e:
        logging.error(f'Error navigating to the page: {e}')
    finally:
        logging.info('Closing the browser.')
        driver.quit()

if __name__ == '__main__':
    main()
