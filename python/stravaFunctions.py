#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

import requests
import configparser
from datetime import datetime
import pandas as pd
import os.path
import numpy as np
import logging
import logging.config
import genericFunctions as gf
import csv
import itertools
from itertools import izip_longest as zip_longest

logging.config.fileConfig('./etc/logging.conf')
logger = logging.getLogger('stravamod')

# Read in the config file. The configfile currently contains the access token
config = configparser.ConfigParser()
config.read('/Users/gb/strava.properties')

config = configparser.ConfigParser()
config.read("/Users/gb/strava.properties")

at = (config.get("oAuth2", "oAuth2.accessToken"))

filepath = config.get('locations', 'csvfile.path')
filename = config.get('locations', 'csvfile.name')
csv_filename = filepath + '/' + filename

urlbase = 'https://www.strava.com/api/v3/'


def retrieveAthlete(accessToken):
    "Retrieves the data of the currently logged in user"
    getAthlete = "https://www.strava.com/api/v3/athlete/"
    params1 = dict(access_token=accessToken)

    a = requests.get(getAthlete, params1)

    athlete = a.json()  # This is the json part of the request, returning only a is not enough

    d = {'lastname': [athlete['lastname']], 'email': [athlete['email']]}
    c = ['lastname', 'email']
    dfathlete = pd.DataFrame(d, columns=c)

    return dfathlete


def retrieveAllActivities(accessToken):
    "Gets all activities for the current athlete."

    url = "https://www.strava.com/api/v3/athlete/activities/"

    with open('activity.def') as f:
        c = f.read().splitlines()

    dfactivities = pd.DataFrame(columns=c)
    dfactivities.id = dfactivities.id.astype(np.int64)

    x = True
    j = 1

    while x == True:

        params = dict(access_token=accessToken, page=j, per_page=200)

        r = requests.get(url, params)
        logger.info(r.headers['X-RateLimit-Usage'])
        # logger.info(r.headers['content-type'])

        a = r.json()

        if (len(a) == 0):
            x = False
            # break
        logger.info("still running" + str(j))
        for i in range(len(a)):

            if (a[i]["type"] == "Ride"):

                d = {b: "NA" if b not in a[i] else a[i][b] for b in c}

                """
                    The line above reads the data from the .def file
                    The following issues still exist with this:
                    - athlete_id is in a deeper level (nested)
                    # temporarily solved by adding it manually (see the line
                    # below)
                    'athlete_id':str(a[i]['athlete']['id'])
                """

                f = {'athlete_id': str(a[i]['athlete']['id'])}

                d.update(f)
                dfactivities = dfactivities.append(d, ignore_index=True)

        j += 1

    return dfactivities


def getGear():
    "placeholder for a getGear function"
    return


def getClubs():
    "placeholder for a getClubs function"
    return


def getCurrentRateLimit(at):
    res = retrieveAthlete(at)
    logger.info(res['X-RateLimit-Usage'])
    return


def getActivity(accessToken, activity):
    "Gets the details of the specific activity for the current athlete"
    url = "https://www.strava.com/api/v3/activities/" + str(activity)
    params = dict(access_token=accessToken)
    try:
        r = requests.get(url, params)
        logger.info("Current usage is %s", r.headers['X-RateLimit-Usage'])

    except requests.exceptions.Timeout as e:
        logger.critical(
            "Connection Timeout occurred while connecting to: %s", url)
        exit(1)
    except requests.ConnectionError as e:
        # print("Connection Error occurred while accessing " + url)
        logger.critical(
            "Connection Error occurred while connecting to: %s", url)

        exit(1)

    print(r.text)
    a = r.json()

    return a


def writeDfToCsv(res):

    current_date = datetime.now().strftime('%Y-%m-%d')

    # csv_filename = filepath+'/'+filename

    if os.path.isfile(csv_filename):
        timestamp = str(datetime.today())
        logger.info(
            "Writing data to file, previous file will be saved with the following timestamp: " + current_date)
        os.rename(csv_filename, csv_filename + "." + current_date)

    csv_file = open(csv_filename, 'w')

    res.to_csv(csv_file, encoding='utf8', index=True,
               index_label='Index', sep=";", na_rep="NA")
    csv_file.close()

    return


def writeStreamToCsv(file_name, *args):

    current_date = datetime.now().strftime('%Y-%m-%d')
    # filename = filepath + '/consolidated.csv'
    filename = filepath + '/' + file_name

    if os.path.isfile(filename):
        timestamp = str(datetime.today())
        logger.info(
            "Writing data to file, previous file will be saved with the following timestamp: " + current_date)
        os.rename(filename, filename + "." + current_date)

    with open(filename, 'w') as f:

        wr = csv.writer(f)
        wr.writerows(zip(*args))
        # wr.writerows(*args)
    return


