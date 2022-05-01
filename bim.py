import requests
import schedule
import time
from datetime import datetime
from urllib.parse import urlencode
from lxml import etree
from collections import deque

url = "https://www.linzag.at/static/XML_DM_REQUEST"
stopID = "60500150" # Untergaumberg

departures = deque()


def getSession(stopID):
    data = {
        "sessionID": "0",
        "type_dm": "stopID",
        "name_dm": stopID,
    }
    r = requests.get(url, data)
    data = etree.fromstring(r.content)
    sid = data.get('sessionID')
    return sid


def getDeparture(stopID):
    print("getDeparture")

    result = deque()
    sid = getSession(stopID)
    data = {
        "sessionID": sid,
        "request": "1",
        "dmLineSelectionAll": "1",
    }

    #"itdDateTimeDepArr": "dep",
    #"dmLineSelection": "all",
    #datastring = urlencode(data)

    #for l in lines:
    #    datastring += "&dmLineSelection=" + l

    r = requests.get(url, data)
    data = etree.fromstring(r.content)
    now = datetime.strptime(data.get('now'), "%Y-%m-%dT%H:%M:%S")
    dm_request = data[-1]
    departure_list = dm_request[-1]

    for d in departure_list:
        datetimeobj = d[0]
        dateobj = datetimeobj[0]
        timeobj = datetimeobj[1]

        deptimestring = "%s-%s-%sT%s:%s:%s" %(dateobj.get('year'), dateobj.get('month'), dateobj.get('day'), timeobj.get('hour'), timeobj.get('minute'), '0')

        dep = datetime.strptime(deptimestring, "%Y-%m-%dT%H:%M:%S")
        result.append(dep)
    return result


def update():
    global departures
    print("update")
    now = datetime.now().replace(microsecond=0)

    if (len(departures) == 0):
        departures = getDeparture(stopID)

    next_departure = departures[0]

    if (next_departure < now):
        departures.popleft()

    delta = next_departure - now
    print(delta)

schedule.every(1).seconds.do(update)

while True:
    schedule.run_pending()
    time.sleep(1)
