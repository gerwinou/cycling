#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

import stravaFunctions as sf
import configparser

# Read in the config file. The configfile currently contains the access token
config = configparser.ConfigParser()
config.read('/Users/gb/strava.properties')

at = (config.get('oAuth2', 'oAuth2.accessToken'))

def updateData():
    res = sf.retrieveAllActivities(at)
    #print(res.dtypes)
    sf.writeDfToCsv(res)
    return

def readDataFromCsv():
    res = sf.readDfFromCsv()
    # print(res)
    actIds = res['id']
    print(actIds)
    return

def getActivity():
    #act = sf.getActivity(at,actIds[0])
    #act = sf.getActivity(at,'573957038') # hardcoded to test

    #print("Number of efforts found in this activity: " + str(len(act['segment_efforts'])))
    #print(act['segment_efforts'][0])
    return

# Main
# Must be parameterized by command line switches

# updateData()
readDataFromCsv()
