import csv
from bs4 import BeautifulSoup
from utility import cleanDomain

# Read the HTML content from a file
with open("./Paperbox/index.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Find all divs with the class "Rank0 gz-grid-col"
elements = soup.find_all("div", class_="Rank0 gz-grid-col")

# Initialize a list to store the extracted data
data = []

# Loop through each element and extract details
for element in elements:
    # Find name
    name_tag = element.find("h5", class_="card-title")
    name = name_tag.get_text(strip=True) if name_tag else None

    # Find address
    address_tag = element.find("a", class_="card-link", itemprop="address")
    address = address_tag.get_text(" ", strip=True) if address_tag else None

    # Find contact
    contact_tag = element.find("a", class_="card-link", href=lambda href: href and href.startswith("tel"))
    contact = contact_tag.get_text(strip=True) if contact_tag else None

    # Find website URL
    website_tag = element.find("li", class_="gz-card-website")
    if website_tag:
        website_a_tag = website_tag.find("a", href=True)
        website = website_a_tag["href"] if website_a_tag else None
    else:
        website = None
    if website:
        website = cleanDomain(website)

    if website == "drupa.com" or website == "linkedin.com":
        website = None

    if website:
        # Append the data to the list
        data.append({
            "name": name,
            "address": address,
            "contact": contact,
            "domain": website,
        })

# Define the CSV file name
csv_file_name = "./Paperbox/DATA_321_paperbox.csv"

# Write the data to a CSV file
with open(csv_file_name, "w", newline="", encoding="utf-8") as csvfile:
    # Define the field names
    fieldnames = ["name", "address", "contact", "domain"]
    
    # Create a CSV writer object
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write the header
    writer.writeheader()
    
    # Write the rows
    writer.writerows(data)

print(f"Data has been saved to {csv_file_name}")
