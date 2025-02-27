import json
import csv
from urllib.parse import urlparse

# Input and Output Files
input_file = 'final_part_2.json'
output_file = 'final_part_2.csv'

def clean_domain(url):
    """
    Cleans the URL to extract the domain without protocol, www, or trailing slash.
    """
    if not url:
        return ''
    
    # Parse the URL
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    # Remove 'www.' if present
    if domain.startswith('www.'):
        domain = domain[4:]
    
    return domain

def json_to_csv(file_path):
    """
    Converts JSON data to a CSV file with Name and Cleaned Domain columns.
    Removes duplicate Cleaned Domains.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Using a set to track unique cleaned domains
    seen_domains = set()
    unique_data = []

    # Process each entry
    for entry in data:
        name = entry.get('name', 'N/A')
        domain = entry.get('domain', 'N/A')
        cleaned_domain = clean_domain(domain)
        
        # Check for duplicates
        if cleaned_domain and cleaned_domain not in seen_domains:
            seen_domains.add(cleaned_domain)
            unique_data.append({
                "name": name,
                "cleaned_domain": cleaned_domain
            })
        else:
            print(f"Duplicate domain skipped: {cleaned_domain}")

    # Open CSV for writing
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['Name', 'Domain'])
        
        # Write unique rows
        for entry in unique_data:
            writer.writerow([entry['name'], entry['cleaned_domain']])

    print(f"CSV file '{output_file}' created successfully with unique domains.")

if __name__ == '__main__':
    json_to_csv(input_file)
