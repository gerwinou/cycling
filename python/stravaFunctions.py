#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

import requests
import configparser
from datetime import datetime
import pandas as pd
import os.path
import numpy as np

# Read in the config file. The configfile currently contains the access token
config = configparser.ConfigParser()
config.read('/Users/gb/strava.properties')

filepath = config.get('locations','csvfile.path')
filename = config.get('locations','csvfile.name')
csv_filename = filepath+'/'+filename

def retrieveAthlete(accessToken):
    "Retrieves the data of the currently logged in user"
    getAthlete = "https://www.strava.com/api/v3/athlete/"
    params1 = dict(access_token=accessToken)

    a = requests.get(getAthlete, params1)

    athlete = a.json() # This is the json part of the request, returning only a is not enough

    d =  {'lastname':[athlete['lastname']],'email':[athlete['email']]}
    c = ['lastname','email']
    dfathlete = pd.DataFrame(d, columns=c)

    return dfathlete

def retrieveAllActivities(accessToken):
    "Gets all activities for the current athlete and writes them (optionally to a CSV file)."

    url = "https://www.strava.com/api/v3/athlete/activities/"

    with open('activity.def') as f:
        c = f.read().splitlines()

    dfactivities = pd.DataFrame(columns=c)
    dfactivities.id=dfactivities.id.astype(np.int64)

    x = True
    j = 1

    while x == True:

        params = dict(access_token=accessToken, page=j, per_page=200)

        r = requests.get(url, params)
        print(r.headers['X-RateLimit-Usage'])
        a = r.json()

        if (len(a) == 0):
            x = False

        for i in range (len(a)):

            if (a[i]['type'] == 'Ride'):

                d =  { b:"NA" if b not in a[i] else a[i][b] for b in c }

                """
                    The line above reads the data from the .def file
                    The following issues still exist with this:
                    - athlete_id is in a deeper level (nested)
                    'athlete_id':str(a[i]['athlete']['id']) # temporarily solved by adding it manually (see the line below)
                """

                f = {'athlete_id':str(a[i]['athlete']['id'])}

                d.update(f)
                dfactivities = dfactivities.append(d,ignore_index=True)

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
    print(res['X-RateLimit-Usage'])
    return

def getActivity(accessToken,activity):
    "Gets the details of the specific activity for the current athlete"
    url = "https://www.strava.com/api/v3/activities/" + str(activity)
    params = dict(access_token=accessToken)

    r = requests.get(url, params)
    print(r.headers['X-RateLimit-Usage'])
    a = r.json()

    return a

def writeDfToCsv(res):

    current_date = datetime.now().strftime('%Y-%m-%d')

    # csv_filename = filepath+'/'+filename

    if os.path.isfile(csv_filename):
        timestamp = str(datetime.today())
        print("Writing data to file, previous file will be saved with the following timestamp: " + current_date)
        os.rename(csv_filename, csv_filename + "." + current_date)

    csv_file = open(csv_filename, 'w')

    res.to_csv(csv_file, encoding='utf8',index=True,index_label='Index', sep=";",na_rep="NA")
    csv_file.close()

    return

def readDfFromCsv():
    if os.path.isfile(csv_filename):
        print(csv_filename)
        df = pd.read_csv(csv_filename,sep=";")

    return df
