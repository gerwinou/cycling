import requests
import configparser
from datetime import datetime
import os.path
import logging
import logging.config
import json
import csv
import base64

# TODO: - generalize requests
# TODO: - handle refresh action; reset the AT en RT within

# Make sure locales have been exported correctly:
# export LC_ALL=en_US.UTF-8
# export LANG=en_US.UTF-8




logging.config.fileConfig('fitbitlogging.conf')
logger = logging.getLogger('fitbitClient')

propfile = "/Users/gb/fitbit.properties"
tokenfile = "/Users/gb/fitbittokens.properties"

# Read in the config file.
props = configparser.ConfigParser()
props.read(propfile)

config = configparser.ConfigParser()
config.read(tokenfile)

logger.debug("Configfile to be used: " + propfile)
logger.debug("tokenfile to be used: " + tokenfile)

at = config.get('general', 'at')
rt = config.get('general', 'rt')

username = props.get('oauth2','clientID')
password = props.get('oauth2','clientSecret')

authHeader = base64.b64encode(username + ':' + password)

def resetValue():
    # auth=HTTPBasicAuth('user', 'pass')

    headers = {'Authorization': 'Basic ' + authHeader,
               'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'refresh_token',
            'refresh_token': rt}
    url = "https://api.fitbit.com/oauth2/token"

    r = requests.post(url, data=data, headers=headers)
    logger.debug(r.status_code)
    logger.debug(r.text)

    j = json.loads(r.text)
    newAT = j['access_token']
    newRT = j['refresh_token']
    expiry = j['expires_in']

    logger.debug(newAT)
    logger.debug(newRT)

    newConfig = configparser.ConfigParser()
    newConfig.add_section('general')
    newConfig.set('general', 'at', newAT)
    newConfig.set('general', 'rt', newRT)

    with open(tokenfile, 'w') as f:
        newConfig.write(f)


def testAccess():

    accesstoken = at
    headers = {'Authorization': 'Bearer ' + accesstoken}
    url = 'https://api.fitbit.com/1/user/-/profile.json'

    r = requests.get(url, headers=headers)
    logger.debug(r.status_code)
    if(r.status_code != 200):
        if(r.status_code == 401):
            logger.debug("AT has expired")
            resetValue()
        else:
            logger.warn("Some error has occurred, aborting")
            logger.debug(r.status_code)
            exit()
    j = json.loads(r.text)

def getHeartbeat():
    'gets todays heartbeat'
    accesstoken = at
    headers = {'Authorization': 'Bearer ' + accesstoken}
    url = 'https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json'

    r = requests.get(url, headers=headers)
    logger.debug(r.status_code)
    j = json.loads(r.text)

    logger.debug(j)

def getHeartbeatS(s,e):

    outfile = props.get('output','hrfile')

    sep = ":"
    # accessToken = at
    # headers = {'Authorization': 'Bearer ' + accesstoken}
    headers = {'Authorization': 'Bearer ' + at}
    reqUrl = 'https://api.fitbit.com/1/user/-/activities/heart/date/' + s + '/' + e + '.json'

    r = requests.get(reqUrl, headers=headers)
    logger.debug(r.status_code)
    #return json.loads(r.text)
    #return r.text
    a = json.loads(r.text)
    logger.debug(a)

    lengte = len(a["activities-heart"])

    dt  = "NV"
    rhr = "NV"
    #zone0_name = "Out of Range"
    zone0_caloriesOut = "NV"
    zone0_minutes = "NV"

    #zone0_name = "Fat Burn"
    zone1_caloriesOut = "NV"
    zone1_minutes = "NV"

    #zone0_name = "Cardio"
    zone2_caloriesOut = "NV"
    zone2_minutes = "NV"

    #zone0_name = "Peak"
    zone3_caloriesOut = "NV"
    zone3_minutes = "NV"

    with open(outfile,'wb') as csvfile:
        fieldnames = ['date','resthr','zone0Cal','zone0Min','zone0Cal','zone1Cal','zone1Min','zone2Cal','zone2Min','zone3Cal','zone3Min']
        writer = csv.writer(csvfile,delimiter=sep)
        writer.writerow(fieldnames)
        for i in range(lengte):
            dt  = a["activities-heart"][i]["dateTime"]

            try:
                rhr = a["activities-heart"][i]['value']["restingHeartRate"]
            except KeyError as e:
                logger.debug(e)

            try:
                zone0_caloriesOut = int(a["activities-heart"][i]["value"]["heartRateZones"][0]["caloriesOut"])
            except KeyError as e:
                logger.debug(e)

            try:
                zone0_minutes = a["activities-heart"][i]["value"]["heartRateZones"][0]["minutes"]
            except KeyError as e:
                logger.debug(e)

            try:
                zone1_caloriesOut = int(a["activities-heart"][i]["value"]["heartRateZones"][1]["caloriesOut"])
            except KeyError as e:
                logger.debug(e)

            try:
                zone1_minutes = a["activities-heart"][i]["value"]["heartRateZones"][1]["minutes"]
            except KeyError as e:
                logger.debug(e)

            try:
                zone2_caloriesOut = int(a["activities-heart"][i]["value"]["heartRateZones"][2]["caloriesOut"])
            except KeyError as e:
                logger.debug(e)

            try:
                zone2_minutes = a["activities-heart"][i]["value"]["heartRateZones"][2]["minutes"]
            except KeyError as e:
                logger.debug(e)

            try:
                zone3_caloriesOut = int(a["activities-heart"][i]["value"]["heartRateZones"][3]["caloriesOut"])
            except KeyError as e:
                logger.debug(e)

            try:
                zone3_minutes = a["activities-heart"][i]["value"]["heartRateZones"][3]["minutes"]
            except KeyError as e:
                logger.debug(e)

            resultstring = dt,str(rhr),str(zone0_caloriesOut),str(zone0_minutes),str(zone1_caloriesOut),str(zone1_minutes),str(zone2_caloriesOut),str(zone2_minutes),str(zone3_caloriesOut),str(zone3_minutes)
            #print (dt + ":" + str(rhr) + ":" + str(zone0_caloriesOut) + ":" + str(zone0_minutes))
            writer.writerow(resultstring)
            #print(resultstring)


def main():
    loggerConfig()
    testAccess()

if __name__ == "__main__":
        main()
