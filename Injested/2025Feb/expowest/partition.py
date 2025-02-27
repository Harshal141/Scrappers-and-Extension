import json
from urllib.parse import urlparse

# Input and Output Files
first_file = 'final_part_1.json'
second_file = 'extracted_name_domain.json'
output_file = 'final_part_2.json'

def clean_domain(url):
    """
    Cleans the URL to extract the domain without protocol, www, or trailing slash.
    """
    if not url:
        return ''
    
    # Parse the URL
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    
    # Remove 'www.' if present
    if domain.startswith('www.'):
        domain = domain[4:]
    
    return domain

def compare_json(first_path, second_path):
    """
    Compares two JSON files and finds entries in the second file 
    that are not present in the first file.
    """
    # Load first JSON
    with open(first_path, 'r', encoding='utf-8') as f:
        first_data = json.load(f)
    
    # Load second JSON
    with open(second_path, 'r', encoding='utf-8') as f:
        second_data = json.load(f)

    # Extract and clean domains from the first file
    first_domains = {clean_domain(item['domain']) for item in first_data}

    # Filter second data to find domains not in the first file
    not_in_first = [
        item for item in second_data
        if clean_domain(item['domain']) not in first_domains
    ]

    # Save the result to a new JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(not_in_first, f, indent=4)

    print(f"Entries not present in the first file saved to '{output_file}'")
    print(f"{len(not_in_first)} new entries found.")

if __name__ == '__main__':
    compare_json(first_file, second_file)
