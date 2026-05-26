from datetime import datetime

'''def is_time_between(start, end, check):
    fmt = "%H:%M"
    start = datetime.strptime(start, fmt).time()
    end = datetime.strptime(end, fmt).time()
    check = datetime.strptime(check, fmt).time()
    return start <= check <= end

print(is_time_between("10:00", "10:50", "11:30"))  # True'''


##########overnight
def is_time_between(start, end, check):
    fmt = "%H:%M"
    start = datetime.strptime(start, fmt).time()
    end = datetime.strptime(end, fmt).time()
    check = datetime.strptime(check, fmt).time()

    if start <= end:
        return start <= check <= end
    else:
        # crosses midnight
        return check >= start or check <= end

print(is_time_between("10:00", "9:00", "9:30"))  # True
print(is_time_between("22:00", "06:00", "05:30"))  # True
print(is_time_between("22:00", "06:00", "12:00"))  # False