def writeListStreamToCsv(file_name, list):

    current_date = datetime.now().strftime('%Y-%m-%d')
    # filename = filepath + '/consolidated.csv'
    filename = filepath + '/' + file_name

    if os.path.isfile(filename):
        timestamp = str(datetime.today())
        logger.info(
            "Writing data to file, previous file will be saved with the following timestamp: " + current_date)
        os.rename(filename, filename + "." + current_date)

    with open(filename, 'w') as f:

        wr = csv.writer(f)
        wr.writerows(zip_longest(*list))
        # wr.writerows(*args)
    return


def getSegmentDetails(id):
    'Get distance and altitude of a segment'
    url = urlbase + "/segments/" + str(id) + "/streams/altitude"
    params = dict(access_token=at, resolution='low')

    r = gf.getRequest(url, params)
    # logger.debug(r.text)
    return r


def getSegmentEffortStream(id, type):
    'Get a specific stream of a specific activity'
    # type can be distance, altitude or time
    url = urlbase + "/segment_efforts/" + str(id) + "/streams/" + type

    params = dict(access_token=at, resolution='high')
    r = gf.getRequest(url, params)
    return r
    # print(r.text)

'''
def getSegmentEfforts(id):
    'Get multiple streams of a specific activity'
    # need to add a function to retrieve more than 200 results in the future
    logger.info(
        "Getting efforts for the Holdeurn segment (hardcoded segment id)")
    #df = pd.DataFrame
    url = urlbase + "/segments/" + str(id) + "/all_efforts"

    params = dict(access_token=at, resolution='high',
                  athlete_id=549238, per_page=200)
    r = gf.getRequest(url, params)
    # logger.debug(r.text)


    ac = r.json()
    if (len(ac) > 0):
        logger.info(
            str(len(ac)) + " Efforts found for segment name:" + ac[0]['name'])
        # for i in range(len(a)):
        for i in range(0, 3):
            # logger.info(ac[i]['start_date'])
            effortID = str(ac[i]["id"])
            logger.debug("Effort id is : " + str(ac[i]["id"]))
            logger.debug("Writing file for " + effortID)

            req1 = getSegmentEffortStream(ac[i]["id"], 'time')
            req2 = getSegmentEffortStream(ac[i]["id"], 'velocity_smooth')
            req3 = getSegmentEffortStream(ac[i]["id"], 'heartrate')
            req4 = getSegmentEffortStream(ac[i]["id"], 'altitude')

            a = req1.json()[0]["data"]
            a.insert(0, 'time')
            b = req2.json()[0]["data"]
            b.insert(0, 'distance')
            c = req2.json()[1]["data"]
            c.insert(0, 'velocity')
            d = req3.json()[1]["data"]
            d.insert(0, 'heartrate')
            e = req4.json()[1]["data"]
            e.insert(0, 'altitude')

            writeStreamToCsv(effortID + '.csv', a, b, c, d, e)
'''


def getSegmentEffortsByType(id, atype):
    'Get a specific stream (speed) of multiple efforts'
    # need to add a function to retrieve more than 200 results in the future
    logger.info(
        "Getting speed efforts for the Holdeurn segment (hardcoded segment id)")
    #df = pd.DataFrame
    url = urlbase + "/segments/" + str(id) + "/all_efforts"

    logger.info("Getting segment details")
    d = getSegmentDetails(id)

    dist = d.json()[0]["data"]
    dist.insert(0, "distance")

    alt = d.json()[1]["data"]
    alt.insert(0, "altitude")
    params = dict(access_token=at, resolution='high',
                  athlete_id=549238, per_page=200)
    r = gf.getRequest(url, params)
    # logger.debug(r.text)
    ac = r.json()
    aList = []
    aList.append(dist)
    aList.append(alt)

    if (len(ac) > 0):
        logger.info(
            str(len(ac)) + " Efforts found for segment name:" + ac[0]['name'])
        # for i in range(len(a)):
        for i in range(len(ac)):
            logger.info(ac[i]['start_date'])
            effortID = str(ac[i]["id"])
            logger.debug("Effort id is : " + str(ac[i]["id"]))
            # here we should catch the error when data is not available
            req = getSegmentEffortStream(ac[i]["id"], atype)
            tmpjson = req.json()
            logger.debug("length: " + str(len(tmpjson)))
            if (len(tmpjson)>1):
                result = req.json()[1]["data"]
                #logger.debug("Result: " + str(result))
                #result.insert(0, 'effort' + str(i))
                result.insert(0, effortID)
                aList.append(result)
            else:
                continue
            
        writeListStreamToCsv(atype + '.csv', aList)


def readDfFromCsv():
    if os.path.isfile(csv_filename):
        # print(csv_filename)
        df = pd.read_csv(csv_filename, sep=";")

    return df
