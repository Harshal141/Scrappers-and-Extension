from dotenv import load_dotenv
import os
import pandas as pd
import psycopg2

# Load environment variables from .env
load_dotenv()

# Load the CSV file containing company names and domains
csv_file = 'expowest/DATA_335_expowest_result_cleaned.csv'
df = pd.read_csv(csv_file)

# Ensure the CSV has the required columns
required_columns = {'name', 'domain'}
if not required_columns.issubset(df.columns):
    raise ValueError(f"The CSV must include the following columns: {required_columns}")

# Convert domain and name into a list of dictionaries for easy iteration
company_data = df[['name', 'domain']].to_dict('records')

# Set up the database connection
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    dbname='auth',
    user='postgres',
    password=os.getenv('DB_PASS')
)
cur = conn.cursor()

# Open a file to save the output
output_file = 'expowest/DATA_335_expowest_existing_contacts.csv'
results_data = []

for company in company_data:
    name = company['name']
    domain = company['domain']

    print("running " + name)

    # Fetch users' data (name, email, and type) for the domain
    contacts_query = f"""
    SELECT name, email, type 
    FROM users 
    WHERE email LIKE '%@{domain}';
    """
    cur.execute(contacts_query)
    contacts_results = cur.fetchall()

    # Extract the company type
    if contacts_results:
        company_type = contacts_results[0][2]  # Assuming 'type' is the third column in the SELECT
        merged_contacts = ",\n ".join(
            [f"{Name} <{Email}>" for Name, Email, type in contacts_results]
        )
    else:
        company_type = "Unknown"
        merged_contacts = "No contacts found"

    # Append the result for this company
    results_data.append({
        'company_name': name,
        'domain': domain,
        'contacts': merged_contacts,
        'company_type': company_type
    })

# Write the results to a CSV file
output_df = pd.DataFrame(results_data)
output_df.to_csv(output_file, index=False)

print(f"Results saved to {output_file}")

# Close the database connection
cur.close()
conn.close()
