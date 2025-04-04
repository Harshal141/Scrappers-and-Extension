import pandas as pd

# Load the CSV file
input_file = "14kListRandom.csv"  # Update with your actual file path
output_file = "filtered_output.csv"

# Read the CSV
df = pd.read_csv(input_file)

# Convert "Already processed" column to string for comparison
df["Already processed"] = df["Already processed"].astype(str)

# Filter rows where "Already processed" is "No" (not equal to manufacturer_id)
filtered_df = df[df["Already processed"] != df["manufacturer_id"].astype(str)]

# Keep only the "domain" column and add an empty "name" column
filtered_df = filtered_df[["domain"]]
filtered_df.insert(0, "name", "")  # Insert empty "name" column at the beginning

# Save to new CSV
filtered_df.to_csv(output_file, index=False)

print(f"Filtered data saved to {output_file}")
