#task1
import datetime

current_data = datetime.datetime.now()
five_days_ago = current_data - datetime.timedelta(days = 5)
print(five_days_ago)

#task2
import datetime 
today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days=1)
tomorrow = today + datetime
#or
import datetime 
dataa = datetime.datetime.now()
today = dataa.day
yesterday = today - 1
tomorrow = today + 1
print(yesterday, today,tomorrow)

#task3
import datetime 
current_time1 = datetime.datetime.now()
new_data = current_time1.replace(microsecond=0)

print(new_data)

#task4
from datetime import datetime 
date1 = datetime(2023, 10, 25, 12, 0, 0)
date2 = datetime(2023, 10, 20, 10, 30, 0)
difference = (date1 - date2).total_seconds()
print(f'Difference between {date1} and {date2} is {difference} seconds.')