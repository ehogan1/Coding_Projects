import csv
import sys

csv_in = str(sys.argv[1])
planned_date = str(sys.argv[2]) # Keep in mind that whatever passes here is getting turned to a string
lstcal = [[]] * 61 # Option to schedule within a 30 day max range of one date
with open(csv_in, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
print(csv_reader)