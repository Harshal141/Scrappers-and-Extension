import csv
from urllib.parse import urlparse

# Input and Output Files
input_file = 'input.csv'
output_file = 'output.csv'

def clean_domain(url):
    """
    Cleans the URL to extract the domain without protocol, www, or trailing slash.
    """
    if not url:
        return ''
    
    # Parse the URL
    parsed_url = urlparse(url.strip())
    domain = parsed_url.netloc.lower()  # Convert to lowercase
    
    # Remove 'www.' if present
    if domain.startswith('www.'):
        domain = domain[4:]
    
    return domain

def is_valid_domain(domain):
    """
    Checks if the domain is valid (not null, empty, or invalid).
    """
    # Domain should not be empty, just a hyphen, or only whitespace
    return bool(domain and domain != '-' and domain.strip())

def csv_clean_domains(file_path):
    """
    Cleans the domains, removes null or invalid domains, and saves to a new CSV.
    """
    cleaned_data = []

    # Open CSV for reading
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            name = row.get('Name', 'N/A').strip()
            domain = row.get('Domain', '').strip()
            
            # Clean the domain
            cleaned_domain = clean_domain(domain)
            
            # Only add rows with non-empty, valid cleaned domain
            if is_valid_domain(cleaned_domain):
                cleaned_data.append([name, cleaned_domain])

    # Open CSV for writing
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['Name', 'Domain'])
        
        # Write cleaned rows
        writer.writerows(cleaned_data)

    print(f"Cleaned CSV file '{output_file}' created successfully.")

if __name__ == '__main__':
    csv_clean_domains(input_file)
