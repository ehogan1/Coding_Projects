# import email_to_ics
import csv_to_lstcal
from datetime import datetime, timedelta

def combine_days(day1, day2):
    """
    """
    # print("Combining:\n")
    # print(day1, day2)
    # print("\n")
    length = len(day2)
    while length > 2:
        day1 = csv_to_lstcal.add_to_day(day1, day2[1], day2[2])
        day2 = [day2[0]] + day2[3:]
        length -= 2
    # print("Result:\n")
    # print(day1)
    # print("\n")
    return day1

def free_to_busy(avail):
    """
    """
    busy = [-1]
    if avail[0][:5] != "00:00":
        busy.append(0.0)
    for time in avail:
        time = time.strip()
        if time[:5] != "00:00":
            busy.append(int(time[:2]) + (int(time[3:5]) / 60))
        busy.append(int(time[6:8]) + (int(time[9:]) / 60))
    busy.append(24.0)
    busy.append(25)
    return busy

def busy_to_free(busy_times):
    """
    """
    # Invert the busy_times calendar to find the free times
    free_times = []
    for index, day in enumerate(busy_times):
        free_day = []
        if day[1] != 0:
            free_day.append(0)
            free_day.append(day[1])
        for index, time in enumerate(day):
            if not (index)%2 and index != 0:
                free_day.append(time)
                free_day.append(day[(index + 1)])
        if free_day == [24, 25]:
            free_times.append([])
        else:
            free_times.append(free_day[:-2])
    return free_times

def find_times(lstcals, planned_time, flex, availibility = "09:00-17:00", weekends = False):
    """
    """

    # Combine all of the List Calendars to compile a singular list of all busy times
    busy_times = [[] for _ in range(((flex * 2) + 1))]
    for index, day in enumerate(busy_times):
        day = lstcals[0][index]
        for person in lstcals[1:]:
            day = combine_days(day, person[index])
        busy_times[index] = day

    # Add in Unavailible times as busy
    avail = availibility.split(',')
    unavail = free_to_busy(avail)
    for index, day in enumerate(busy_times):
        day = combine_days(day, unavail)
        busy_times[index] = day

    # Invert the busy_times calendar to find the free times
    free_times = busy_to_free(busy_times)

    # Find and trim the weekends if needed
    time = datetime.strptime(planned_time, '%Y-%m-%d %H:%M:%S%z')
    days_until_saturday = (5 - time.weekday()) % 7
    days_until_sunday = (6 - time.weekday()) % 7
    weekend = (flex + days_until_saturday)%7
    # For times when a Sunday is the first day
    if (flex + days_until_sunday) == 7:
        free_times[0] = []
    if weekend >= ((flex * 2) + 1):
        weekend = None
    if not weekends and (weekend or weekend == 0):
        for index, day in enumerate(free_times):
            if (index % 7) == weekend or (index % 7) == (weekend + 1):
                free_times[index] = []

    return free_times