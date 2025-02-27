# import csv
# import json
# from utility import jsonIndexer

# # input_file = './FnBScanner/DATA_267_afpa.csv'
# output_file = './FnBScanner/DATA_267_afpa.json'
# output_2 = './FnBScanner/DATA_267_afpa_indexed.json'

# jsonIndexer(output_file, output_2)
# data = []
# with open(input_file, mode='r',encoding="ISO-8859-1") as f:
#     csv_reader = csv.DictReader(f)
#     for row in csv_reader:
#         data.append(row)

# with open(output_file, 'w', encoding="utf-8") as f:
#     json.dump(data, f, indent=4)

# print('CSV to JSON conversion completed successfully.')

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
import json
from webdriver_manager.chrome import ChromeDriverManager

# Setup headless browser
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Get cookies using Selenium
def get_cookies(driver, url):
    driver.get(url)
    driver.implicitly_wait(5)  # Wait for page load and scripts
    cookies = driver.get_cookies()
    return {cookie['name']: cookie['value'] for cookie in cookies}

# Perform GraphQL request with cookies
def graphql_request(cookies):
    headers = {
        'content-type': 'application/json',
        'origin': 'https://newhope.app.swapcard.com',
        'referer': 'https://newhope.app.swapcard.com/',
    }

    payload = [
        {
            "operationName": "FeaturesQuery",
            "variables": {"code": "EXHIBITOR_CHAT", "withEvent": True, "eventId": "RXZlbnRfMTg2NDYzMQ=="},
            "extensions": {"persistedQuery": {"version": 1, "sha256Hash": "babb0861eba347dce93cb1d99b672f84188803649cd9d9e86262fe772dcd37fd"}},
        },
        {
            "operationName": "EventExhibitorDetailsViewQuery",
            "variables": {"withEvent": True, "skipMeetings": True, "exhibitorId": "RXhoaWJpdG9yXzE3MDgyNzk=", "eventId": "RXZlbnRfMTg2NDYzMQ=="},
            "extensions": {"persistedQuery": {"version": 1, "sha256Hash": "f9a01985a3222c9c7b98da9e6fa72422d06016251a48cee9f0849c5539fc4d3e"}},
        }
    ]

    response = requests.post(
        'https://newhope.app.swapcard.com/api/graphql',
        headers=headers,
        cookies=cookies,
        json=payload
    )

    if response.ok:
        print("[✅] Success:", response.json())
    else:
        print("[❌] Failed:", response.status_code, response.text)

driver = setup_driver()
cookies = get_cookies(driver, "https://newhope.app.swapcard.com/")
driver.quit()

graphql_request(cookies)

