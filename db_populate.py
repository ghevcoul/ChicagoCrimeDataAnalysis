#!flask/bin/python
import datetime

import requests

from app import db
from app.models import Chicago
from config import APP_TOKEN

# Values used throughout
url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json"
fields = ["arrest", "beat", "block", "case_number", "community_area", "date", "description", "district", "domestic", "id", "iucr", "latitude", "longitude", "location_description", "primary_type", "updated_on", "ward", "year"]
dlLimit = 50000

def get_data(offset):
    """
    Download the data from the City of Chicago website.
    Returns a list of dicts containing data for each row.
    """
    query = [
        url, "?",
        "$where=year>=2005", 
        "&$order=date", 
        "&$select=",
        ",".join(fields), 
        "&$limit={0}".format(dlLimit),
        "&$offset={0}".format(offset)
    ]
    r = requests.get("".join(query), headers={"X-App-Token":APP_TOKEN})
    return r.json()

def clean_data(d):
    """
    Takes the dict of data from the website. Inserts Nones for any missing values, splits the date field into separate date and time columns, and determines the weekday.
    Returns a new dictionary.
    """
    x = {}
    for i in fields:
        if i in d:
            if d[i] != "" and d[i] != " ":
                x[i] = d[i]
            else:
                x[i] = None
        else:
            x[i] = None
    
    dt = d["date"]
    x["date"] = datetime.date(int(dt[:4]), int(dt[5:7]), int(dt[8:10]))
    x["time"] = datetime.time(int(dt[11:13]), int(dt[14:16]), int(dt[17:19]))
    x["weekday"] = x["date"].strftime("%A")
    return x

def write_data(d):
    """
    Takes a list of dicts and calls clean_data() on each dict before writing it to the database.
    """
    for i in d:
        j = clean_data(i)
        crime = Chicago(id=j["id"],
                        case_number=j["case_number"],
                        date=j["date"],
                        time=j["time"],
                        block=j["block"],
                        iucr=j["iucr"],
                        primary_type=j["primary_type"],
                        description=j["description"],
                        location_description=j["location_description"],
                        arrest=j["arrest"],
                        domestic=j["domestic"],
                        beat=j["beat"],
                        district=j["district"],
                        ward=j["ward"],
                        community_area=j["community_area"],
                        year=j["year"],
                        updated_on=j["updated_on"],
                        latitude=j["latitude"],
                        longitude=j["longitude"],
                        weekday=j["weekday"])
        db.session.add(crime)
        db.session.commit()

if __name__ == "__main__":
    offset = 0
    while True:
        print("Downloading values...")
        dat = get_data(offset)
        if len(dat) > 0:
            print("Got data up to {}".format(dat[-1]["date"]))
            write_data(dat)
        else:
            break
        offset += dlLimit
