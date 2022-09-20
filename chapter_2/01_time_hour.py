import time

# UTC offset for my local time
# (US Eastern Daylight Time)
utc_offset_hours = -4
seconds_per_hour = 3600
seconds_per_day = seconds_per_hour * 24  # 86,400

unix_time = time.time()
utc_time_of_day_seconds = unix_time % seconds_per_day
utc_time_of_day_hours = (
    utc_time_of_day_seconds / seconds_per_hour)
local_time_of_day_hours = (
    utc_time_of_day_hours + utc_offset_hours)
local_hour = int(local_time_of_day_hours)

print("local hour:", local_hour)
