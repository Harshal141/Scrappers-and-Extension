import json
import re
from urllib.parse import urlparse

# Input and Output Files
input_file = 'neimaganzine.json'
output_file = 'neimaganzine_final.json'

def extract_website(text):
    """
    Extracts website URL from the given text.
    """
    # Regular expression to find website URLs
    website_pattern = re.compile(
        r"Website:\s*(https?://)?(www\.)?([a-zA-Z0-9.-]+)", re.IGNORECASE)
    
    match = website_pattern.search(text)
    if match:
        domain = match.group(3).lower()
        return domain
    return None

def extract_unique_websites(file_path):
    """
    Extracts unique websites from the JSON file.
    """
    websites = set()

    # Load the input JSON file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract websites from Field1
    for item in data:
        field1 = item.get('Field1', '')
        website = extract_website(field1)
        if website:
            websites.add(website)

    # Convert set to list and wrap each domain in an object
    unique_websites = [{"domain": domain} for domain in sorted(list(websites))]

    # Save to output JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(unique_websites, f, indent=4)

    print(f"Extracted {len(unique_websites)} unique websites.")
    print(f"JSON file '{output_file}' created successfully.")

if __name__ == '__main__':
    extract_unique_websites(input_file)
