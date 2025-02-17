import time
import logging
import os
import json
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
    
    :param browser_path: Path to the Chromium browser executable.
    :param arguments: List of arguments for the Chromium browser.
    :return: Configured ChromiumOptions instance.
    """
    options = ChromiumOptions().auto_port()
    options.set_paths(browser_path=browser_path)
    for argument in arguments:
        options.set_argument(argument)
    return options

def main():
    # Chromium Browser Path
    isHeadless = os.getenv('HEADLESS', 'false').lower() == 'true'
    
    if isHeadless:
        from pyvirtualdisplay import Display

        display = Display(visible=0, size=(1920, 1080))
        display.start()

    browser_path = os.getenv('CHROME_PATH', "/usr/bin/google-chrome")
    
    # Windows Example
    # browser_path = os.getenv('CHROME_PATH', r"C:/Program Files/Google/Chrome/Application/chrome.exe")

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

    # Initialize the browser
    driver = ChromiumPage(addr_or_opts=options)
    website="https://www.globalspec.com/productfinder/material_handling_packaging"
    login_website="https://www.globalspec.com/MyGlobalSpec/Login"
    try:
        logging.info('Navigating to the demo page.')
        driver.get(login_website)

        # Where the bypass starts
        logging.info('Starting Cloudflare bypass.')
        cf_bypasser = CloudflareBypasser(driver)


        cf_bypasser.bypass()

        logging.info("Enjoy the content!")
        logging.info("Title of the page: %s", driver.title)
        
         # Fill in the login form
        email_input = driver.ele("css:form[name='relogin'] input[name='email']")
        logging.info("Email input found: %s", email_input)
        email_input.click()
        email_input.input("herculeswarrior.in@gmail.com")
        time.sleep(4)
        
        password_input = driver.ele("css:form[name='relogin'] input[name='password']")
        logging.info("Password input found: %s", password_input)
        password_input.input("$M1kw$li")
        time.sleep(4)
        
        # Select the login button based on the HTML snippet (an input element of type submit)
        login_button = driver.ele("css:form[name='relogin'] input[type='submit']")
        login_button.click()

        # Sleep for a while to let the user see the result if needed
        time.sleep(10)
        
        driver.get(website)
        
        h2_elements = driver.eles("css:#browse-categories h2")
        data = []
        
        for h2 in h2_elements:
            try:
                a_element = h2.ele("tag:a")
                href = a_element.link
                text = a_element.text
                logging.info("Extracted data: %s - %s", text, href)
                
                span_element = h2.ele("tag:span")
                suppliers_text = span_element.text.strip()
                
                logging.info("Number of suppliers: %s", suppliers_text)
                
                num_suppliers = suppliers_text.strip("()").split()[0]
                data.append({
                    "href": href,
                    "text": text,
                    "num_suppliers": num_suppliers
                })
            except Exception as e:
                logging.error("An error occurred: %s", str(e))
        
        # Write the results to a JSON file
        output_file = "output.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        logging.info("Extracted %d item from and saved to output.json", len(data), output_file)
        
        
        time.sleep(10)
    except Exception as e:
        logging.error("An error occurred: %s", str(e))
    finally:
        logging.info('Closing the browser.')
        driver.quit()
        if isHeadless:
            display.stop()

if __name__ == '__main__':
    main()