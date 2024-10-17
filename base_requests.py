import requests

from api_keys import api_key_currencylayer

base_link = "http://api.currencylayer.com/change"
curr = "USD,EUR"
start_date = "2024-10-14"
end_date = "2024-10-14"
path_to_file = "./data/currency/eur_uah.json"
source_curr = "UAH"

URL = f"{base_link}?access_key={api_key_currencylayer}&source={source_curr}&currencies={curr}&&start_date={start_date}&end_date={end_date}"

r = requests.get(url=URL)

result = r.json()  # dict

# append_to_json_file(path_to_file, result)
print(result.get("quotes").get("UAHUSD"))
