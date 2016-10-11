#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3


import requests
import argparse
import stravaFunctions as sf
import configparser

config = configparser.ConfigParser()
config.read("/Users/gb/strava.properties")

at = (config.get("oAuth2", "oAuth2.accessToken"))

# Oude Kleefsebaan: 5319561


def getStream(id):
    #sf.getStreamSegment(id, type)
    # sf.getSegmentEfforts(id)
    # sf.getSegmentDetails(id)
    sf.getSegmentEffortsByType(id, 'heartrate')

parser = argparse.ArgumentParser(
    description="This script gets Strava streams")

script_version = "0.4"

parser.add_argument('-v', '--version',
                    action='version',
                    version='%(prog)s (version ' + script_version + ')')
# parser.add_argument("-l", dest='location', type=str, metavar='locationfile', default='location.list',
#                    help='Supply the name of the location file (default location.list)', required=False)
# parser.add_argument("-b", dest='backend', type=str, metavar='backendfile', default='backend.list',
# help='Supply the name of the backends file (default backend.list)',
# required=False)

args = parser.parse_args()


def main():
    'this uses a specific segment (Oude Kleefsebaan)'
    getStream(5319561)


if __name__ == "__main__":
    main()
