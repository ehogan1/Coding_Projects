from datetime import datetime, timedelta

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


start_time = datetime(2023, 1, 31, 3, 0, 0)
end_time = datetime(2023, 2, 5, 21, 30, 0)
time_difference = end_time - start_time
print(start_time, end_time, time_difference.days)