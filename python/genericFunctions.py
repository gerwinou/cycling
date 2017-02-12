import requests
import configparser
from datetime import datetime
import os.path
import logging
import logging.config
import json
import csv
import ast
import inspect

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Some general checks to see if everything is in place

logconfigurationfile = './etc/logging.conf'

if (not os.path.isfile(logconfigurationfile)):
    # print("Logging Config file found, all looks good")
    # else:
    print("Logging configuration not found, exiting(1)")
    exit(1)
else:
    print("Logging configuration found")
logging.config.fileConfig(logconfigurationfile)
logger = logging.getLogger('Generic')

propfile = "./etc/strava.conf"

if (not os.path.isfile(propfile)):
    # logger.debug("Config file found")
    # else:
    logger.warn("Config file not found, exiting(1)")
    exit(1)
else:
    # Read in the config file.
    config = configparser.ConfigParser()
    config.read(propfile)
    logger.debug("Configfile to be used: " + propfile)

authConfig = configparser.ConfigParser()
authConfig.read("/Users/gb/strava.properties")

at = (authConfig.get("oAuth2", "oAuth2.accessToken"))
# filepath = config.get('general', 'csvfile.path')

# Begin functions
logger.debug("Starting execution")


def getRequest(reqUrl, params):
    'Generic get request'
    logger.debug("Inside function getRequest")
    #logger.debug("---" + inspect.stack()[0][3])

    r = requests.get(reqUrl, params)
    logger.debug("requestedURL: " + reqUrl)
    if (r.status_code == 200):
        logger.debug("Ok (200)")
        logger.debug(r.text)

    else:
        logger.warn("Something went wrong: " + str(r.status_code))
    return r
