import json
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize WebDriver
driver = webdriver.Chrome()

try:
    # Open the website
    driver.get("https://www.packworld.com/leaders")

    time.sleep(10)
    # Wait for elements to load
    wait = WebDriverWait(driver, 10)

    # Find all company list items
    company_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.leaders-nav__item")))

    # Initialize ActionChains
    actions = ActionChains(driver)

    # Store results
    results = []

    # Iterate through each company element
    for company in company_elements:
        try:
            # Hover over the company item
            actions.move_to_element(company).perform()
            time.sleep(1)  # Allow time for the active card to change

            # Find the currently active card
            active_card = driver.find_element(By.CSS_SELECTOR, ".leaders-card--active")

            # Extract company name
            name_element = company.find_element(By.CSS_SELECTOR, ".leaders-nav-link-contents__title")
            company_name = name_element.text.strip()

            # Extract "Visit Site" link (if available)
            try:
                visit_site_element = active_card.find_element(By.CSS_SELECTOR, "div.leaders-company-details__links a.leaders-button-link--accent")
                visit_site_url = visit_site_element.get_attribute("href")
            except:
                visit_site_url = None  # If "Visit Site" link is missing

            # Store in list
            results.append({"name": company_name, "domain": visit_site_url})
            print(f"Extracted: {company_name} - {visit_site_url}")

        except Exception as e:
            print(f"Error extracting data for one company: {e}")

    # Save results to JSON file
    with open("output.json", "w") as f:
        json.dump(results, f, indent=4)

    print("\nData successfully saved to output.json")

finally:
    # Close browser
    driver.quit()
