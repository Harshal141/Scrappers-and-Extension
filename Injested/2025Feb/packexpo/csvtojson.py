import json
import csv
from urllib.parse import urlparse

# Input and Output Files
input_file = 'filtered_us_ca_packExpo.json'
output_file = 'filtered_us_ca_packExpo.csv'

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
    Converts JSON data to a CSV file with Name, Domain, and Cleaned Domain columns.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Open CSV for writing
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['Name', 'Domain'])
        
        # Write rows
        for entry in data:
            name = entry.get('name', 'N/A')
            domain = entry.get('url', 'N/A')
            cleaned_domain = clean_domain(domain)
            writer.writerow([name,cleaned_domain])

    print(f"CSV file '{output_file}' created successfully.")

if __name__ == '__main__':
    json_to_csv(input_file)
