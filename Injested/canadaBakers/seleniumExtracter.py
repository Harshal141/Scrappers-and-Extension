from prefect import task, flow
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Chrome()

@task
def next_page():
    next_button = driver.find_element(By.ID, 'nextPage')
    ActionChains(driver).move_to_element(next_button).perform()
    next_button.click()
    print("Clicked the 'Next' button")

@task
def save_data(elements):
    parent = elements[1] # The second element contains the data we need

    div_html = parent.get_attribute('innerHTML')


    with open('./canadaBakers/div_content.html', 'a', encoding='utf-8') as file:
        file.write(div_html)

    print("HTML content has been appended to div_content.txt")


@flow
def extract_Data():
    try:
        driver.get('https://app.joinit.com/o/the-baking-association/directory')  # Replace with the actual URL
        
        time.sleep(5)

        country_select_element = driver.find_element(By.CLASS_NAME, 'country_selector')
        
        # Use the Select class to interact with the dropdown
        select = Select(country_select_element)

        # Select the option with visible text "Canada"
        select.select_by_visible_text('Canada')

        # Verify the selection or continue with other actions
        print(f"Selected option: {select.first_selected_option.text}")
        step = 0

        while True:
            step += 1
            time.sleep(5)

            try:
                no_records_message = driver.find_element(By.XPATH, '//h5[text()="No membership records matched this query"]')
                print("No membership records matched. Stopping the loop.")
                break
            except:
                pass

            elements = driver.find_elements(By.CSS_SELECTOR, '.grid.grid-cols-1')

            if len(elements) >= 2:  
                save_data(elements)
            else:
                print("Less than two elements found with the selector .grid.grid-cols-1")
                break

            next_page()

            if step == 50:
                break

    finally:
        driver.quit()

if __name__ == '__main__':
    extract_Data()
