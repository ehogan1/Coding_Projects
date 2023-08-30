import vobject
import csv
import sys

def isc_to_csv(filename, csv_out):
    with open(csv_out, mode='w') as csv_out:
        csv_writer = csv.writer(csv_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['WHAT', 'FROM', 'TO'])
        data = open(filename).read()
        for cal in vobject.readComponents(data):
            for component in cal.components():
                if component.name == "VEVENT": # If there is an event then write it to the CSV
                    csv_writer.writerow([component.summary.valueRepr(), \
                                        component.dtstart.valueRepr(), \
                                        component.dtend.valueRepr()])

# filename = str(sys.argv[1])
# csv_out = str(sys.argv[2])                    
# isc_to_csv(filename, csv_out)