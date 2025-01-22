import json
import csv

def cleanDomain(domainName):
    website = domainName.strip()
    if website[-1] == "/":
        website = website[:-1]
    website = website.replace("http://", "").replace("https://", "").replace("www.", "")
    website = website.split("/")[0]
    website = website.lower()
    return website


# Define function to process the input JSON file and save extracted data as CSV
def process_json_to_csv(input_file, output_file):
    try:
        # Load JSON data from the input file
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Extract only name, domain (from URL), and isRelated fields
        transformed_data = [
            {
                "name": entry["name"],
                "domain": cleanDomain(entry["url"]),
                "isRelated": entry["isRelated"]
            }
            for entry in data
        ]
        
        # Write to CSV
        csv_columns = ["name", "domain", "isRelated"]
        with open(output_file, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
            writer.writeheader()
            writer.writerows(transformed_data)

        print(f"Data successfully processed and saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Specify input and output file paths
input_json_file = "./FnBScanner/DATA_267_ai.json"  # Replace with the path to your JSON file
output_csv_file = "./FnBScanner/DATA_267_result.csv"  # Replace with the desired CSV output path

# Call the function
process_json_to_csv(input_json_file, output_csv_file)
