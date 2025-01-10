from bs4 import BeautifulSoup
import json

# Load the HTML file
file_path = "./WFF/index.html"
with open(file_path, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# JSON data collection
collection = []

# Loop through all tables and rows
rows = soup.find_all("tr")
print("rows", len(rows))

for row in rows:
    # Get all <td> elements
    tds = row.find_all("td")
    if len(tds) >= 2:  # Check if the second <td> exists
        second_td = tds[1]
        a_tag = second_td.find("a")  # Find the <a> tag inside the second <td>
        if a_tag and a_tag.get("href"):  # Ensure <a> tag and href exist
            collection.append({
                "name": a_tag.text.strip(),
                "url": a_tag["href"]
            })

# Save the results to a JSON file
output_file = "./WFF/urls.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(collection, file, indent=4, ensure_ascii=False)

print(f"Data saved to {output_file}.")
