import time
import logging
import os
import json
from bs4 import BeautifulSoup
from CloudflareBypass import CloudflareBypasser
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

    # Load URLs from JSON
    json_file_path = 'food_master_urls.json'  # Place the JSON file in the same directory
    urls = extract_links_from_json(json_file_path)

    all_data = {
        "sponsored_listings": [],
        "listing_summaries": []
    }

    # Loop through each URL and display the parsed HTML
    for url in urls:
        try:
            # Initialize the browser for Cloudflare Bypass
            driver = ChromiumPage(addr_or_opts=options)
            driver.get(url)

            # Cloudflare Bypass
            logging.info('Starting Cloudflare bypass.')
            cf_bypasser = CloudflareBypasser(driver)
            cf_bypasser.bypass()

            # Get the page source after Cloudflare bypass
            page_source = driver.html
            soup = BeautifulSoup(page_source, 'html.parser')

            # Extract data from sponsored listings
            sponsored_listings = soup.find_all("article", class_="sponsored-listing")
            sponsored_data = []

            for sponsored_listing in sponsored_listings:
                try:
                    company_name = sponsored_listing.find("h1", class_="sponsored-listing__company-name").text.strip()
                    company_domain = sponsored_listing.find("a", class_="sponsored-listing__url")['href'].strip()
                    city = sponsored_listing.find("div", class_="sponsored-listing__city").text.strip()
                    state = sponsored_listing.find("div", class_="premium-listing__state-province").text.strip()
                    location = f"{city}, {state}"

                    sponsored_data.append({
                        "company_name": company_name,
                        "company_domain": company_domain,
                        "location": location
                    })
                except Exception as e:
                    logging.error(f"Error processing sponsored listing: {str(e)}")

            # Extract data from listing summaries
            listing_summaries = soup.find_all('article', class_='listing-summary')
            summary_data = []

            for summary in listing_summaries:
                try:
                    company_name_tag = summary.find('h1', class_='listing-summary__company-name')
                    company_name = company_name_tag.get_text(strip=True) if company_name_tag else "N/A"

                    domain_tag = summary.find('a', class_='listing-summary__url')
                    domain = domain_tag.get_text(strip=True) if domain_tag else "N/A"

                    city = summary.find('div', class_='listing-summary__city')
                    state = summary.find('div', class_='premium-listing__state-province')
                    location = f"{city.get_text(strip=True)}, {state.get_text(strip=True)}" if city and state else "N/A"

                    summary_data.append({
                        "company_name": company_name,
                        "company_domain": domain,
                        "location": location
                    })
                except Exception as e:
                    logging.error(f"Error processing listing summary: {str(e)}")

            # Store collected data
            all_data["sponsored_listings"].extend(sponsored_data)
            all_data["listing_summaries"].extend(summary_data)

            # Write the results to a JSON file after processing each URL
            output_file = "output.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(all_data, f, indent=4)
            logging.info(f"Extracted data saved to {output_file}")

        except Exception as e:
            logging.error("An error occurred: %s", str(e))
        finally:
            logging.info('Closing the browser.')
            driver.quit()
            if isHeadless:
                display.stop()

if __name__ == '__main__':
    main()
