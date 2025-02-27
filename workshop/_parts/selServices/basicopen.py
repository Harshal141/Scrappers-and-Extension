from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize the WebDriver (Example: Chrome)
driver = webdriver.Chrome()

# Open the desired URL
driver.get('https://example.com')

# Find the element using CSS selector with multiple classes
element = driver.find_element(By.CSS_SELECTOR, '.supplier-result-title.item-title')

# Print the text or interact with the element
print(element.text)

# Close the browser
driver.quit()
