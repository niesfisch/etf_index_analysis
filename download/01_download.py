import os
import time

import requests
from datetime import datetime, timedelta

# only downloads new data and data in the past

# Create the data directory if it doesn't exist
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, 'data')
os.makedirs(data_dir, exist_ok=True)


# Function to get the last day of the month
def get_last_day_of_month(year, month):
    first_day_of_next_month = datetime(year, month, 1) + timedelta(days=32)
    last_day_of_month = first_day_of_next_month.replace(day=1) - timedelta(days=1)
    return last_day_of_month.strftime('%m%d')


# download json files for each stichtag
for year in range(2008, 2026):
    for month in range(1, 13):
        last_day_of_month = get_last_day_of_month(year, month)
        stichtag = f"{year}{last_day_of_month}"
        # skip if we have not yet reached the month
        if datetime.now() < datetime(year, month, 1):
            print(f"skipping {stichtag} as it is in the future")
            continue

        # if the data already exists, skip it
        if os.path.exists(os.path.join(data_dir, f"{stichtag}.json")):
            print(f"skipping {stichtag} as it already exists")
            continue

        print(f"downloading {stichtag}")
        url = f"https://www.ishares.com/de/privatanleger/de/produkte/251882/ishares-msci-world-ucits-etf-acc-fund/1478358465952.ajax?tab=all&fileType=json&asOfDate={stichtag}&_=1743498789719"
        response = requests.get(url)
        response.raise_for_status()
        with open(os.path.join(data_dir, f"{stichtag}.json"), 'wb') as file:
            file.write(response.content)
        # sleep
        time.sleep(1)
