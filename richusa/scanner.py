from bs4 import BeautifulSoup

with open("./richusa/cards.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# // parse the html using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Find all product elements
products = soup.find_all("div", class_="product product-card")

# Extract data into a list of dictionaries
result = []
for product in products:
    product_id = product.find("a", class_="product-code").find("span").text
    
    image_tag = product.find("img")
    image_url = image_tag["src"] if image_tag else None
    
    # Add to result list
    if product_id and image_url:
        result.append({"id": product_id, "imageurl": image_url})

print(result[:3])


# save in a text file after parsing

with open("./richusa/parsed_data.txt", "w", encoding="utf-8") as file:
    for item in result:
        file.write(f"{item}\n")