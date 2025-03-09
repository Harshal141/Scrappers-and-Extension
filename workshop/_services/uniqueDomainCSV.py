import pandas as pd

COLUMN_NAME = 'domain'

INPUT_FILE = "workshop/fssc/cleanedusa.csv"

OUTPUT_FILE = INPUT_FILE.replace(".csv", "_unique.csv")

# Load the CSV file
df = pd.read_csv(INPUT_FILE)  # Replace with the actual file name

# Drop duplicates based on the "domain" column, keeping only the first occurrence
df_cleaned = df.drop_duplicates(subset=COLUMN_NAME, keep="first")

# Save the cleaned data back to a new CSV file
df_cleaned.to_csv(OUTPUT_FILE, index=False)

print("Duplicates removed. Cleaned file saved as 'cleaned_file.csv'.")
