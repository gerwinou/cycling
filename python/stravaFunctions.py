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


def getSegmentEffortStream(id, type):
    'Get a specific stream of a specific activity'
    # type can be distance, altitude or time
    url = urlbase + "/segment_efforts/" + str(id) + "/streams/" + type

    params = dict(access_token=at, resolution='high')
    r = gf.getRequest(url, params)
    return r
    # print(r.text)


def getSegmentEfforts(id):
    'Get a specific stream of a specific activity'
    # need to add a function to retrieve more than 200 results in the future
    logger.info(
        "Getting efforts for the Holdeurn segment (hardcoded segment id)")

    url = urlbase + "/segments/" + str(id) + "/all_efforts"

    params = dict(access_token=at, resolution='high',
                  athlete_id=549238, per_page=200)
    r = gf.getRequest(url, params)
    a = r.json()
    if (len(a) > 0):
        logger.info(
            str(len(a)) + " Efforts found for segment name:" + a[0]['name'])
        for i in range(2):
            logger.debug(a[i]["id"])
            req = getSegmentEffortStream(a[i]["id"], 'time')
            logger.debug(req.text)


def readDfFromCsv():
    if os.path.isfile(csv_filename):
        # print(csv_filename)
        df = pd.read_csv(csv_filename, sep=";")

    return df
