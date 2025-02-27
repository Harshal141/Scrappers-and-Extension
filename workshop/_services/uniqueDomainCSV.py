import pandas as pd

# Load the CSV file
df = pd.read_csv("workshop/newtopisnow/cleanedBatch2.csv")  # Replace with the actual file name

# Drop duplicates based on the "domain" column, keeping only the first occurrence
df_cleaned = df.drop_duplicates(subset="name", keep="first")

# Save the cleaned data back to a new CSV file
df_cleaned.to_csv("workshop/newtopisnow/cleanedBatch3.csv", index=False)

print("Duplicates removed. Cleaned file saved as 'cleaned_file.csv'.")
