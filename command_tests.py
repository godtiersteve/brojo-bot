import sqlite3
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
from requests_toolbelt.utils import dump

characterName = 'Narmaya'
characterCode = 'NARM'
conn = sqlite3.connect('granblue.db')
cursor = conn.cursor()

cursor.execute('DELETE FROM Characters WHERE characterCode = \'' + characterCode + '\'')

URL = 'http://www.dustloop.com/wiki/api.php'
page = 'GBVS/' + characterName + '/Frame_Data'
PARAMS = {"page":page, "action":"parse", "prop":"text", "format":"json", "formatversion":2, "section":3, "prop":"text" }
#print(page)

r = requests.get(URL, params = PARAMS)
html = r.json()["parse"]["text"]
table_class = "cargoDynamicTable"
#html = r.content

soup = BeautifulSoup(html, "html.parser")
indiatable = soup.find('table', {'class':'cargoDynamicTable'})
df = pd.read_html(str(indiatable))
df = pd.DataFrame(df[0])
df.drop(df.tail(1).index,inplace=True) 
df = df.reset_index()
for index, row in df.iterrows():
    insert = 'INSERT INTO Moves (characterCode, input, damage, guardType, startup, active, recovery, onBlock, onHit, level, invuln, stance, moveType) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    values = (characterCode, row['input'], row['damage'], row['guard'], row['startup'], row['active'], row['recovery'], row['onBlock'], row['onHit'], row['level'], row['invuln'], '', 'Normal Move')
    #print(values)
    cursor.execute(insert,      values)
#print(df.head())

conn.commit()
conn.close()
#print(len(soup.find_all('td', attrs={"class":"details-control"})))
#subs = soup.find('td', {'class':'details-control'}).findChildren()

