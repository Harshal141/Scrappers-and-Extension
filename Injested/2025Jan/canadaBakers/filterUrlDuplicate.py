import pandas as pd

# Define your cleaning function
def clean_domain(domain):
    if domain is None or pd.isna(domain):
        return ""
    if domain[-1] == "/":
        domain = domain[:-1]
    domain = domain.replace("http://", "").replace("https://", "").replace("www.", "")
    domain = domain.split("/")[0]
    domain = domain.lower()
    if "@" in domain or domain.startswith("."):
        return ""
    return domain

# Load the CSV file
file_path = "./canadaBakers/output_filter.csv"
df = pd.read_csv(file_path)

# Apply the cleaning function to the 'Website' column
if 'Website' in df.columns:
    df['Website_cleaned'] = df['Website'].apply(clean_domain)
    # Remove rows where the cleaned domain is empty or contains '--'
    df = df[~df['Website_cleaned'].isin(["", "--"])]
    # Ensure that the websites are unique
    df = df.drop_duplicates(subset='Website_cleaned')
else:
    print("Error: 'Website' column not found in the CSV.")

# Save the cleaned file
output_file_path = "./canadaBakers/cleaned_file.csv"  # Update with your desired output file path
df.to_csv(output_file_path, index=False)
print(f"Cleaned and deduplicated file saved as {output_file_path}")
