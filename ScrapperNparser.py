# coding: utf-8

from datetime import datetime, timedelta
import webarchive
import os


def extnparser(current, end, city, station):
    os.mkdir(station)
    lookup_URL = (
        "https://www.wunderground.com/history/daily/in/{}/{}/date/{}-{}-{}.html"
    )

    while current != end:
        if start.day == 1:
            print(start)
        formatted_lookup_URL = lookup_URL.format(
            city, station, current.year, current.month, current.day
        )
        page = pywebarchive(formatted_lookup_URL)
        print(page)
        break


cities = [("mumbai", "VABB")]
print("Enter a starting date (MM/DD/YYYY): ")
start_date = input()
print("\nEnter an ending date (MM/DD/YYYY): ")
end_date = input()

for city, station in cities:
    start, end = datetime.strptime(start_date, "%m/%d/%Y"), datetime.strptime(
        end_date, "%m/%d/%Y"
    )
    extnparser(start, end, city, station)
