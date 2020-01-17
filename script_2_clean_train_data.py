import csv

print('--- Cleaning... ---')
with open("E0.csv") as input_csv:
    with open("cleaned.csv", "w", newline='') as out_csv:
        csv_reader = csv.reader(input_csv)
        csv_writer = csv.writer(out_csv)

        for row in csv_reader:
            row = row[1:7]
            csv_writer.writerow(row)
        
print('--- Cleaning complete ---')
