import requests
import re
import datetime

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.3"
}


def pull() -> str:
    r = requests.get("https://www.espn.com/f1/schedule", headers=headers)
    f = open("test", "w")
    f.write(r.text)
    return r.text


def parse(txt: str):
    inds = [
        m.start()
        for m in re.finditer(
            "http://sports.core.api.espn.pvt/v2/sports/racing/leagues/f1/events", txt
        )
    ]
    events = []
    for ind in inds:
        temp = txt[ind - 300 : ind]
        label = temp.find("label")
        events.append(temp[label + 8 : label + 100])
    events_formatted = {}
    for event in events:
        name_end = event.find(r'"')
        event_name = event[:name_end]
        start = event.find("startDate")
        event_start_time = event[start + 11 : start + 30]
        events_formatted[event_name] = event_start_time
    return events_formatted


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


format(parse(pull()))
