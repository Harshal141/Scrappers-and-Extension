from bs4 import BeautifulSoup
import csv

# Path to the HTML file
html_file_path = "expoData.html"  # Replace with the path to your HTML file

# Load the HTML file
with open(html_file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all elements with the class `csdXSf`
elements = soup.find_all(class_='csdXSf')

# Extract the text and remove duplicates
data = {element.get_text(strip=True) for element in elements}  # Use a set to store unique texts

# Save the data to a CSV file
output_file = 'csdXSf_data_unique.csv'
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Text'])  # Header row
    writer.writerows([[text] for text in sorted(data)])  # Sort data alphabetically for consistency

print(f"Unique data extracted and saved to {output_file}")
