import stravaFunctions as sf
import configparser
from datetime import datetime
import os.path

current_date = datetime.now().strftime('%Y-%m-%d')

# Read in the config file. The configfile currently contains the access token
config = configparser.ConfigParser()
config.read('/Users/gb/strava.properties')

res = sf.retrieveAllActivities(at)