import os
import csv
import time
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# List of product URLs
urls = [
  "schreiber-white-pasteurized-process-cheese-product-slices-4-5-120-slices/",
  "schreiber-sharp-cheddar-loaf-2-5/",
  "sharp-cheddar-white-feather-shreds-4-5/",
  "strawberry-cream-cheese-spread-bulk-1-30/",
  "yellow-pasteurized-process-cheese-spread-pouch-6-5/",
  "schreiber-cheddar-jack-50-50-feather-shreds-4-5/",
  "schreiber-yellow-pasteurized-process-american-slices-4-5-flow-through-wrapper-96-slices/",
  "friendship-lowfat-plain-yogurt-cup-6-2/",
  "schreiber-low-moisture-part-skim-mozzarella-slices-12-1-16-slices/",
  "schreiber-1-milk-12-32-fl-oz/",
  "schreiber-yellow-pasteurized-process-reduced-fat-reduced-sodium-american-slices-4-5-160-slices/",
  "schreiber-colby-jack-50-50-feather-shreds-4-5/",
  "american-heritage-sharp-cheddar-fancy-shreds-12-8oz/",
  "swiss-slices-18-1-32-slices/",
  "american-heritage-monterey-jack-chunk-12-8oz/",
  "raskas-strawberry-cream-cheese-spread-portion-control-cup-100-75oz/",
  "american-heritage-low-moisture-part-skim-mozzarella-chunk-12-8oz/",
  "schreiber-skim-milk-12-32-fl-oz/",
  "havarti-slices-6-1-5-24-slices/",
  "land-o-lakes-lowfat-plain-yogurt-cup-6-2/",
  "schreiber-monterey-jack-fancy-shreds-4-5/",
  "schreiber-1-milk-6-32-fl-oz/",
  "land-o-lakes-lowfat-blended-blueberry-yogurt-tub-4-5/",
  "american-heritage-mexican-style-blend-fancy-shreds-12-8oz/",
  "schreiber-mild-cheddar-slices-12-1-20-slices/",
  "raskas-cream-cheese-spread-portion-control-cup-100-1oz/",
  "schreiber-pasteurized-process-swiss-slices-4-5-160-slices/",
  "yellow-pasteurized-process-sharp-american-slices-6-3-5-210-slices/",
  "schreiber-pasteurized-process-pepper-jack-slices-4-5-120-slices/",
  "schreiber-1-milk-12-32-fl-oz-2/",
  "schreiber-extra-sharp-cheddar-white-loaf-2-5/",
  "cream-cheese-substitute-bulk-1-30/",
  "schreiber-pasteurized-process-swiss-slices-4-5-flow-through-wrapper-120-slices/",
  "cream-cheese-with-carob-bean-gum-bulk-1-30/",
  "land-o-lakes-lowfat-blended-peach-yogurt-cup-6-2/",
  "schreiber-mild-cheddar-snack-cubes-4-5/",
  "schreiber-mild-cheddar-white-feather-shreds-4-5/",
  "schreiber-cream-cheese-loaf-10-3/",
  "land-o-lakes-lowfat-blended-strawberry-yogurt-pail-1-32/",
  "level-valley-creamery-cream-cheese-style-blend-bar-36-8oz/",
  "amera-melt-white-pasteruzied-process-american-block-1-20/",
  "yellow-pasteurized-process-restricted-melt-american-slices-8-5-160-slices/",
  "yellow-pasteurized-process-american-slices-12-12oz-16-slices/",
  "schreiber-amera-melt-white-pasteurized-process-american-loaf-6-5/",
  "schreiber-yellow-pasteurized-process-american-slices-4-5-200-slices/",
  "schreiber-mild-cheddar-loaf-2-5/",
  "schreiber-2-milk-6-32-fl-oz/",
  "schreiber-pasteurized-process-high-flavor-swiss-american-slices-4-5-184-slices/",
  "friendship-lowfat-plain-yogurt-pail-1-35/",
  "schreiber-mild-cheddar-slices-6-1-5-32-slices/",
  "pasteurized-process-monterey-jack-slices-4-5-184-slices/",
  "raskas-neufchatel-loaf-10-3/",
  "five-cheese-pizza-blend-feather-shreds-4-5/",
  "schreiber-yellow-pasteurized-process-american-slices-4-5-184-slices/",
  "whipped-cream-cheese-bulk-1-25/",
  "land-o-lakes-lowfat-blended-strawberry-yogurt-cup-48-4oz/",
  "sharp-cheddar-white-fancy-shreds-4-5/",
  "land-o-lakes-lowfat-blended-blueberry-yogurt-cup-6-2/",
  "swiss-fancy-shreds-4-5/",
  "schreiber-pasteurized-process-hot-pepper-jack-saucing-loaf-6-5/",
  "neufchatel-with-carob-bean-gum-bulk-1-30/",
  "raskas-cream-cheese-bar-12-6-8oz/",
  "schreiber-yellow-pasteurized-process-american-slices-4-5-160-slices/",
  "schreiber-whole-milk-6-32-fl-oz/",
  "land-o-lakes-lowfat-blended-vanilla-yogurt-pail-1-32/",
  "schreiber-premium-swiss-loaf-6-8-9-random-weight/",
  "swiss-slices-18-1-5-36-slices/",
  "pauly-low-moisture-part-skim-mozzarella-loaf-6-5/",
  "schreiber-swiss-snack-cubes-4-5/",
  "schreiber-swiss-slices-8-1-5-32-slices/",
  "land-o-lakes-nonfat-plain-yogurt-cup-6-2/",
  "schreiber-2-milk-12-32-fl-oz/",
  "low-moisture-part-skim-mozzarella-provolone-cheddar-80-10-10-feather-shreds-4-5/",
  "white-pasteurized-process-reduced-sodium-sharp-american-slices-4-5-160-slices/",
  "land-o-lakes-lowfat-blended-strawberry-banana-yogurt-cup-48-4oz/",
  "pauly-colby-mini-longhorn-4-6-random-weight/",
  "whole-milk-plain-yogurt-tub-4-5/",
  "pauly-cream-cheese-bulk-1-30/",
  "whole-milk-mozzarella-provolone-50-50-feather-shreds-4-5/",
  "schreiber-yellow-pasteurized-process-american-cheese-rectangular-feather-cut-shreds-4-5/",
  "land-o-lakes-plain-yogurt-barrel-1-400/",
  "garden-vegetable-cream-cheese-spread-bulk-1-30/",
  "pauly-pepper-jack-loaf-2-5/",
  "schreiber-yellow-pasteurized-process-sharp-american-slices-4-5-200-slices/",
  "provolone-full-moon-slices-18-1-32-slices/",
  "schreiber-monterey-jack-feather-shreds-4-5/",
  "schreiber-reduced-fat-mild-cheddar-feather-shreds-4-5/",
  "level-valley-creamery-cream-cheese-bulk-1-30/",
  "pasteurized-process-extra-hot-pepper-jack-slices-4-5-120-slices/",
  "schreiber-extra-sharp-cheddar-loaf-2-5/",
  "schreiber-white-pasteurized-process-american-slices-4-5-120-slices/",
  "schreiber-provolone-4-inch-slices-12-1-22-slices/",
  "schreiber-yellow-pasteurized-process-american-slices-4-5-flow-through-wrapper-160-slices/",
  "schreiber-yellow-pasteurized-process-cheddar-slices-4-5-160-slices/",
  "schreiber-pasteurized-process-swiss-american-slices-4-5-flow-through-wrapper-120-slices/",
  "schreiber-2-lactose-free-milk-6-32-fl-oz/",
  "american-heritage-yellow-pasteurized-process-american-slices-12-1-24-slices/",
  "yellow-light-pasteurized-process-american-cheese-snack-slices-1-24-2-600-stacks-of-5-slices/",
  "american-heritage-low-moisture-part-skim-mozzarrella-feather-shreds-12-8oz/",
  "schreiber-colby-longhorn-1-14-random-weight/",
  "schreiber-whole-milk-12-32-fl-oz/",
  "schreiber-pasteurized-process-swiss-american-slices-4-5-160-slices/",
  "plain-cream-cheese-spread-bulk-1-30/",
  "schreiber-swiss-slices-12-1-32-slices/",
  "schreiber-colby-jack-longhorn-1-14-random-weight/",
  "mexican-blend-fancy-shreds-4-5/",
  "schreiber-white-pasteurized-process-american-slices-4-5-160-slices/",
  "pauly-colby-jack-loaf-2-5/",
  "american-heritage-sharp-cheddar-chunk-12-8oz/",
  "schreiber-white-pasteurized-process-cheese-product-slices-4-5-160-slices/",
  "pasteurized-process-pepper-jack-cheese-product-restricted-melt-1-4-diced-4-5/",
  "schreiber-skim-milk-6-32-fl-oz/",
  "schreiber-gouda-slices-6-1-5-twin-stack-32-slices/",
  "american-heritage-provolone-slices-8-6oz-shingle-8-slices/",
  "raskas-cream-cheese-spread-6-pack-portion-control-cup-36-1oz/",
  "schreiber-yellow-pasteurized-process-american-slices-4-5-flow-through-wrapper-120-slices/",
  "schreiber-yellow-pasteurized-process-restricted-melt-american-slices-4-5-184-slices/",
  "pauly-cream-cheese-baking-ingredient-bulk-1-30/",
  "pauly-colby-jack-mini-longhorn-2-6-random-weight/",
  "schreiber-mild-cheddar-snack-bar-2-50-75oz/",
  "schreiber-medium-cheddar-loaf-2-5/",
  "raskas-neufchatel-bulk-1-30/",
  "culinary-cream-cheese-spread-bulk-1-30/",
  "schreiber-provolone-loaf-3-12-random-weight/",
  "land-o-lakes-lowfat-blended-vanilla-yogurt-cup-6-2/",
  "schreiber-yellow-pasteurized-process-cheese-product-slices-4-5-flow-through-wrapper-120-slices/",
  "cream-cheese-bulk-1-50/",
  "schreiber-soft-cream-cheese-light-portion-control-cup-100-1oz/",
  "american-heritage-pepper-jack-chunk-12-8oz/",
  "american-heritage-mild-cheddar-fancy-shreds-12-8oz/",
  "american-heritage-soft-cream-cheese-light-cup-12-8oz/",
  "schreiber-mild-cheddar-loaf-8-5/",
  "land-o-lakes-lowfat-blended-strawberry-yogurt-cup-6-2/",
  "schreiber-cheddar-jack-50-50-fancy-shreds-4-5/",
  "raskas-cream-cheese-bulk-1-30/",
  "american-heritage-yellow-pasteurized-process-cheese-product-singles-12-8oz-12-slices/",
  "schreiber-monterey-jack-loaf-2-5/",
  "schreiber-provolone-4-inch-slices-12-1-16-slices/",
  "schreiber-monterey-jack-slices-12-1-20-slices/",
  "friendship-lowfat-plain-yogurt-tub-4-5/",
  "schreiber-swiss-loaf-sandwich-cut-6-8-9-random-weight/",
  "schreiber-muenster-slices-10-1-22-slices/",
  "provolone-chunk-6-8-random-weight/",
  "jalapeno-cream-cheese-spread-bulk-1-30/",
  "schreiber-low-moisture-part-skim-mozzarella-feather-shreds-4-5/",
  "level-valley-creamery-cream-cheese-spread-tub-4-5/",
  "american-heritage-cream-cheese-bar-8oz-bar-3-packs-of-12/",
  "pepper-jack-feather-shreds-4-5/",
  "raskas-whipped-cream-cheese-spread-tub-4-3/",
  "yellow-pasteurized-process-restricted-melt-sharp-american-slices-4-5-200-slices/",
  "schreiber-low-moisture-whole-milk-mozzarella-feather-shreds-4-5/",
  "havarti-slices-12-1-24-slices/",
  "schreiber-mild-cheddar-fancy-shreds-4-5/",
  "schreiber-yellow-pasteurized-process-american-slices-6-3-72-slices/",
  "schreiber-yellow-pasteurized-process-restricted-melt-american-slices-4-5-160-slices/",
  "schreiber-pasteurized-process-pepper-jack-slices-12-1-24-slices/",
  "schreiber-pasteurized-process-hot-pepper-jack-cubes-4-5/",
  "pauly-cream-cheese-loaf-10-3/",
  "american-heritage-string-cheese-retail-package-12-1/",
  "american-heritage-mild-cheddar-chunk-12-8oz/",
  "medium-cheddar-slices-6-1-5-32-slices/",
  "land-o-lakes-lowfat-plain-yogurt-tub-4-5/",
  "schreiber-mild-cheddar-feather-shreds-4-5/",
  "amera-melt-yellow-pasteruzied-process-american-block-1-20/",
  "level-valley-creamery-cream-cheese-loaf-10-3/",
  "schreiber-amera-melt-yellow-pasteurized-process-american-loaf-6-5/",
  "schreiber-provolone-4-inch-slices-6-1-5-32-slices/",
  "white-pasteurized-process-sharp-american-cheese-feather-cut-shreds-4-5/",
  "schreiber-white-pasteurized-processs-american-slices-4-5-200-slices/",
  "schreiber-sharp-cheddar-feather-shreds-4-5/",
  "schreiber-yellow-pasteurized-processs-american-slices-4-5-flow-through-wrapper-96-slices/",
  "schreiber-monterey-jack-feather-shreds-6-5/",
  "schreiber-yellow-pasteurized-process-american-slices-4-5-96-slices/",
  "schreiber-pasteurized-process-hot-pepper-jack-feather-cut-shreds-4-5/",
  "schreiber-mild-cheddar-slices-12-1-32-slices/",
  "cream-cheese-for-baking-bulk-1-50/",
  "schreiber-cream-cheese-substitute-loaf-10-3/",
  "medium-cheddar-jack-fancy-shreds-4-5/",
  "schreiber-swiss-slices-8-1-5-24-slices/",
  "schreiber-colby-jack-snack-cubes-4-5/",
  "american-heritage-string-cheese-bulk-168-1oz/",
  "white-pasteurized-process-restricted-melt-american-slices-4-5-160-slices/",
  "schreiber-2-lactose-free-milk-12-32-fl-oz/",
  "american-heritage-yellow-pasteurized-process-cheese-product-singles-12-12oz-16-slices/",
  "raskas-cream-cheese-with-carob-bean-gum-bulk-1-50/",
  "raskas-cream-cheese-loaf-10-3/",
  "american-heritage-yellow-imitation-pasteurized-process-american-cheese-food-singles-48-12oz-16-slices/",
  "schreiber-swiss-feather-shreds-4-5/",
  "land-o-lakes-plain-yogurt-pail-1-32/",
  "schreiber-pepper-jack-slices-12-1-22-slices/",
  "schreiber-provolone-slices-12-1-32-slices/",
  "schreiber-yellow-pasteurized-process-sharp-american-slices-4-5-flow-through-wrapper-120-slices/",
  "yellow-cheddar-pasteurized-process-cheese-product-restricted-melt-1-4-diced-4-5/",
  "yellow-pasteurized-process-cheese-spread-with-peppers-and-onions-pouch-4-5/",
  "land-o-lakes-lowfat-blended-peach-yogurt-cup-48-4oz/",
  "schreiber-yellow-pasteurized-process-cheese-product-slices-4-5-flow-through-wrapper-160-slices/",
  "schreiber-sharp-cheddar-slices-12-1-22-slices/",
  "american-heritage-cream-cheese-spread-cup-12-8oz/",
  "schreiber-yellow-pasteurized-process-cheese-product-slices-4-5-160-slices/"
]


