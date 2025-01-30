# import json
# import csv

# def json_to_csv(input_file, output_file):
#     try:
#         # Read the JSON file
#         with open(input_file, 'r') as json_file:
#             data = json.load(json_file)

#         # Open the CSV file for writing
#         with open(output_file, 'w', newline='') as csv_file:
#             csv_writer = csv.writer(csv_file)

#             # Write the header row
#             csv_writer.writerow(["name", "domain"])

#             # Iterate through the JSON data
#             for record in data:
#                 if record.get("domain") != "Domain not found!":
#                     csv_writer.writerow([record.get("name", ""), record.get("domain", "")])

#         print(f"CSV file '{output_file}' created successfully.")

#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Example usage
# input_file = "./thomas/thomas_packaging_2.json"  # Replace with your JSON file path
# output_file = "./thomas/thomas_packaging_2.csv"  # Replace with your desired CSV file path

# # Call the function
# json_to_csv(input_file, output_file)


import json

# Load the original JSON file
input_file = "thomas/data.json"  # Update with your actual file path
output_file = "thomas/data_source.json"

# Read the raw JSON data
with open(input_file, "r", encoding="utf-8") as file:
    raw_data = json.load(file)

# Extract and clean the data
cleaned_data = []
index = 1

for item in raw_data:
    if "domain" in item and isinstance(item["domain"], list):
        for entry in item["domain"]:
            if "name" in entry and "relDomain" in entry:
                cleaned_data.append({
                    "index": index,
                    "name": entry["name"],
                    "relDomain": entry["relDomain"]
                })
                index += 1  # Increment index for each entry

# Save the cleaned data to a new JSON file
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(cleaned_data, file, indent=4)

print(f"Cleaned data saved to {output_file}")
