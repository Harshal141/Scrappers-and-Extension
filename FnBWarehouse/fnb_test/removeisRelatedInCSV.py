import csv

with open("fnbWarehouse/fnb_test/fnb_scrapped_ai.csv", "r") as file:
    reader = csv.reader(file)
    lines = list(reader)
    # // remove ones that are areRelated as false, and save it to a new file
    with open("fnbWarehouse/fnb_test/fnb_scrapped_ai_no_isRelated.csv", "w") as file:
        writer = csv.writer(file)
        for line in lines:
            if line[2] == "True":
                writer.writerow(line)
            else:
                continue