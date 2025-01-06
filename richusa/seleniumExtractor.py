from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import json

# Load JSON data
with open('./richusa/parsed_data_indexed.json', 'r') as file:
    products = json.load(file)

startIndex = 1
endIndex = 10

# Open the CSV file for writing
with open('product_images_indexed_sol.csv', 'a', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['index', 'id', 'heroimage', 'imagesextracted']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    driver = webdriver.Chrome()
    try:
        for product in products:
            if startIndex <= product['index'] <= endIndex:
                print(f"Extracting images for product ID: {product['id']} (Index: {product['index']})")

                # Build the product URL
                product_url = f"https://www.richsusa.com/products///{product['id']}/"  
                driver.get(product_url)

                # Wait for the page to load
                time.sleep(2)

                # Extract image sources
                divs = driver.find_elements(By.CSS_SELECTOR, "div.item.image")
                image_sources = []
                for div in divs:
                    img = div.find_element(By.TAG_NAME, "img")
                    image_sources.append(img.get_attribute("src"))

                # Write data to the CSV
                writer.writerow({
                    'index': product["index"],
                    'id': product["id"],
                    'heroimage': product["imageurl"],
                    'imagesextracted': " | ".join(image_sources)
                })

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the WebDriver
        driver.quit()

print("CSV file has been created with the selected range of products.")
