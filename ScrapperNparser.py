# coding: utf-8

from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import os



def extnparser(current, end, city, station):
    # os.mkdir(station)
    lookup_URL = "https://www.wunderground.com/history/daily/in/{}/{}/date/{}-{}-{}"

    while current != end:
        if start.day == 1:
            print(start)
        formatted_lookup_URL = lookup_URL.format(
            city, station, current.year, current.month, current.day
        )
        print(formatted_lookup_URL)
        print(
            "https://www.wunderground.com/history/daily/in/mumbai/VABB/date/2015-7-31"
        )

        table_data = requests.get(formatted_lookup_URL).content

        print(table_data)

        """soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", class_="ng-star-inserted")

        tbody_sections = table.find_all("tbody")

        def extract_row_values(row):
            pass

        for tbody in tbody_sections:
            rows = tbody.find_all("tr", class_="ng-star-inserted")[1:]
            for r in rows:
                print(r)"""
        break


cities = [("mumbai", "VABB")]
# print("Enter a starting date (MM/DD/YYYY): ")
start_date = "07/31/2015"  # input()
# print("\nEnter an ending date (MM/DD/YYYY): ")
end_date = "07/31/2023"  # input()

for city, station in cities:
    start, end = datetime.strptime(start_date, "%m/%d/%Y"), datetime.strptime(
        end_date, "%m/%d/%Y"
    )
    extnparser(start, end, city, station)
