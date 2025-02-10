import csv

filtered = []
existingDomain = set()
with open('serper/test.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
        if row[2] == 'False':
            continue
        domain = row[1]
        if domain not in existingDomain:
            existingDomain.add(domain)
            filtered.append(row)

with open('serper/test_cleaned.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(filtered)