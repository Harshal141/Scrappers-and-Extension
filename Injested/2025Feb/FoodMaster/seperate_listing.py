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
    website = domainName.strip()
    if website.endswith("/"):
        website = website[:-1]
    website = website.replace("http://", "").replace("https://", "").replace("www.", "")
    website = website.split("/")[0]
    website = website.lower()
    return website

def json_to_csv(input_file, output_file):
    """
    Converts a JSON file to a CSV file with cleaned columns: name, domain
    """
    try:
        # Load JSON data
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Open CSV file for writing
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'domain']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # Extract, clean, and write relevant data
            for entry in data:
                name = entry.get('company_name', 'N/A').strip()
                domain = entry.get('company_domain', 'N/A').strip()

                # Clean the domain
                cleaned_domain = cleanDomain(domain)
                
                writer.writerow({'name': name, 'domain': cleaned_domain})

        logging.info(f"CSV file created: {output_file}")

    except FileNotFoundError:
        logging.error(f"File {input_file} not found.")
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

def main():
    # Convert sponsered_listing JSON to CSV
    json_to_csv('us_canada_sponsered_listing.json', 'us_canada_sponsered_listing.csv')

    # Convert listing_summaries JSON to CSV
    json_to_csv('us_canada_listing_summaries.json', 'us_canada_listing_summaries.csv')

if __name__ == "__main__":
    main()
