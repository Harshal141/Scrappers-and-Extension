import csv
from urllib.parse import urlparse

# Input and Output Files
input_file = 'vitafood.csv'
output_file = 'final_vitafood.csv'

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

def csv_clean_domains(file_path):
    """
    Cleans the domains and removes null domains from the CSV.
    """
    cleaned_data = []

    # Open CSV for reading
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            name = row.get('Name', 'N/A')
            url = row.get('URL', '').strip()
            
            # Clean the domain
            cleaned_domain = clean_domain(url)
            
            # Only add rows with non-empty cleaned domain
            if cleaned_domain:
                cleaned_data.append({
                    "name": name,
                    "domain": cleaned_domain
                })

    # Open CSV for writing
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['Name', 'Domain'])
        
        # Write cleaned rows
        for entry in cleaned_data:
            writer.writerow([entry['name'], entry['domain']])

    print(f"Cleaned CSV file '{output_file}' created successfully.")

if __name__ == '__main__':
    csv_clean_domains(input_file)
