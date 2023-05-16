from datetime import datetime, timedelta

day = '06/01/2019'
dt = datetime.strptime(day, '%d/%m/%Y')
number_days = timedelta(days=dt.weekday()+1)

if number_days.days == 7:
    start = dt
    end = start + timedelta(days=6)
else:
    start = dt - timedelta(days=dt.weekday()+1)
    end = start + timedelta(days=6)

print(start)
print(end)
