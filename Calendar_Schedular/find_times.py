import email_to_ics
import ics_to_csv
import csv_to_lstcal

def convert(emails, planned_time, flex):
    """
    """
    ics = []
    csv = []
    lstcals = []
    for email in emails:
        ics.append(email_to_ics.email_to_ics(email))
    for ics_file in ics:
        csv.append(ics_to_csv.isc_to_csv(ics_file))
    for csv_file in csv:
        lstcals.append(csv_to_lstcal.csv_to_lstcal(csv_file, planned_time, flex))
    return lstcals

def combine_days(day1, day2):
    """
    """
    length = len(day2)
    while length > 2:
        day1 = csv_to_lstcal.add_to_day(day1, day2[1:3])
        day2 = [day2[0]] + day2[3:]
        length -= 2
    return day1

def find_times(avaibalility, weekends, emails, planned_time, flex):

    # Converting the emails provided into workable List Calendars
    lstcals = convert(emails, planned_time, flex)

    # Combine all of the List Calendars to compile a singular list of all busy times
    busy_times = [[] for _ in range(((flex * 2) + 1))]
    for index, day in enumerate(busy_times):
        day = lstcals[0][index]
        for person in lstcals[1:]:
            day = combine_days(day, person[index])
        busy_times[index] = day

    # Invert the busy_times calendar to find the free times


    # Trim the free times to the specified guidelines


    return []