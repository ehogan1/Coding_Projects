import vobject
import csv

with open('sample.csv', mode='w') as csv_out:
    csv_writer = csv.writer(csv_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['WHAT', 'WHO', 'FROM', 'TO', 'DESCRIPTION'])

    # read the data from the file
    data = open("sample.ics").read()

    # iterate through the contents
    for cal in vobject.readComponents(data):
        for component in cal.components():
            if component.name == "VEVENT":
                # write to csv
                csv_writer.writerow([component.summary.valueRepr(),component.attendee.valueRepr(),component.dtstart.valueRepr(),component.dtend.valueRepr(),component.description.valueRepr()])