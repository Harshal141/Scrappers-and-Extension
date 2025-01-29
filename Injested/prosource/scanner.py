from bs4 import BeautifulSoup

# Read the HTML content from a file
with open("./prosource/index.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Base URL to append
base_url = "https://www.prosource.org/"

# Initialize an array to store the URLs
urls = []

# Find all <li> tags with data-component="category-entry-card"
elements = soup.find_all("li", {"data-component": "category-entry-card"})

# Loop through each element and extract the href
for element in elements:
    a_tag = element.find("a", href=True)  # Find the <a> tag with an href attribute
    if a_tag:
        full_url = base_url + a_tag["href"].lstrip("/")  # Append to base URL and remove leading slash
        urls.append(full_url)  # Add to the list

# Save the URLs to a file
output_file = "./prosource/DATA_320_urls_array.txt"
with open(output_file, "w", encoding="utf-8") as file:
    file.write(str(urls))  # Write the array as a string

print(f"URLs have been saved to {output_file}")
