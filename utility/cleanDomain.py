website = description.find('a')['href'].strip()
if website[-1] == "/":
    website = website[:-1]
website = website.replace("http://", "").replace("https://", "").replace("www.", "")
website = website.split("/")[0]
website = website.lower()