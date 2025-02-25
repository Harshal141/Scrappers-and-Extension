import csv

def cleanDomain(domainName):
    website = domainName.strip()
    if website[-1] == "/":
        website = website[:-1]
    website = website.replace("http://", "").replace("https://", "").replace("www.", "")
    website = website.split("/")[0]
    website = website.lower()
    return website

with open("Injested/2025Feb/Bevnet/source.csv", "r", encoding="utf-8") as file:
    data = csv.DictReader(file)
    headers = ["name", "domain"]
    with open("Injested/2025Feb/Bevnet/cleaned.csv", "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for entry in data:
            name = entry.get("name", "")
            domain = entry.get("domain", "")
            if domain is not None:
                website = cleanDomain(domain)
            else:
                continue
            writer.writerow([name, website])
print("Data successfully saved to Injested/2025Feb/Bevnet/cleaned.csv.")