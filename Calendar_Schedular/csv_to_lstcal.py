from calendar import day_abbr
import csv
from math import e
from collections import Counter
from datetime import datetime, timedelta
from time import time_ns
from tracemalloc import start


START = -1
END = 25


def same_day(date1, date2):
    """
    """
    date2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S%z')
    return date1.year == date2.year and date1.month == date2.month and date1.day == date2.day


def add_to_day(day, start_time, end_time):
    """
    """
    started, end_placed, start_placed, already = False, False, False, False
    if isinstance(start_time, str):
        start_time = int(start_time[:2]) + (int(start_time[3:]) / 60) # Making the time a decimal
    if isinstance(end_time, str):
        end_time = int(end_time[:2]) + (int(end_time[3:]) / 60)
    for index, time in enumerate(day): # Creating the Time Pairs
        if start_time <= time and not started:
            if (index)%2 and start_time != day[index - 1]:
                day.insert(index, start_time)
                start_placed = True
            started = index
        if end_time <= time and started:
            if index == (started) and (started)%2:
                day.insert((index + 1), end_time)
                break
            if not (index)%2:
                day.insert(index, end_time)
                end_placed = True
            # Checking what to cut out depending on how much was added and how
            # many we skipped between placing the start and end number
            if time == 25 and already:
                continue
            if start_placed:
                day = day[:(started + 1)] + day[(index):]
            else:
                day = day[:(started)] + day[(index):]
            if time == 25:
                already = True
            break
    element_counts = Counter(day)
    day = [element for element, count in element_counts.items() if count == 1]
    return day


def csv_to_lstcal(csv_in, planned_time, flex):
    """
    """
    lstcal = [[START, END] for _ in range(((flex * 2) + 1))] # Option to schedule within a 30 day max range of one date
    with open(csv_in, 'r') as csv_in:
        csv_reader = csv.reader(csv_in)

        # Finding the Date Range
        date = datetime.strptime(planned_time, '%Y-%m-%d %H:%M:%S%z')
        cal_start = date - timedelta(days=flex)
        cal_end = date + timedelta(days=flex)

        # Iterating Through each Event in the Calendar
        day_count = 0
        current_day = None
        for index, row in enumerate(csv_reader):
            if not index:
                continue
            start_date = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S%z')
            end_date = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S%z')
            if start_date < cal_start or end_date > cal_end:
                continue
            if current_day:
                if not same_day(current_day, row[1]):
                    day_count = ((datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S%z')).date() - cal_start.date()).days # making positve???
                    current_day = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S%z')
                lstcal[day_count] = add_to_day(lstcal[day_count], row[1][11:16], row[2][11:16])
            else:
                day_count = ((datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S%z')).date() - cal_start.date()).days
                lstcal[day_count] = add_to_day(lstcal[day_count], row[1][11:16], row[2][11:16])
                current_day = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S%z')
    return lstcal, cal_start


# csv_in = str(sys.argv[1])
# planned_time = str(sys.argv[2]) # Keep in mind that whatever passes here is getting turned to a string
# test = csv_to_lstcal(csv_in, planned_time)
# for day in test:
#     if day == [-1, 25]:
#         print("NO EVENT\n")
#     else:
#         print(day)
