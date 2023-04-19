'''
Library for interacting with NASA's Astronomy Picture of the Day API.
'''
import http
import json
import re
import image_lib
import nasapy
import sys


def main():
    # TODO: Add code to test the functions in this module
    return

def get_apod_info(apod_date):
    """Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    Args:
        apod_date (date): APOD date (Can also be a string formatted as YYYY-MM-DD)

    Returns:
        dict: Dictionary of APOD info, if successful. None if unsuccessful
    """
    apod_date = apod_date.isoformat()
    print(f"Getting {apod_date} APOD information from NASA...", end='')
    # try:
    with open('api.txt', 'r') as f:
        api_key = f.read()

    nasa = nasapy.Nasa(key=api_key)
    apod = nasa.picture_of_the_day(date=apod_date)

    print("success")
    return apod
    # except Exception as e:
    #     print(str(e))
    #     sys.exit("Process aborted.")
        # return

def get_apod_image_url(apod):
    """Gets the URL of the APOD image from the dictionary of APOD information.

    If the APOD is an image, gets the URL of the high definition image.
    If the APOD is a video, gets the URL of the video thumbnail.

    Args:
        apod_info_dict (dict): Dictionary of APOD info from API

    Returns:
        str: APOD image URL
    """
    if apod["media_type"] == "image":
        
        return apod["hdurl"]
        
    elif apod["media_type"] == "video":  
        
        img_url = apod["url"]

        if "youtube" in img_url or "youtu.be" in img_url:
            youtube_id_regex = re.compile("(?:(?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)")
            video_id = youtube_id_regex.findall(img_url)
            video_id = ''.join(''.join(elements) for elements in video_id).replace("?", "").replace("&", "")
            video_thumb = "https://img.youtube.com/vi/" + video_id + "/0.jpg"

        elif "vimeo" in img_url:
            # get ID from Vimeo URL
            vimeo_id_regex = re.compile("(?:/video/)(\d+)")
            vimeo_id = vimeo_id_regex.findall(img_url)[0]
            # make an API call to get thumbnail URL
            vimeo_request = http.request("GET", "https://vimeo.com/api/v2/video/" + vimeo_id + ".json")
            data = json.loads(vimeo_request.data.decode('utf-8'))
            video_thumb = data[0]['thumbnail_large']

        else:
            video_thumb = ""

        return video_thumb
    else:
        return


if __name__ == '__main__':
    main()
