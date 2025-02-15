import requests
from unidecode import unidecode
import json
import datetime
import re

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.3"
}


def pull():
    reqs = []
    for i in range(16):
        reqs.append(
            requests.get(
                f"https://www.espn.com/f1/race/_/id/{600052045 + i}", headers=headers
            ).text
        )
    for i in range(8):
        reqs.append(
            requests.get(
                f"https://www.espn.com/f1/race/_/id/{600052101 + i}", headers=headers
            ).text
        )
    return reqs


def parse(txts):
    with open("text2.txt","w") as f:
        f.write(txts[0])
    pattern = re.compile(r'\D\D\D,\s\D+\s\d+(th|st|nd|rd)\sat\s\d+:\d\d\s\D\D')
    dates = []
    types = ['fp1','fp2','fp3','q','r']
    stypes = ['fp1','ss','sr','q','r']
    race_name_pattern = re.compile(r'(?<!\d)[\D\s]+\sGrand\sPrix')
    for txt in txts:
        txt = unidecode(txt)
        temp_match = pattern.finditer(txt)
        matches = [m.group(0) for m in temp_match]
        race_name = race_name_pattern.search(txt).group(0)
        if re.findall(r'Sprint',txt):
            temp_races = dict(zip(stypes,matches))
        else:
            temp_races = dict(zip(types,matches))
        temp_races['name'] = race_name
        dates.append(temp_races)
    with open('out.json','w') as f:
        json.dump(dates,f)

def format(events: dict):
    names = list(events.keys())
    times = events.values()
    dates = []
    for time in times:
        date = datetime.date(int(time[1:5]), int(time[6:8]), int(time[9:11]))
        date += datetime.timedelta(days=2)
        dates.append(date)
    for i in range(len(names)):
        print(f"{names[i]} on {dates[i]}")


parse(pull())
