import csv

done = [
    "iicag.com", "sartoricheese.com", "talmera.com", "grassland.com", "cabotcreamery.com",
    "milkspecialties.com", "highdesertmilk.com", "oatkamilk.com", "organicvalley.com", "apsbiogroup.com",
    "hilmarcheese.com", "jfarrell.com", "landolakes.com", "uda.coop", "glanbianutritionals.com",
    "schreiberfoods.com", "hoogwegtus.com", "agrimarkwheyproteins.com", "eriefoods.com", "hphood.com",
    "cmingredients.com", "mctdairies.com", "jacoby.com", "valleymilkca.com", "tedfordtellico.com",
    "burtlewisingredients.com", "belgioioso.com", "tropicalfoodsllc.com", "leprinofoods.com", "darigold.com",
    "agropur.com", "mitsui.com", "proliantinc.com", "firstdistrict.com", "dfamilk.com",
    "interrainternational.com", "prairiefarms.com", "orangecheeseusa.com", "schumancheese.com", "sargento.com",
    "grande.com", "liusa.com", "tillamook.com", "fayrefieldfoodsusa.com", "saputo.com",
    "californiadairies.com", "ampi.com", "idahomilkproducts.com", "agridairy.com", "bongards.com",
    "alouettefoodservice.com", "renardscheese.com", "vqcheese.com", "interfood.com"
]

# Read the input CSV
with open("workshop/usdairy/suppliers.csv", "r") as infile:
    reader = csv.reader(infile)
    lines = list(reader)

# Write to output CSV excluding done domains
with open("workshop/usdairy/pending.csv", "w", newline='') as outfile:
    writer = csv.writer(outfile)
    
    # If there's a header, write it first
    writer.writerow(lines[0])

    for line in lines[1:]:  # Skip header row
        domain = line[1].strip()  # Remove any leading/trailing spaces
        if domain in done:
            print(f"Skipped: {domain}")
            continue
        writer.writerow(line)

print("Done ✅")
