#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

import stravaFunctions as sf
import configparser
import argparse
import logging
import logging.config

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("strava")

parser = argparse.ArgumentParser(
    description="Strava Data Analysis Tool",
    epilog="Happy Cycling!")

script_version = "0.1"

parser.add_argument("-v", "--version",
                    help="print version and exit", action="store_true")
parser.add_argument(
    "-u", "--update", help="Updates all activities in the csv file", action="store_true")
#parser.add_argument("--password", help="your Garmin Connect password (otherwise, you will be prompted)", nargs="?")

args = parser.parse_args()

if args.version:
    print("version " + script_version)
    exit(0)

# Read in the config file. The configfile currently contains the access token
config = configparser.ConfigParser()
config.read("/Users/gb/strava.properties")

at = (config.get("oAuth2", "oAuth2.accessToken"))


def updateData():
    cur = readDataFromCsv()
    res = sf.retrieveAllActivities(at)

    logger.info("Previous no. of records " + str(len(cur.index)))
    logger.info("Current no. of records " + str(len(res.index)))

    #row_ids = res[res["id"] != cur.id].index
    firstlist = set(cur.id)
    targetDF = res[res.id.isin(firstlist) == False]
    if(len(targetDF.index) > 0):
        logger.info("Some new records found")
        logger.info(targetDF['id'])
    else:
        logger.info("No new records found")

    sf.writeDfToCsv(res)
    return


def readDataFromCsv():
    res = sf.readDfFromCsv()
    return res


def getActivity(res):

    act = sf.getActivity(at, res)

    logger.info("Number of efforts found in this activity: %s",
                str(len(act["segment_efforts"])))
    for i in range(len(act["segment_efforts"])):
        logger.info(str(act["segment_efforts"][i]["segment"][
                    "id"]) + ":" + act["segment_efforts"][i]["segment"]["name"])
    return

if args.update:
    logger.info("Updating the list of activities")
    updateData()
    logger.info("Done updating the list of activities")

    exit(0)

logger.info("Starting from existing CSV file")
res = readDataFromCsv()  # reads from the CSV
getActivity(res["id"][0])

"""
Future enhancements:
- if option update was chosen:
    read in the file first
    then get all activities
    compare these with the activities already in the file
    update the file (simply by calling writeDfToCsv), but keep the new entries in a separate array
    do extra processing based on the entries in the separate array (for example detect new segments)
    keep a list of all segments, so segment efforts can be built
"""
