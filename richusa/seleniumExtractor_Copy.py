from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import json

with open('./richusa/parsed_data_2.json', 'r') as file:
    products = json.load(file)

count = 600

# Open the CSV file for writing
with open('product_images_1.csv', 'a', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['id', 'heroimage', 'imagesextracted']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()  # Write the header row

    # Loop through each product
    for product in products:
        print(f"Extracting images for product ID: {product['id']}")
        print(f"Product {count}")
        count += 1
        driver = webdriver.Chrome()

        product_url = "https://www.richsusa.com/products///" + product["id"] + '/'  
        driver.get(product_url)

        time.sleep(4)

        divs = driver.find_elements(By.CSS_SELECTOR, "div.item.image")
        image_sources = []
        for div in divs:
            img = div.find_element(By.TAG_NAME, "img")  # Find the img tag inside the div
            image_sources.append(img.get_attribute("src"))  # Add the src attribute to the list

        writer.writerow({
            'id': product["id"],
            'heroimage': product["imageurl"],
            'imagesextracted': " | ".join(image_sources)  # Join extracted image URLs with a delimiter
        })

        driver.quit()  # Close the browser window

print("CSV file has been created with the images.")
