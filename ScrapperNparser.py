# coding: utf-8

from datetime import datetime, timedelta
import csv
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def extnparser(df, columns, current, end, city, station):
    while current != end:
        lookup_URL = "https://www.wunderground.com/history/daily/in/{}/{}/date/{}-{}-{}"

        formatted_lookup_URL = lookup_URL.format(
            city, station, current.year, current.month, current.day
        )
        chromeProfile = webdriver.ChromeOptions()

        chrome_prefs = {
            "profile.default_content_setting_values": {"images": 2, "stylesheet": 2}
        }
        chromeProfile.add_experimental_option("prefs", chrome_prefs)

        driver = webdriver.Chrome(options=chromeProfile)
        driver.get(formatted_lookup_URL)

        element = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.TAG_NAME, "table"))
        )

        data = element.text
        lines = data.split("\n")
        numerical_values = []
        first_24 = False

        for line in lines:
            words = line.split()
            for word in words:
                try:
                    value = float(word)

                    if word == "24" and not first_24 and words[0] == "Precipitation":
                        first_24 = True
                    else:
                        numerical_values.append(value)
                except ValueError:
                    # Handle the case of '--' and '-' (null values)
                    if word in ["--", "-"]:
                        numerical_values.append(None)

        numerical_values.insert(0, current)
        tmp_df = pd.DataFrame([numerical_values], columns=columns)
        df = pd.append([df, tmp_df], ignore_index=True)
        current += timedelta(days=1)


os.mkdir("Data_ETL")
columns = [
    "Date",
    "High Temp: Actual",
    "High Temp: Historic Avg",
    "High Temp: Record",
    "Low Temp: Actual",
    "Low Temp: Historic Avg",
    "Low Temp: Record",
    "Day Average Temp: Actual",
    "Day Average Temp: Historic Avg",
    "Day Average Temp: Record",
    "Precipitation (past 24 hours from 00:10:00): Actual",
    "Precipitation (past 24 hours from 00:10:00): Historic Avg",
    "Precipitation (past 24 hours from 00:10:00): Record",
    "Dew Point: Actual",
    "Dew Point: Historic Avg",
    "Dew Point: Record",
    "High: Actual",
    "High: Historic Avg",
    "High: Record",
    "Low: Actual",
    "Low: Historic Avg",
    "Low: Record",
    "Average: Actual",
    "Average: Historic Avg",
    "Average: Record",
    "Max Wind Speed: Actual",
    "Max Wind Speed: Historic Avg",
    "Max Wind Speed: Record",
    "Visibility: Actual",
    "Visibility: Historic Avg",
    "Visibility: Record",
    " Sea Level Pressure: Actual",
    "Sea Level Pressure: Historic Avg",
    "Sea Level Pressure: Record",
]

df = pd.DataFrame(columns=columns)
cities = [("mumbai", "VABB")]
print("Enter a starting date (MM/DD/YYYY): ")
start_date = input()
print("\nEnter an ending date (MM/DD/YYYY): ")
end_date = input()

for city, station in cities:
    start, end = datetime.strptime(start_date, "%m/%d/%Y"), datetime.strptime(
        end_date, "%m/%d/%Y"
    )
    extnparser(df, columns, start, end, city, station)


print(df.head())
df.to_csv("output.csv", index=False)
