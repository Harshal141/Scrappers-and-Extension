
ids = [66,61,68,62,67,63,70,72,65,69,64,73]

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time

from _utils.cleaner import your_function_name


# driver = webdriver.Chrome()

# data = []

# flip = 0
# for id in ids:
#     if flip == 1:
#         break
#     else:
#         flip= 1
#     driver.get(f"https://www.thinkusadairy.org/applications/supplier-search/Results?CategoryID={id}&startRow=0&rowsPerPage=100")
#     print(driver.current_url)
#     print(driver.title)
#     time.sleep(3)

#     parents = driver.find_elements(By.CSS_SELECTOR, '.supplier-result.content-box')
#     for parent in parents:
#         title = parent.find_element(By.CSS_SELECTOR, '.supplier-result-title.item-title')
#         bottomRow = parent.find_element(By.CSS_SELECTOR, '.row.bottom-row')
#         a_tag = bottomRow.find_element(By.CSS_SELECTOR, 'a')
#         name = title.text.strip()
#         domain = a_tag.get_attribute('href')
#         website = cleanDomain(domain)
#         data.append([name, website])
#         print(name, website)

# # save to csv
# import csv
# headers = ["name", "domain"]

# with open("workshop/usdairy/suppliers_temp.csv", "w", encoding="utf-8", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(headers)
#     for entry in data:
#         writer.writerow(entry)
# print("Data successfully saved to workshop/usdairy/suppliers.csv.")



# driver.quit()
