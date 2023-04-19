import sys
import os
from datetime import datetime
import os
import sqlite3
import sys

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

def create_database():
    connection = sqlite3.connect("./images/image_cache.db")
    cur = connection.cursor()

    with open("schema.sql", 'r') as f:
        query = f.read()
        cur.executescript(query)

    connection.commit()
    connection.close()


def get_database_connection():
    conn = sqlite3.connect("./images/image_cache.db")
    conn.row_factory = sqlite3.Row
    return conn

IMAGE_DIR = "./images"
print("Image cache directory: ", sys.path[0] + '\images')

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)
    print("Image cache directory created.")
else:
    print("Image cache directory already exists.")

print("Image cache directory DB: ", sys.path[0] + '\images\image_cache.db')

if not os.path.exists("./images/image_cache.db"): 
    create_database()
    print("Image cache DB created.")
else:
    print("Image cache DB already exists.")
