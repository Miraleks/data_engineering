import time

import requests
from datetime import datetime, timedelta

from api_keys import api_key_currencylayer
from file_processing import CSVHandler

base_link = "https://api.currencylayer.com/historical"
source_curr = "UAH"
curr = "USD,EUR"
path_to_file = "./data/currency/eur_uah.json"

start_date = "2023-11-01"
end_date = "2023-11-30"

start = datetime.strptime(start_date, "%Y-%m-%d")
end = datetime.strptime(end_date, "%Y-%m-%d")

csv_handler = CSVHandler(date=start_date)

print(start_date)
current_date = start
while current_date <= end:
    timestamp = current_date.strftime("%Y-%m-%d")

    URL = f"{base_link}?access_key={api_key_currencylayer}&source={source_curr}&currencies={curr}&&date={timestamp}"
    r = requests.get(url=URL)

    result = r.json()

    csv_handler.add_to_file(new_data=result)

    current_date += timedelta(days=1)
    time.sleep(1)  # used to avoid blocking by the API


