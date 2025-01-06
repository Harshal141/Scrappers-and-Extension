import requests

url = "https://www.dnb.com/business-directory/company-profiles.magna_international_inc.a5e89a69831772b0540706aeb05c039a.html"

# Headers as provided
headers = {
    # ":authority": "api5763.d41.co",
    # ":method": "GET",
    # ":path": "/api?ctver=6&req=api5763&form=json",
    # ":scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "origin": "https://www.dnb.com",
    "priority": "u=1, i",
    "referer": "https://www.dnb.com/business-directory/company-profiles.magna_international_inc.a5e89a69831772b0540706aeb05c039a.html",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

# Sending the GET request
response = requests.get(url, headers=headers)

# Output the response
if response.status_code == 200:
    print("Request successful!")
    print("Response:", response.text)
else:
    print(f"Failed to fetch the page. Status code: {response.status_code}")
    print("Response:", response.text)
