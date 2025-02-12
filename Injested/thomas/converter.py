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

def json_to_csv(input_file, output_file):
    try:
        # Read the JSON file
        with open(input_file, 'r') as json_file:
            data = json.load(json_file)

        # Open the CSV file for writing
        with open(output_file, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write the header row
            csv_writer.writerow(["name", "domain"])
            unique_domains = set()
            # Iterate through the JSON data
            for record in data:
                if record.get("domain") != "Domain not found!":
                    domain = cleanDomain(record.get("domain"))
                    if domain in unique_domains:
                        print(f"Duplicate domain found: {domain}")
                        continue
                    csv_writer.writerow([record.get("name", ""), domain])
                    unique_domains.add(domain)

        print(f"CSV file '{output_file}' created successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_file = "Injested/thomas/DATA_385/batch2.json"  # Replace with your JSON file path
output_file = "Injested/thomas/DATA_385/batch2.csv"  # Replace with your desired CSV file path

# Call the function
json_to_csv(input_file, output_file)


# import json

# # Load the original JSON file
# input_file = "Injested/thomas/DATA_385/data.json"  # Update with your actual file path
# output_file = "Injested/thomas/DATA_385/data_indexed.json"

# # Read the raw JSON data
# with open(input_file, "r", encoding="utf-8") as file:
#     raw_data = json.load(file)

# # Extract and clean the data
# cleaned_data = []
# index = 1
# unique_domains = set()

# for item in raw_data:
#     # Extract the required fields
#     name = item.get("name", "")
#     domain = item.get("relDomain", "")
#     if domain in unique_domains:
#         continue
#     cleaned_data.append({
#         "index": index,
#         "name": name,
#         "url": domain
#     })
#     index += 1
#     unique_domains.add(domain)

# # Save the cleaned data to a new JSON file
# with open(output_file, "w", encoding="utf-8") as file:
#     json.dump(cleaned_data, file, indent=4)

# print(f"Cleaned data saved to {output_file}")

