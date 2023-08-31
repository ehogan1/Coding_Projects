import sys
import ics_to_csv
import csv_to_lstcal
import find_times
from datetime import datetime, timedelta
    
def convert(icss, planned_time, flex):
    """
    """
    csvs = []
    lstcals = []
    count = 0
    # for email in emails:
    #     icss.append(email_to_ics.email_to_ics(email))
    for ics_file in icss:
        ics_to_csv.isc_to_csv(ics_file, f"csv{count}")
        csvs.append(f"csv{count}")
        count += 1
    for csv_file in csvs:
        csv, cal_start = csv_to_lstcal.csv_to_lstcal(csv_file, planned_time, flex)
        lstcals.append(csv)
    return lstcals, cal_start

def meeting_times(icss, planned_time, flex):
    """
    """
    gate = False
    lstcals, cal_start = convert(icss, planned_time, flex)
    times = find_times.find_times(lstcals, planned_time, flex)
    print(f"\n\nPOTENTIAL MEETING TIMES\n\n")
    for index, day in enumerate(times):
        if day == []:
            continue
        print(f"On {(cal_start + timedelta(days=index)).date()}, you have  \
                availible meeting times(s) from:")
        for index, hour in enumerate(day):
            # Using a gate to not double print pairs
            if gate:
                continue
            hour = str(hour).split('.')
            next_hour = str(day[(index + 1)]).split('.')
            if len(hour[1]) < 2:
                hour[1] = hour[1] * 10
            if len(next_hour[1]) < 2:
                next_hour[1] = next_hour[1] * 10
            print(f"    {hour[0]}:{hour[1]} - {next_hour[0]}:{next_hour[1]}")
        print('\n')
    return

meeting_times(sys.argv[1], "2023-08-31 12:00:00+00:00", 2)