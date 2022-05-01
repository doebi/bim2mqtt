import requests
import datetime
from urllib.parse import urlencode
from lxml import etree

url = "http://www.linzag.at/static/XML_DM_REQUEST"
lines = ["4:0", "4:1", "4:2", "4:3", "5:0", "5:1"]
stopID = "60500150" # Untergaumberg
stopID = "60501720" # Hauptbahnhof

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
    sid = getSession(stopID)
    data = {
        "sessionID": sid,
        "requestID": 1,
        "dmLineSelectionAll": 1,
        "command": "dmNext"
    }


    #"itdDateTimeDepArr": "dep",
    #"dmLineSelection": "all",
    #"dmLineSelection": "4:0"
    #datastring = urlencode(data)

    #for l in lines:
    #    datastring += "&dmLineSelection=" + l

    r = requests.get(url, data)
    print(r.text)
    data = etree.fromstring(r.content)
    dm_request = data[-1]
    departure_list = dm_request[-1]

    #print(departure_list)
    #now = datetime.strptime(data.get('now'), "%Y-%m-%dT%H:%M:%S")
    #print(now)


getDeparture(stopID)
