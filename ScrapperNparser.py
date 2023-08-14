# coding: utf-8

from datetime import datetime, timedelta
import time
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
        driver.set_page_load_timeout(20)

        element = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="inner-content"]/div[2]/div[1]/div[3]/div[1]/div/lib-city-history-summary/div/div[2]/table',
                )
            )
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
                    if word in ["--", "-"]:
                        numerical_values.append(None)

        numerical_values.insert(0, current)
        if len(numerical_values) > 34:
            numerical_values = numerical_values[:34]
        #print(current.strftime("%m-%d-%Y"))
        tmp_df = pd.DataFrame([numerical_values], columns=columns)
        df = pd.concat([df, tmp_df], ignore_index=True)
        current += timedelta(days=1)
        time.sleep(5)
        driver.quit()
    return df


def divide_date_range(start_date, end_date, interval_days):
    current_date = start_date
    intervals = []
    while current_date <= end_date:
        interval_end = current_date + timedelta(days=interval_days)
        if interval_end > end_date:
            interval_end = end_date

        intervals.append((current_date, interval_end))
        current_date = interval_end + timedelta(days=1)

    return intervals


if not os.path.exists("Data_ETL"):
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
    "Sea Level Pressure: Actual",
    "Sea Level Pressure: Historic Avg",
    "Sea Level Pressure: Record",
]

df = pd.DataFrame(columns=columns)
cities = [("mumbai", "VABB")]
print("Enter a starting date (MM/DD/YYYY): ")
start_date = input()
print("\nEnter an ending date (MM/DD/YYYY): ")
end_date = input()
print(" ")
for city, station in cities:
    start, end = datetime.strptime(start_date, "%m/%d/%Y"), datetime.strptime(
        end_date, "%m/%d/%Y"
    )
    date_intervals = divide_date_range(start, end, 30)
    n = len(date_intervals)
    for i in range(n):
        print(i," of ",n,' interval processing')
        df = extnparser(
            df, columns, date_intervals[i][0], date_intervals[i][1], city, station
        )
        time.sleep(40)
s = "_"+start.strftime("%m_%d_%Y")+"_"+end.strftime("%m_%d_%Y")
df.to_csv("output{}.csv".format(s), index=False)
