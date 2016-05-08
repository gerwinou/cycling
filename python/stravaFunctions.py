import requests
import configparser
from datetime import datetime
import pandas as pd
import os.path

# Read in the config file. The configfile currently contains the access token
config = configparser.ConfigParser()
config.read('/Users/gb/strava.properties')

#at = (config.get('oAuth2', 'oAuth2.accessToken'))

filepath = config.get('locations','csvfile.path')
filename = config.get('locations','csvfile.name')

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
    c = [
        'type',
        'max_speed',
        'average_watts',
        'id',
        'private',
        'start_longitude',
        'moving_time',
        'elev_low',
        'total_elevation_gain',
        'average_heartrate',
        'location_state',
        'gear_id',
        'athlete_count',
        'location_country',
        'timezone',
        'elev_high',
        'end_latlng',
        'average_cadence',
        'start_date',
        'location_city',
        'max_heartrate',
        'start_latitude',
        'distance',
        'name',
        'kilojoules',
        'resource_state',
        'start_date_local',
        'athlete_id',
	    'elapsed_time',
        'start_latlng',
        'average_speed',

         ]
    dfactivities = pd.DataFrame(columns=c)

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
                d =  {
                    'id':str(a[i]['id']),
                    'type':a[i]['type'],
                    'max_speed':a[i]['max_speed'],
                    'average_watts':a[i]['average_watts'],
                    'private':a[i]['private'],
                    'start_longitude':a[i]['start_longitude'],
                    'moving_time':a[i]['moving_time'],
                    'elev_low':a[i]['elev_low'],
                    'total_elevation_gain':a[i]['total_elevation_gain'],
                    'average_heartrate':"NA" if 'average_heartrate' not in a[i] else a[i]['average_heartrate'],
                    'location_state':a[i]['location_state'],
                    'gear_id':a[i]['gear_id'],
                    'athlete_count':a[i]['athlete_count'],
                    'location_country':a[i]['location_country'],
                    'timezone':a[i]['timezone'],
                    'elev_high':a[i]['elev_high'],
                    'end_latlng':a[i]['end_latlng'],
                    'average_cadence':"NA" if 'average_cadence' not in a[i] else a[i]['average_cadence'],
                    'start_date':a[i]['start_date'],
                    'location_city':a[i]['location_city'],
                    'max_heartrate':"NA" if 'max_heartrate' not in a[i] else ['max_heartrate'],
                    'start_latitude':a[i]['start_latitude'],
                    'distance':a[i]['distance'],
                    'name':a[i]['name'],
                    'kilojoules':a[i]['kilojoules'],
                    'resource_state':a[i]['resource_state'],
                    'start_date_local':a[i]['start_date_local'],
                    'athlete_id':str(a[i]['athlete']['id']) ,
                    'elapsed_time':a[i]['elapsed_time'],
                    'start_latlng':a[i]['start_latlng'],
                    'average_speed':a[i]['average_speed']
                      }
                dfactivities = dfactivities.append(d,ignore_index=True)
            #i+=1
        j += 1
    writeDfToCsv(dfactivities)
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
    "Gets the activities for the current athlete"
    url = "https://www.strava.com/api/v3/activities/" + str(activity)
    params = dict(access_token=accessToken)

    r = requests.get(url, params)
    print(r.headers['X-RateLimit-Usage'])
    a = r.json()

    return a

def writeDfToCsv(res):

    current_date = datetime.now().strftime('%Y-%m-%d')

    #csv_filename = '../../data/cycling/strava_activities.csv'
    csv_filename = filepath+'/'+filename

    if os.path.isfile(csv_filename):
        timestamp = str(datetime.today())
        print("Writing data to file, previous file will be saved with the following timestamp: " + current_date)
        os.rename(csv_filename, csv_filename + "." + current_date)

    csv_file = open(csv_filename, 'w')

    res.to_csv(csv_file, encoding='utf8',index=True,index_label='Index')
    csv_file.close()

    return