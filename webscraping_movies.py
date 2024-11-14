import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
db_name = './data/Movies_Top_50.db'
table_name = 'Top_50'
csv_path = './data/top_50_films.csv'
df = pd.DataFrame(columns=["Average Rank", "Film", "Year", "Rotten Tomatoes' Top 100"])
count = 0

html_page = requests.get(url).text
data = BeautifulSoup(html_page, 'html.parser')

tables = data.find_all('tbody')
rows = tables[0].find_all('tr')

for row in rows:
    if count<50:
        col = row.find_all('td')
        if len(col)!=0:
            data_dict = {"Average Rank": col[0].contents[0],
                         "Film": col[1].contents[0],
                         "Year": (col[2].contents[0]),
                         "Rotten Tomatoes' Top 100": col[3].contents[0]}
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df,df1], ignore_index=True)
            count+=1
    else:
        break

df["Year"] = df["Year"].astype(int)
df = df.astype({"Average Rank": str, "Film": str, "Year": int, "Rotten Tomatoes' Top 100": str})

# print(df.dtypes)
print(df[df["Year"]>=2000])
# print(df)

df.to_csv(csv_path)
#
conn = sqlite3.connect(db_name)
df.to_sql(table_name, conn, if_exists='replace', index=False)
conn.close()