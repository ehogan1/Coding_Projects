start_time = "07:30"
end_time = "09:30"
day = [-1, 25]

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
        if index == (started + 1) and not (started)%2:
            day.insert(index, end_time)
            break
        if not (index)%2:
            day.insert(index, end_time)
        day = day[:(started + 1)] + day[index:]
print(day)