'''
The following lines are provided as a reference for how to do a request, and how to get the refresh_token

curl -i -H "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0N1E4TEYiLCJhdWQiOiIyMjdTVEciLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNDc0NjY2MjE1LCJpYXQiOjE0NzQ2Mzc0MTV9.bi_BRBVNGi-LVirPq9XsW5_mBVyNSCERuPDcwthAQhs" https://api.fitbit.com/1/user/-/profile.json

eyJhbGciOiJIUzI1NiJ9eyJzdWIiOiI0N1E4TEYiLCJhdWQiOiIyMjdTVEciLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNDc0NjY2MjE1LCJpYXQiOjE0NzQ2Mzc0MTV9bi/vv71EFU0aL++/vVYqz6vvv73vv71b77+977+9BVzvv71IIRHvv73vv73vv73vv73vv71AQhs=

Refresh token
curl -X POST -i -H "Authorization: Basic MjI3U1RHOjIxZGRmNWRiNTU5NTFiY2ViZTY4OWU1MGZjYWFjOThj" -H "Content-Type: application/x-www-form-urlencoded"
-d "grant_type=refresh_token" -d "refresh_token=f1a4a36f7ea84077807596e224fca71319c6627c50af772b108df36a18571ece" https://api.fitbit.com/oauth2/token

{"access_token":"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0N1E4TEYiLCJhdWQiOiIyMjdTVEciLCJpc3MiOiJGaXRiaXQiLCJ0eXAiO
iJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNDc0Nj
Y2MjE1LCJpYXQiOjE0NzQ2Mzc0MTV9.bi_BRBVNGi-LVirPq9XsW5_mBVyNSCERuPDcwthAQhs",
"expires_in":28800,
"refresh_token":"c472f65d0ff7104eb264e4a89f8f0d0d8ac44026c29f3657f7186461b53e705c","scope":"profile activity settings social location weight sleep heartrate nutrition","token_type":"Bearer","user_id":"47Q8LF"}

{"access_token":"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0N1E4TEYiLCJhdWQiOiIyMjdTVEciLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJudXQgcnBybyByc2xlIiwiZXhwIjoxNDc0NjY3NDQyLCJpYXQiOjE0NzQ2Mzg2NDJ9.Go0_BJkAyukoKFu009p0qrLSfApJ9hupk3ns-ejph-I",
"expires_in":28800,
"refresh_token":"df61aec4473d87a94db7d144593780c7ba2d8f7f0882c72ed6ff7ccb2e78bbf4",
"scope":"social activity nutrition settings location heartrate profile sleep weight","token_type":"Bearer","user_id":"47Q8LF"}

'''

import requests
import configparser
from datetime import datetime
import os.path
import logging
import logging.config
import json
import base64

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

    headers = {'Authorization': ' Basic MjI3U1RHOjIxZGRmNWRiNTU5NTFiY2ViZTY4OWU1MGZjYWFjOThj',
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

    logger.debug(j['user']['fullName'])
    logger.debug(j['user']['topBadges'][0]['name'])


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
