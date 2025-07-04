from bs4 import BeautifulSoup

# Corrected HTML snippet (fixing missing closing </a> tags)
html = """
<ol start="151" class="browse_categoryList__OH7sX"><li class="browse_categoryListItem__iXxDh"><a href="https://www.thomasnet.com/suppliers/usa/cosmetic-stencils-97008078">Cosmetic Stencils</a><small class="pad-l-2">(8 suppliers)</small></li><li class="browse_categoryListItem__iXxDh"><a href="https://www.thomasnet.com/suppliers/usa/manicure-sticks-80500606">Manicure Sticks</a><small class="pad-l-2">(12 suppliers)</small></li><li class="browse_categoryListItem__iXxDh"><a href="https://www.thomasnet.com/suppliers/usa/sun-care-products-81345001">Sun Care Products</a><small class="pad-l-2">(90 suppliers)</small></li><li class="browse_categoryListItem__iXxDh"><a href="https://www.thomasnet.com/suppliers/usa/sunglasses-81346009">Sunglasses</a><small class="pad-l-2">(192 suppliers)</small></li><li class="browse_categoryListItem__iXxDh"><a href="https://www.thomasnet.com/suppliers/usa/sunvisors-95933818">Sunvisors</a><small class="pad-l-2">(32 suppliers)</small></li><li class="browse_categoryListItem__iXxDh"><a href="https://www.thomasnet.com/suppliers/usa/abdominal-back-supporters-81353005">Abdominal &amp; Back Supporters</a><small class="pad-l-2">(29 suppliers)</small></li><li class="browse_categoryListItem__iXxDh"><a href="https://www.thomasnet.com/suppliers/usa/athletic-supporters-81353203">Athletic Supporters</a><small class="pad-l-2">(11 suppliers)</small></li><li class="browse_categoryListItem__iXxDh"><a href="https://www.thomasnet.com/suppliers/usa/collar-supporters-81353401">Collar Supporters</a><small class="pad-l-2">(9 suppliers)</small></li><li class="browse_categoryListItem__iXxDh"><a href="https://www.thomasnet.com/suppliers/usa/massage-tables-96076716">Massage Tables</a><small class="pad-l-2">(18 suppliers)</small></li><li class="browse_categoryListItem__iXxDh"><a href="https://www.thomasnet.com/suppliers/usa/talcum-82672403">Talcum</a><small class="pad-l-2">(7 suppliers)</small></li><li class="browse_categoryListItem__iXxDh"><a href="https://www.thomasnet.com/suppliers/usa/tampons-82691403">Tampons</a><small class="pad-l-2">(36 suppliers)</small></li><li class="browse_categoryListItem__iXxDh"><a href="https://www.thomasnet.com/suppliers/usa/hair-setting-tapes-83625004">Hair Setting Tapes</a><small class="pad-l-2">(6 suppliers)</small></li><li class="browse_categoryListItem__iXxDh"><a href="https://www.thomasnet.com/suppliers/usa/facial-tissue-85861102">Facial Tissue</a><small class="pad-l-2">(169 suppliers)</small></li><li class="browse_categoryListItem__iXxDh"><a href="https://www.thomasnet.com/suppliers/usa/toilet-travel-kits-42032003">Toilet Travel Kits</a><small class="pad-l-2">(31 suppliers)</small></li><li class="browse_categoryListItem__iXxDh"><a href="https://www.thomasnet.com/suppliers/usa/toiletries-85920205">Toiletries</a><small class="pad-l-2">(116 suppliers)</small></li><li class="browse_categoryListItem__iXxDh"><a href="https://www.thomasnet.com/suppliers/usa/toothbrushes-86570462">Toothbrushes</a><small class="pad-l-2">(79 suppliers)</small></li><li class="browse_categoryListItem__iXxDh"><a href="https://www.thomasnet.com/suppliers/usa/toothpaste-86570504">Toothpaste</a><small class="pad-l-2">(78 suppliers)</small></li><li class="browse_categoryListItem__iXxDh"><a href="https://www.thomasnet.com/suppliers/usa/toothpicks-86570603">Toothpicks</a><small class="pad-l-2">(32 suppliers)</small></li><li class="browse_categoryListItem__iXxDh"><a href="https://www.thomasnet.com/suppliers/usa/cosmetic-towelettes-96104245">Cosmetic Towelettes</a><small class="pad-l-2">(20 suppliers)</small></li><li class="browse_categoryListItem__iXxDh"><a href="https://www.thomasnet.com/suppliers/usa/massage-vibrators-91940601">Massage Vibrators</a><small class="pad-l-2">(22 suppliers)</small></li><li class="browse_categoryListItem__iXxDh"><a href="https://www.thomasnet.com/suppliers/usa/foot-warmers-92140201">Foot Warmers</a><small class="pad-l-2">(23 suppliers)</small></li><li class="browse_categoryListItem__iXxDh"><a href="https://www.thomasnet.com/suppliers/usa/wigs-toupees-hair-pieces-94054202">Wigs, Toupees &amp; Hair Pieces</a><small class="pad-l-2">(18 suppliers)</small></li></ol>
"""


# Parse the HTML
soup = BeautifulSoup(html, "html.parser")

# Extract category -> URL mapping
category_url_mapping = {
    a.get_text(strip=True): a["href"]
    for a in soup.find_all("a", href=True)
}

# Format as Python dictionary string
formatted_output = "category_urls = {\n"
for category, url in category_url_mapping.items():
    formatted_output += f'    "{category}": "{url}",\n'
formatted_output += "}"

# Save to text file
with open("category_urls.txt", "w", encoding="utf-8") as f:
    f.write(formatted_output)