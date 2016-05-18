#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

import stravaFunctions as sf
import configparser

import argparse

parser = argparse.ArgumentParser(
    description = 'Strava Data Analysis Tool',
    epilog = 'Happy Cycling!')

script_version = '0.1'

parser.add_argument('-v','--version', help="print version and exit", action="store_true")
parser.add_argument('-u','--update', help="Updates all activities in the csv file", action="store_true")
#parser.add_argument('--password', help="your Garmin Connect password (otherwise, you will be prompted)", nargs='?')

args = parser.parse_args()

if args.version:
	print ("version " + script_version)
	exit(0)

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
    #print(res)
    #actIds = res['id']
    #print(actIds)
    return res

def getActivity(res):
    #act = sf.getActivity(at,actIds[0])
    #act = sf.getActivity(at,'573957038') # hardcoded to test
    act = sf.getActivity(at,res['id'][0])
    print("Number of efforts found in this activity: " + str(len(act['segment_efforts'])))

    for i in range (len(act['segment_efforts'])):
        print(str(act['segment_efforts'][i]['segment']['id'])+":"+act['segment_efforts'][i]['segment']['name'])
    return

# Main
# Must be parameterized by command line switches
if args.update:
    updateData()
    exit(0)

# updateData() # updates the csv file with activities
res = readDataFromCsv() # reads from the CSV
getActivity(res)
