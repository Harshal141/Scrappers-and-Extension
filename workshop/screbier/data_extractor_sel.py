import os
import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome in headless mode
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
options.add_argument("--window-size=1920,3000")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Your target product page
url = "https://www.schreiberfoodsproducts.com/products/schreiber-sharp-cheddar-loaf-2-5/"
driver.get(url)
time.sleep(2)  # Give time for content to load

# Prepare output folder
output_folder = "product_output"
os.makedirs(output_folder, exist_ok=True)

product_data = {}

# 🧠 Extract name and description
name = driver.find_element(By.CSS_SELECTOR, ".entry-header h1").text.strip()
desc = driver.find_element(By.CSS_SELECTOR, ".product__header-info p").text.strip()
product_data["name"] = name
product_data["description"] = desc

# 📦 Extract Product Specs
specs = {}
tables = driver.find_elements(By.CSS_SELECTOR, ".product__specs-table")
for table in tables:
    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) == 2:
            key = cells[0].text.strip().replace(":", "")
            value = cells[1].text.strip()
            if key:
                specs[key] = value
product_data["product_specs"] = specs

# 🧾 Extract Ingredients (from accordion)
accordion_buttons = driver.find_elements(By.CSS_SELECTOR, ".accordion h2 button")
accordion_divs = driver.find_elements(By.CSS_SELECTOR, ".accordion > div")

for i, btn in enumerate(accordion_buttons):
    if "Ingredients" in btn.text:
        ingredients = accordion_divs[i].text.strip()
        product_data["ingredients"] = ingredients
        break

# 🖼️ Capture Nutrition section as image
try:
    nutrition = driver.find_element(By.CSS_SELECTOR, ".nutrition__wrapper")
    nutrition_img_path = os.path.join(output_folder, "nutrition_facts.png")
    nutrition.screenshot(nutrition_img_path)
    product_data["nutrition_image"] = nutrition_img_path
except Exception as e:
    product_data["nutrition_image"] = None
    print("⚠️ Nutrition section not found:", e)

# 💾 Save as JSON
with open(os.path.join(output_folder, "product_data.json"), "w", encoding="utf-8") as f:
    json.dump(product_data, f, indent=2, ensure_ascii=False)

driver.quit()

print("✅ Done! Data saved to product_output/")
