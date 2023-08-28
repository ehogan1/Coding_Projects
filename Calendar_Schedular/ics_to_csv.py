import vobject
import csv
import sys

# def isc_to_csv(csv_out, filename):
filename = str(sys.argv[1])
csv_out = str(sys.argv[2])
with open(csv_out, mode='w') as csv_out:
    csv_writer = csv.writer(csv_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['WHAT', 'FROM', 'TO'])

    # read the data from the file
    data = open(filename).read()
    
    # iterate through the contents
    for cal in vobject.readComponents(data):
        for component in cal.components():
            if component.name == "VEVENT":
                # write to csv
                csv_writer.writerow([component.summary.valueRepr(), \
                                    component.dtstart.valueRepr(), \
                                    component.dtend.valueRepr()])