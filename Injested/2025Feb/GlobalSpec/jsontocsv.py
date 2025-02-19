import json
import csv
from urllib.parse import urlparse

def clean_domain(url):
    """
    Extracts and cleans the domain from a URL.
    For example, 'https://www.ellsworth.com/' becomes 'ellsworth.com'.
    """
    parsed = urlparse(url)
    domain = parsed.netloc
    # Remove 'www.' prefix if present
    if domain.startswith("www."):
        domain = domain[4:]
    # Remove any trailing slash (if present in path, but usually netloc doesn't contain slash)
    return domain

def main():
    input_file = "final_filteredData.json"
    output_file = "final_filtered.csv"
    
    # Load JSON data
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Open CSV file for writing
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # Write header row
        writer.writerow(["name", "domain"])
        
        # Process each entry and write to CSV
        for entry in data:
            name = entry.get("supplier_name", "").strip()
            website = entry.get("supplier_website", "").strip()
            domain = clean_domain(website)
            writer.writerow([name, domain])
    
    print(f"CSV conversion complete. Output saved to {output_file}")

if __name__ == "__main__":
    main()
