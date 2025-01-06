from bs4 import BeautifulSoup
from prefect import task, flow
import csv

# Read the HTML file
with open("./canadaBakers/div_content.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

@task
def collect_Data(children, data_collection ):
    for child in children:
        fields = child.find_all('div', style="border-bottom: 0.5px solid lightgray")
        row = {}
        flip = 0

        for field in fields:

            if flip == 0:
                flip = 1
                continue

            # Extract label and value only if they exist
            label_tag = field.find('span')
            value_tag = field.find('h5')

            # Ensure both label and value exist before extracting
            if label_tag and value_tag:
                label = label_tag.get_text(strip=True)
                value = value_tag.get_text(strip=True)
                row[label] = value

        # Add the row to the collection if not empty
        if row:
            data_collection.append(row)

@task
def write_to_csv(data_collection, csv_file):
    
    if data_collection:
        # Create headers from the first row
        headers = data_collection[0].keys()
        
        # Write to CSV file
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()  # Write headers
            writer.writerows(data_collection)  # Write all rows

        print(f"Data has been written to {csv_file}")


@flow
def filter_Data():
    # Find all child elements within the parent div that match a specific class
    children = soup.select(".w-full.max-w-sm.h-min.bg-white.border.border-gray-200")

    # Print the number of children found
    print(f"Found {len(children)} children")

    # Initialize collections
    data_collection = []

    collect_Data(children, data_collection)

    for i in range(min(3, len(data_collection))):
        print(data_collection[i])
        print("  ")

    csv_file = "output1.csv"

    write_to_csv(data_collection, csv_file)

filter_Data()