import csv
import sys
from datetime import datetime, timedelta

csv_in = str(sys.argv[1])
planned_time = str(sys.argv[2]) # Keep in mind that whatever passes here is getting turned to a string
START = -1
END = 25


def same_day(date1, date2):
    date2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S%z')
    return (
        date1.year == date2.year and
        date1.month == date2.month and
        date1.day == date2.day
    )


def add_to_day(day, start_time, end_time)
    """
    Check Phone Notes
    """
    started, ended = False, False
    start_time = int(start_time[:2]) + (int(start_time[3:]) / 60) # Making the time a decimal
    end_time = int(end_time[:2]) + (int(end_time[3:]) / 60)
    for index, time in enumerate(day): # Creating the Time Pairs
        if start_time < time and not started:
            if (index)%2:
                day.insert(index, start_time)
            started = index
            continue
        if end_time < time and started:
            if index = (started + 1) and not (started)%2:
                day.insert(index, end_time)
                break
            if not (index)%2:
                day.insert(index, end_time)
            day = day[:(started + 1)] + day[index:]
    return day


def csv_to_lstcal(csv_in, planned_time)
    """
    """
    lstcal = [[START, END]] * 61 # Option to schedule within a 30 day max range of one date
    with open(csv_in, 'r') as csv_in:
        csv_reader = csv.reader(csv_in)

    # Finding the Date Range
    date = datetime.strptime(planned_time, '%Y-%m-%d %H:%M:%S%z')
    cal_start = date - timedelta(days=30)
    cal_end = date + timedelta(days=30)
    next(csv_reader)

    # Iterating Through each Event in the Calendar
    day_count = 0
    current_day = None
    for row in csv_reader:
        if row[1] < cal_start or row[2] > cal_end:
            break
        if current_day:
            if not same_day(current_day, row[1]):
                day_count += 1
                current_day = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S%z')
            lstcal[day_count] = add_to_day(lstcal[day_count], row[1][11:16], row[2][11:16])       
        else:
            lstcal[0] = add_to_day(lstcal[0], row[1], row[2])
            current_day = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S%z')
    return lstcal