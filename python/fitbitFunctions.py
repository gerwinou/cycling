import requests
import configparser
from datetime import datetime
import os.path
import logging
import logging.config
import json
import base64

# TODO: - generalize requests
# TODO: - handle refresh action; reset the AT en RT within

# Make sure locales have been exported correctly:
# export LC_ALL=en_US.UTF-8
# export LANG=en_US.UTF-8
logging.config.fileConfig('fitbitlogging.conf')
logger = logging.getLogger('fitbitClient')

propfile = "/Users/gb/fitbit.properties"
tokenfile = "/Users/gb/fitbittokens.properties"

# Read in the config file.
props = configparser.ConfigParser()
props.read(propfile)

config = configparser.ConfigParser()
config.read(tokenfile)

logger.debug("Configfile to be used: " + propfile)
logger.debug("tokenfile to be used: " + tokenfile)


at = config.get('general', 'at')
rt = config.get('general', 'rt')


def resetValue():
    # auth=HTTPBasicAuth('user', 'pass')

    headers = {'Authorization': 'Basic MjI3U1RHOjIxZGRmNWRiNTU5NTFiY2ViZTY4OWU1MGZjYWFjOThj',
               'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'refresh_token',
            'refresh_token': rt}
    url = "https://api.fitbit.com/oauth2/token"

    r = requests.post(url, data=data, headers=headers)
    logger.debug(r.status_code)
    logger.debug(r.text)

    j = json.loads(r.text)
    newAT = j['access_token']
    newRT = j['refresh_token']
    expiry = j['expires_in']

    logger.debug(newAT)
    logger.debug(newRT)

    newConfig = configparser.ConfigParser()
    newConfig.add_section('general')
    newConfig.set('general', 'at', newAT)
    newConfig.set('general', 'rt', newRT)

    with open(tokenfile, 'w') as f:
        newConfig.write(f)


def testAccess():

    accesstoken = at
    headers = {'Authorization': 'Bearer ' + accesstoken}
    url = 'https://api.fitbit.com/1/user/-/profile.json'

    r = requests.get(url, headers=headers)
    logger.debug(r.status_code)
    if(r.status_code != 200):
        if(r.status_code == 401):
            logger.debug("AT has expired")
            resetValue()
        else:
            logger.warn("Some error has occurred, aborting")
            logger.debug(r.status_code)
            exit()
    j = json.loads(r.text)

    #logger.debug(j['user']['fullName'])
    #logger.debug(j['user']['topBadges'][0]['name'])


def getHeartbeat():

    accesstoken = at
    headers = {'Authorization': 'Bearer ' + accesstoken}
    url = 'https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json'

    r = requests.get(url, headers=headers)
    logger.debug(r.status_code)
    j = json.loads(r.text)

    logger.debug(j)


def main():
    testAccess()
    getHeartbeat()


if __name__ == "__main__":
    main()