# Setup Chrome
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Use headless optionally
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Output folder for images
base_folder = "downloaded_images"
os.makedirs(base_folder, exist_ok=True)

# CSV path
csv_path = "products_data.csv"
write_headers = not os.path.exists(csv_path)

for idx, url in enumerate(urls, start=1):
    try:
        print(f"\n🔗 Opening: {url}")
        driver.get("https://www.schreiberfoodsproducts.com/products/" + url)
        time.sleep(1)

        try:
            name = driver.find_element(By.CSS_SELECTOR, ".entry-header h1").text.strip()
        except:
            name = ""
            print("⚠️ Product name not found")

        try:
            desc = driver.find_element(By.CSS_SELECTOR, ".product__header-info p").text.strip()
        except:
            desc = ""
            print("⚠️ Product description not found")

        print(f"🏷️ Product Name: {name}")
        print(f"📝 Description: {desc}")


        # --- Extract accordion HTML and parse with BeautifulSoup ---
        accordion = driver.find_element(By.CLASS_NAME, "accordion")
        soup = BeautifulSoup(accordion.get_attribute("outerHTML"), "html.parser")
        children = [el for el in soup.find("div", class_="accordion").children if el.name in ["h2", "div"]]

        # Ingredients
        ingredients_div = children[3]
        ingredients = ingredients_div.get_text(separator=" ", strip=True)

        # Product Specs
        product_specs_div = children[1]
        product_specs = {}
        tables = product_specs_div.find_all("table", class_="product__specs-table")
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all("td")
                if len(cells) == 2:
                    key = cells[0].get_text(strip=True).replace(":", "")
                    value = cells[1].get_text(strip=True)
                    if key:
                        product_specs[key] = value

        print(f"🧂 Ingredients: {ingredients}")
        print(f"📦 Specs: {product_specs}")

        # --- Setup folder using GTIN ---
        gtin = product_specs.get("GTIN", f"no_gtin_{idx}")
        product_folder = os.path.join(base_folder, url)
        os.makedirs(product_folder, exist_ok=True)

        # --- Download all carousel images ---
        image_elements = driver.find_elements(By.CSS_SELECTOR, "#product-main li.splide__slide img")
        for img_idx, img in enumerate(image_elements, start=1):
            img_url = img.get_attribute("src")
            if not img_url:
                continue
            parsed_url = urlparse(img_url)
            filename = os.path.join(product_folder, f"img_{img_idx}.png")

            try:
                img_data = requests.get(img_url, timeout=10).content
                with open(filename, "wb") as f:
                    f.write(img_data)
                print(f"✅ Saved image {img_idx}: {filename}")
            except Exception as e:
                print(f"❌ Failed image {img_idx}: {e}")

        # --- Click nutrition accordion if needed ---
        accordion_buttons = driver.find_elements(By.CSS_SELECTOR, ".accordion h2 button")
        for btn in accordion_buttons:
            if "Nutrition" in btn.text:
                if btn.get_attribute("aria-expanded") == "false":
                    driver.execute_script("arguments[0].scrollIntoView({block: 'start'});", btn)
                    time.sleep(0.3)
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(0.3)
                break

        # --- Scroll and screenshot nutrition label ---
        nutrition_element = driver.find_element(By.CSS_SELECTOR, ".nutrition__wrapper .nutr-label")
        nutrition_top = driver.execute_script("return arguments[0].getBoundingClientRect().top + window.scrollY;", nutrition_element)
        driver.execute_script(f"window.scrollTo(0, {nutrition_top - 140});")
        time.sleep(0.3)
        nutrition_screenshot_path = os.path.join(product_folder, f"img_{len(image_elements)+1}.png")
        nutrition_element.screenshot(nutrition_screenshot_path)
        print(f"📸 Saved nutrition label: {nutrition_screenshot_path}")

        # --- Save product info to CSV ---

        csv_data = {
            "url": url,
            "GTIN": gtin,
            "Product Name": name,
            "Description": desc,
            "Ingredients": ingredients,
            "Pack Size": product_specs.get("Pack Size", ""),
            "Product Format": product_specs.get("Product Format", ""),
            "Slice Weight": product_specs.get("Slice Weight", ""),
            "Product Performance": product_specs.get("Product Performance", ""),
            "Item Type": product_specs.get("Item Type", ""),
            "Slice Length": product_specs.get("Slice Length", ""),
            "Slice Width": product_specs.get("Slice Width", ""),
        }
        # csv_data.update(product_specs)

        with open(csv_path, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_data.keys())
            if write_headers:
                writer.writeheader()
                write_headers = False
            writer.writerow(csv_data)

        print("✅ Done!\n")

    except Exception as e:
        print(f"⚠️ Error processing {url}: {e}")

driver.quit()
print("🚀 All done!")