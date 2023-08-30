from datetime import datetime, timedelta
# import email_to_ics
import ics_to_csv
import csv_to_lstcal
from find_times import combine_days, busy_to_free, free_to_busy

# start_time = "07:15"
# end_time = "15:45"
# day = [-1, 5, 8, 14, 16.5, 25]

# started, ended = False, False
# start_time = int(start_time[:2]) + (int(start_time[3:]) / 60) # Making the time a decimal
# end_time = int(end_time[:2]) + (int(end_time[3:]) / 60)
# for index, time in enumerate(day): # Creating the Time Pairs
#     if start_time < time and not started:
#         if (index)%2:
#             day.insert(index, start_time)
#         started = index
#         continue
#     if end_time < time and started:
#         if index == (started + 1) and (started)%2:
#             day.insert(index, end_time)
#             break
#         if (index)%2:
#             day.insert(index, end_time)
#         if (started)%2:
#             day = day[:(started + 1)] + day[(index + 1):]
#         else:
#             day = day[:(started)] + day[(index):]
#         break
# print(day)


# start_time = datetime(2023, 1, 31, 3, 0, 0)
# end_time = datetime(2023, 2, 5, 21, 30, 0)
# time_difference = end_time - start_time
# print(start_time, end_time, time_difference.days)

# def check(x):
#     if isinstance(x, str):
#         print("x is string")
#     if isinstance(x, int):
#         print("x is int")
#     return
# x = 12
# check(x)

# test = [[], [], [], [], [], []]
# x = 0
# for lis in test:
#     lis = [x]
# print(test)

        # availibility = "09:00-17:00"
        # weekends = True
        # planned_time = "2023-08-31 12:00:00+00:00"
        # flex = 2


        # # Missing when there is more than one event in the day
        # lstcals = [[[-1, 7, 9, 14, 20, 25], [-1, 8, 13, 25], [-1, 5, 9, 10, 23, 25], [-1, 10, 14, 25], [-1, 3, 6, 18, 22, 25]],
        #             [[-1, 9, 12, 14, 16, 25], [-1, 5, 10, 12, 16, 25], [-1, 10, 15, 25], [-1, 9, 12, 15, 19, 25], [-1, 5, 10, 25]],
        #             [[-1, 15, 21, 25], [-1, 5, 14, 25], [-1, 12, 15, 17, 24, 25], [-1, 7, 16, 25], [-1, 3, 6, 12, 17, 25]]]

        # # Combine all of the List Calendars to compile a singular list of all busy times
        # busy_times = [[] for _ in range(((flex * 2) + 1))]
        # for index, day in enumerate(busy_times):
        #     day = lstcals[0][index]
        #     for person in lstcals[1:]:
        #         day = combine_days(day, person[index])
        #     busy_times[index] = day

        # # Add in Unavailible times as busy
        # avail = availibility.split(',')
        # unavail = free_to_busy(avail)
        # for index, day in enumerate(busy_times):
        #     day = combine_days(day, unavail)
        #     busy_times[index] = day

        # # Invert the busy_times calendar to find the free times
        # free_times = busy_to_free(busy_times)

        # # Find and trim the weekends if needed
        # time = datetime.strptime(planned_time, '%Y-%m-%d %H:%M:%S%z')
        # days_until_saturday = (5 - time.weekday()) % 7
        # weekend = (flex + days_until_saturday)%7
        # if weekend >= ((flex * 2) + 1):
        #     weekend = None
        # if not weekends and weekend:
        #     for index, day in free_times:
        #         if (index % 7) == weekend or (index % 7) == (weekend + 1):
        #             free_times[index] = []

        # print(free_times)


day1 = [-1, 5, 9, 10, 23, 25]
day2 = [-1, 12, 15, 17, 24, 25]

def combine_days(day1, day2):
    """
    """
    length = len(day2)
    while length > 2:
        print(day1, day2[1], day2[2])
        day1 = csv_to_lstcal.add_to_day(day1, day2[1], day2[2])
        day2 = [day2[0]] + day2[3:]
        length -= 2
    return day1

print(combine_days(day1, day2))