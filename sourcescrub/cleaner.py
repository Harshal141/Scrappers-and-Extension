import pandas as pd
import os

# Define the function to clean domain names
def cleanDomain(domainName):
    website = domainName.strip()
    if website[-1] == "/":
        website = website[:-1]
    website = website.replace("http://", "").replace("https://", "").replace("www.", "")
    website = website.split("/")[0]
    website = website.lower()
    return website

# Load the CSV file
csv_file = "sourcescrub/DATA_391/soursescrub_391.csv"  # Change to your actual CSV file path
df = pd.read_csv(csv_file)

# Normalize column names (handling potential case differences)
df.columns = df.columns.str.strip().str.lower()  

# Ensure 'domain' column exists
if "domain" not in df.columns:
    raise ValueError("CSV file must contain a 'Domain' column.")

# Clean the domains
df["domain"] = df["domain"].astype(str).apply(cleanDomain)

# Remove duplicates based on the cleaned domain column
before_dedup = len(df)
df = df.drop_duplicates(subset=["domain"])
after_dedup = len(df)

# Count the number of duplicates removed
duplicates_removed = before_dedup - after_dedup
print(f"Total duplicates removed: {duplicates_removed}")

# Define the output directory
output_dir = "sourcescrub/DATA_391/cleaned_batches"
os.makedirs(output_dir, exist_ok=True)  # Create folder if it doesn't exist

batch_size = 990

# Save data in chunks
for i, start in enumerate(range(0, len(df), batch_size), start=1):
    batch_df = df.iloc[start:start + batch_size]
    output_path = os.path.join(output_dir, f"cleaned_batch_{i}.csv")
    batch_df.to_csv(output_path, index=False)

print(f"Processing completed! {len(df) // batch_size + 1} batch files created in '{output_dir}' folder.")
