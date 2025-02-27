import json
import csv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def cleanDomain(domainName):
    """
    Cleans and normalizes domain names.
    - Removes http://, https://, and www.
    - Strips trailing slashes.
    - Converts to lowercase.
    """
    if not domainName:
        return None
    website = domainName.strip()
    if website.endswith("/"):
        website = website[:-1]
    website = website.replace("http://", "").replace("https://", "").replace("www.", "")
    website = website.split("/")[0]
    website = website.lower()
    return website

def json_to_csv(input_file, output_file):
    """
    Converts a JSON file to a CSV file with cleaned and unique columns: name, domain
    """
    try:
        # Load JSON data
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Use a set to track unique domains
        unique_data = set()
        cleaned_data = []

        # Clean and filter data
        for entry in data:
            name = entry.get('name', '').strip()
            domain = entry.get('domain', '').strip()

            # Clean the domain
            cleaned_domain = cleanDomain(domain)

            # Check for null values and duplicates
            if name and cleaned_domain and (name, cleaned_domain) not in unique_data:
                unique_data.add((name, cleaned_domain))
                cleaned_data.append({
                    'name': name,
                    'domain': cleaned_domain
                })

        # Open CSV file for writing
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'domain']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # Write the cleaned and unique data
            for entry in cleaned_data:
                writer.writerow(entry)

        logging.info(f"CSV file created: {output_file}")

    except FileNotFoundError:
        logging.error(f"File {input_file} not found.")
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

def main():
    # Convert input JSON to cleaned and unique CSV
    json_to_csv('total_bevnet.json', 'cleaned_domains.csv')

if __name__ == "__main__":
    main()
