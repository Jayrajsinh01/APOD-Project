""" 
COMP 593 - Final Project

Description: 
  Downloads NASA's Astronomy Picture of the Day (APOD) from a specified date
  and sets it as the desktop background image.

Usage:
  python apod_desktop.py [apod_date]

Parameters:
  apod_date = APOD date (format: YYYY-MM-DD)
"""
from datetime import datetime
import hashlib
import os
import sqlite3
import sys
import uuid

import requests

import image_lib
import inspect
import apod_api

# Global variables
image_cache_dir = None  # Full path of image cache directory
image_cache_db = None   # Full path of image cache database

def main():
    ## DO NOT CHANGE THIS FUNCTION ##
    # Get the APOD date from the command line
    apod_date = get_apod_date()    

    # Get the path of the directory in which this script resides
    script_dir = get_script_dir()

    # Initialize the image cache
    init_apod_cache(script_dir)

    # Add the APOD for the specified date to the cache
    apod_id = add_apod_to_cache(apod_date)

    # Get the information for the APOD from the DB
    apod_info = get_apod_info(apod_id)

    # Set the APOD as the desktop background image
    if apod_id != 0:
        image_lib.set_desktop_background_image(apod_info['file_path'])

def get_database_connection():
    conn = sqlite3.connect("./images/image_cache.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_apod_date():
    """Gets the APOD date
     
    The APOD date is taken from the first command line parameter.
    Validates that the command line parameter specifies a valid APOD date.
    Prints an error message and exits script if the date is invalid.
    Uses today's date if no date is provided on the command line.

    Returns:
        date: APOD date
    """
    # TODO: Complete function body

    today_date = datetime.today().date()
    last_date = datetime(1995, 6, 16).date()

    if sys.argv[-1] != os.path.basename(__file__): apod_date = sys.argv[-1]
    else: apod_date = today_date

    try:
        apod_date = datetime.fromisoformat(apod_date).date()
        try:
            if apod_date < last_date: 
                raise Exception("Error: APOD date cannot be before 1995-06-16") 
            elif apod_date > today_date: 
                raise Exception("Error: APOD date cannot be in the future")
            else: 
                pass
        except Exception as e: 
            print(str(e))
            sys.exit("Script execution aborted")
    except Exception as e:
        print("Error: Invalid date format; " + str(e))
    
    return apod_date

def get_script_dir():
    """Determines the path of the directory in which this script resides

    Returns:
        str: Full path of the directory in which this script resides
    """
    ## DO NOT CHANGE THIS FUNCTION ##
    script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
    return os.path.dirname(script_path)

def init_apod_cache(parent_dir):
    """Initializes the image cache by:
    - Determining the paths of the image cache directory and database,
    - Creating the image cache directory if it does not already exist,
    - Creating the image cache database if it does not already exist.
    
    The image cache directory is a subdirectory of the specified parent directory.
    The image cache database is a sqlite database located in the image cache directory.

    Args:
        parent_dir (str): Full path of parent directory    
    """
    global image_cache_dir
    global image_cache_db
    # TODO: Determine the path of the image cache directory
    # TODO: Create the image cache directory if it does not already exist
    # TODO: Determine the path of image cache DB
    # TODO: Create the DB if it does not already exist
    
    def create_database():
        connection = sqlite3.connect("./images/image_cache.db")
        cur = connection.cursor()

        with open("schema.sql", 'r') as f:
            query = f.read()
            cur.executescript(query)

        connection.commit()
        connection.close()

    image_dir_name = 'images'
    image_cache_dir = '/'.join([parent_dir, image_dir_name])

    print("Image cache directory: ", image_cache_dir)

    if not os.path.exists(image_cache_dir):
        os.makedirs(image_cache_dir)
        print("Image cache directory created.")
    else:
        print("Image cache directory already exists.")

    image_cache_db = parent_dir + "/images/image_cache.db"
    print("Image cache directory: ", image_cache_db)

    if not os.path.exists(image_cache_db): 
        create_database()
        print("Image cache DB created.")
    else:
        print("Image cache DB already exists.")


def add_apod_to_cache(apod_date):
    """Adds the APOD image from a specified date to the image cache.
     
    The APOD information and image file is downloaded from the NASA API.
    If the APOD is not already in the DB, the image file is saved to the 
    image cache and the APOD information is added to the image cache DB.

    Args:
        apod_date (date): Date of the APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if a new APOD is added to the
        cache successfully or if the APOD already exists in the cache. Zero, if unsuccessful.
    """
    print("APOD date:", apod_date.isoformat())
    # TODO: Download the APOD information from the NASA API
    # TODO: Download the APOD image
    # TODO: Check whether the APOD already exists in the image cache
    # TODO: Save the APOD file to the image cache directory
    # TODO: Add the APOD information to the DB

    apod = apod_api.get_apod_info(apod_date)

    title = apod["title"]
    explanation = apod ["explanation"]
    print(f"APOD title: {title}")

    image_url = apod_api.get_apod_image_url(apod)
    img_path = determine_apod_file_path(title, image_url)
    image_data = image_lib.download_image(image_url)

    if image_data is not None:
        image_hash = hashlib.sha256(image_data).hexdigest()
        print(f"APOD SHA-256: {image_hash}")

    apod_id = get_apod_id_from_db(image_hash)

    if apod_id:
        print("APOD image is already in cache.")
    else:
        print("APOD image is not already in cache.")
        image_lib.save_image_file(image_data, img_path)
        apod_id = add_apod_to_db(title, explanation, img_path, image_hash)
    return apod_id

def add_apod_to_db(title, explanation, file_path, sha256):
    """Adds specified APOD information to the image cache DB.
     
    Args:
        title (str): Title of the APOD image
        explanation (str): Explanation of the APOD image
        file_path (str): Full path of the APOD image file
        sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: The ID of the newly inserted APOD record, if successful.  Zero, if unsuccessful       
    """
    # TODO: Complete function body
    try:
        print("Adding APOD to image cache DB...", end='')
        id = uuid.uuid4().hex

        conn = get_database_connection()
        conn.execute("INSERT INTO apod_data VALUES(?, ?, ?, ?, ?)", (id, title, explanation, file_path, sha256))
        conn.commit()
        conn.close()

        print("success")
        return id

    except Exception as e:
        print(str(e))
        return 0

def get_apod_id_from_db(image_sha256):
    """Gets the record ID of the APOD in the cache having a specified SHA-256 hash value
    
    This function can be used to determine whether a specific image exists in the cache.

    Args:
        image_sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if it exists. Zero, if it does not.
    """
    # TODO: Complete function body
    conn = get_database_connection()

    apod_id = conn.execute("SELECT id FROM apod_data WHERE SHA_hash = ?", (image_sha256,)).fetchone()

    if apod_id:
        return apod_id['id']
    else:
        return 0


def determine_apod_file_path(image_title, image_url):
    """Determines the path at which a newly downloaded APOD image must be 
    saved in the image cache. 
    
    The image file name is constructed as follows:
    - The file extension is taken from the image URL
    - The file name is taken from the image title, where:
        - Leading and trailing spaces are removed
        - Inner spaces are replaced with underscores
        - Characters other than letters, numbers, and underscores are removed

    For example, suppose:
    - The image cache directory path is 'C:\\temp\\APOD'
    - The image URL is 'https://apod.nasa.gov/apod/image/2205/NGC3521LRGBHaAPOD-20.jpg'
    - The image title is ' NGC #3521: Galaxy in a Bubble '

    The image path will be 'C:\\temp\\APOD\\NGC_3521_Galaxy_in_a_Bubble.jpg'

    Args:
        image_title (str): APOD title
        image_url (str): APOD image URL
    
    Returns:
        str: Full path at which the APOD image file must be saved in the image cache directory
    """
    # TODO: Complete function body
    extension = str(image_url).split('.')[-1]
    name = image_title.replace(" ", "_").replace(":", "_") + f".{extension}"

    path = '/'.join([image_cache_dir, name])

    return path


def get_apod_info(image_id):
    """Gets the title, explanation, and full path of the APOD having a specified
    ID from the DB.

    Args:
        image_id (int): ID of APOD in the DB

    Returns:
        dict: Dictionary of APOD information
    """
    # TODO: Query DB for image info
    # TODO: Put information into a dictionary

    conn = get_database_connection()
    data = conn.execute("SELECT title, explanation, img_path FROM apod_data WHERE id = ?", (str(image_id),)).fetchone()
    conn.close()

    apod_info = {
        'title': data["title"], 
        'explanation': data["explanation"],
        'file_path': data["img_path"],
    }
    return apod_info

def get_all_apod_titles():
    """Gets a list of the titles of all APODs in the image cache

    Returns:
        list: Titles of all images in the cache
    """
    # TODO: Complete function body
    # NOTE: This function is only needed to support the APOD viewer GUI
    return

if __name__ == '__main__':
    main()
