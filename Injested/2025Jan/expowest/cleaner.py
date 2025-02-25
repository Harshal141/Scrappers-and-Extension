import csv
import os

# remove values with isRelated column as false 
with open('expowest/DATA_335_expowest_result.csv', 'r') as inp, open('expowest/DATA_335_expowest_result_cleaned.csv', 'w') as out:
    writer = csv.writer(out)
    for row in csv.reader(inp):
        if row[2] == 'True':
            writer.writerow(row)