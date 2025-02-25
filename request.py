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
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://icanhazip.com")  # Displays the public IP
ip_address = driver.find_element("tag name", "body").text.strip()
print(f"My IP address from Selenium: {ip_address}")

driver.quit()
