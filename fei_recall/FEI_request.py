
import requests
import json

# 🔐 Replace with your actual credentials
AUTH_USER = "harshal.patil@keychain.com"
AUTH_KEY = "jDzWkw2aoREMOPi3"

# ✅ Known FEINumber (use this to test)
TEST_FEINUMBER = 1251294  # Confirmed from FDA sample documentation

# 📦 Request body with updated columns
body = {
    "start": 1,
    "rows": 1,
    "sort": "InspectionID",
    "sortorder": "DESC",
    "filters": {
        "InspectionID": [TEST_FEINUMBER]
    },
    "columns": [
        "InspectionID",
        "FEINumber",
        "AddressLine1",     # street_address
        "AddressLine2",     # street_address
        "City",             # city
        "State",            # state
        "ZipCode",          # zip_code
        "CountryName",      # country
        "FirmProfile"       # dashboard_url (interpreted or renamed as per your use)
    ]
}

# 🌐 Headers with authentication
headers = {
    "Content-Type": "application/json",
    "Authorization-User": AUTH_USER,
    "Authorization-Key": AUTH_KEY
}

# 📤 POST request
response = requests.post(
    "https://api-datadashboard.fda.gov/v1/inspections_classifications",
    headers=headers,
    json=body
)

# 🖨️ Output
print("Status Code:", response.status_code)
try:
    print("Response JSON:\n", json.dumps(response.json(), indent=2))
except ValueError:
    print("Non-JSON response:\n", response.text)
