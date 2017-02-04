import fitbitFunctions as f
import json
import logging
import argparse

logging.config.fileConfig('fitbitlogging.conf')
logger = logging.getLogger('fitbitClient')

def startP():
    res = f.resetValue()
    logger.debug(res.text)

def main():
    startP()

parser = argparse.ArgumentParser(
    description="This script gets a new access and refresh token from fitbit.")

script_version = "0.1"

parser.add_argument('-v', '--version',
                    action='version',
                    version='%(prog)s (version ' + script_version + ')')

args = parser.parse_args()

if __name__ == "__main__":
    main()
