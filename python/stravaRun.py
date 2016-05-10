import stravaFunctions as sf
import configparser

# Read in the config file. The configfile currently contains the access token
config = configparser.ConfigParser()
config.read('/Users/gb/strava.properties')

at = (config.get('oAuth2', 'oAuth2.accessToken'))


res = sf.retrieveAllActivities(at)
#print(res.dtypes)