from datetime import datetime, timedelta
import time

def next_weekday(d, weekday):  # 0 = Monday, 1=Tuesday, 2=Wednesday...
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + timedelta(days_ahead)

now = datetime.now()
n = "%s/%s/%s" % (now.month, now.day, now.year)
N = time.strptime(n, "%m/%d/%Y")
std = now + timedelta(days=90)
STD = "%s/%s/%s" % (std.month, std.day, std.year)
s = time.strptime(STD, "%m/%d/%Y")
print STD

we = next_weekday(datetime.today(), 2)
WE = "%s/%s/%s" % (we.month, we.day, we.year)
date = "1/31/2018"
newdate1 = time.strptime(date, "%m/%d/%Y")
print newdate1 <= N
print date == WE