import csv

INPUT_FILE = "raw.csv"
OUTPUT_FILE = "data.csv"

with open(INPUT_FILE, "r", newline="", encoding="utf-8") as infile, \
     open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        writer.writerow(row[:9])   # Keep first 9 columns
