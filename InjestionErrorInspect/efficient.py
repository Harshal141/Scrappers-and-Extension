import pandas as pd
import time
import logging
import os
from DrissionPage import ChromiumPage, ChromiumOptions
from CloudflareBypasser import CloudflareBypasser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('domain_check.log', mode='w')
    ]
)

def get_chromium_options(browser_path: str, arguments: list) -> ChromiumOptions:
    options = ChromiumOptions().auto_port()
    options.set_paths(browser_path=browser_path)
    for argument in arguments:
        options.set_argument(argument)
    return options

def check_domains(driver, rows, results, batch_size=10, output_file="domain_status_output.csv", concurrent_tabs=4):
    tabs = [driver.new_tab() for _ in range(concurrent_tabs)]
    idx = 0
    total = len(rows)

    while idx < total:
        for tab in tabs:
            if idx >= total:
                break

            row = rows[idx]
            domain_id = row.get("id")
            name = row.get("name")
            domain = row.get("domain")

            if pd.isna(domain):
                idx += 1
                continue

            url = f"https://{domain.strip()}"
            result = {
                "id": domain_id,
                "name": name,
                "domain": domain,
                "status": "no",
                "title": ""
            }

            try:
                tab.get(url)
                cf_bypasser = CloudflareBypasser(tab)
                cf_bypasser.bypass()

                body_text = tab('tag:body').text
                if tab.title and body_text and len(body_text.strip()) > 100:
                    result["status"] = "yes"
                    result["title"] = tab.title.strip()
                else:
                    result["reason"] = "Empty or low-content body"
            except Exception as e:
                result["error"] = str(e)
            finally:
                results.append(result)
                logging.info("[%d] %s - %s", idx + 1, domain, result["status"])
                idx += 1

        if len(results) >= batch_size:
            write_batch(results, output_file)
            results.clear()

    for tab in tabs:
        tab.close()

def write_batch(data, output_file="domain_status_output.csv"):
    df = pd.DataFrame(data)
    file_exists = os.path.isfile(output_file)
    df.to_csv(output_file, mode='a', header=not file_exists, index=False)

def main():
    input_file = "home-page-scrapping-error-domains.csv"  
    df = pd.read_csv(input_file)

    browser_path = os.getenv('CHROME_PATH', "/usr/bin/google-chrome")
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

    try:
        results = []
        check_domains(driver, df.to_dict(orient='records'), results)
        if results:
            write_batch(results)
    finally:
        logging.info("Closing the browser.")
        driver.quit()

if __name__ == '__main__':
    main()