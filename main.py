import sys
import os
from datetime import datetime

today_date = datetime.today().date()
last_date = datetime(1995, 6, 16).date()

if sys.argv[-1] != os.path.basename(__file__): 
    date = sys.argv[-1]
else: 
    date = str(today_date)

try:
    obj = datetime.fromisoformat(date).date()
    try:
        if obj < last_date: 
            raise Exception("Error: APOD date cannot be before 1995-06-16") 
        elif obj > today_date: 
            raise Exception("Error: APOD date cannot be in the future")
        else: 
            pass
    except Exception as e: 
        print(str(e))
        sys.exit("Script execution aborted")
except Exception as e:
    print("Error: Invalid date format; " + str(e))
    sys.exit("Script execution aborted")
