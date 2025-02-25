import pandas as pd
import os

# Define the function to clean domain names
def cleanDomain(domainName):
    if not domainName:
        return
    website = domainName.strip()
    if website[-1] == "/":
        website = website[:-1]
    website = website.replace("http://", "").replace("https://", "").replace("www.", "")
    website = website.split("/")[0]
    website = website.lower()
    return website

# Load the CSV file
csv_file = "Sourcescrub - FP US Not Ing Filtered Next 10,000 2025.02.21 122319982.csv"  # Change to your actual CSV file path
df = pd.read_csv(csv_file)

# Normalize column names (handling potential case differences)
df.columns = df.columns.str.strip().str.lower()  

# Ensure 'domain' column exists
if "website" not in df.columns:
    raise ValueError("CSV file must contain a 'Domain' column.")

# Clean the domains
df["domain"] = df["website"].astype(str).apply(cleanDomain)

# Remove duplicates based on the cleaned domain column
before_dedup = len(df)
df = df.drop_duplicates(subset=["domain"])
df = df[["company name","domain"]]
after_dedup = len(df)

# Count the number of duplicates removed
duplicates_removed = before_dedup - after_dedup
print(f"Total duplicates removed: {duplicates_removed}")

# Define the output directory
output_dir = "Sourcescrub_422_clean.csv"
# os.makedirs(output_dir, exist_ok=True)  # Create folder if it doesn't exist

df.to_csv(output_dir, index=False)