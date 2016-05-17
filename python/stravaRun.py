#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

import stravaFunctions as sf
import configparser

# Read in the config file. The configfile currently contains the access token
config = configparser.ConfigParser()
config.read('/Users/gb/strava.properties')

at = (config.get('oAuth2', 'oAuth2.accessToken'))

res = sf.retrieveAllActivities(at)
#print(res.dtypes)

# sf.writeDfToCsv(res)

actIds = res['id']
#print(actIds)


act = sf.getActivity(at,actIds[0])
print(act)
