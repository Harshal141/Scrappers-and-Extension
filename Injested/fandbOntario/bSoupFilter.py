from bs4 import BeautifulSoup
import csv
import re

def clean_whitespaces(text):
    cleaned_text = []
    for line in text:
        line = line.strip()
        if line:
            line = re.sub(r'\s+', ' ', line)
            cleaned_text.append(line)

    return "\n".join(cleaned_text[2:])


with open("./fandbOntario/input.html", "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser")

articles = soup.find_all('article')

collection = []
for article in articles:
    title = article.find(class_="elementor-heading-title").text.strip()
    companyType = ", ".join([item.text.strip() for item in article.find_all(class_="elementor-post-info__terms-list-item")])

    description_box = article.select_one('.elementor-element.elementor-element-11a1afd.elementor-widget.elementor-widget-theme-post-excerpt')
    
    phone = ""
    website = ""
    desc = ""

    if description_box:
        description = description_box.find(class_="elementor-widget-container")
        if description:
            phone = description.text.split('\n')[1].strip()
            website = description.find('a')['href'].strip()
            if website[-1] == "/":
                website = website[:-1]
            website = website.replace("http://", "").replace("https://", "").replace("www.", "")
            website = website.split("/")[0]
            website = website.lower()
            desc = clean_whitespaces(description.text.split('\n'))

    else:
        print("description_box was not found!")

    data = {
        "Company Name": title,
        "Company Type": companyType,
        "Phone No": phone,
        "Website URL": website,
        "Description": desc,
    }
    collection.append(data)

print(collection[:2])

with open("./fandbOntario/parsed_data.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["Company Name", "Company Type", "Phone No", "Website URL", "Description"])

    writer.writeheader()
    writer.writerows(collection)

print("Data saved to 'output.csv' successfully!")