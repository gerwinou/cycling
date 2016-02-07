This script is based on the script by Kyle Krafka (https://github.com/kjkjava/garmin-connect-export (Copyright (c) 2015 Kyle Krafka). Most, if not all, credit goes to him!

It works with the Garmin connect site, and retrieves your data from it.

I made the following modifications:
- removed downloading TCX and or GPX files (use the original script for that purpose). My goal was to get overall data for all my rides to make graphs of overal progress, trends in cadence and heartbeat, etc.
- I added some data, such as cadence, corrected elevation etc.
- The script will always retrieve all your activities, and store them in a simple CSV file, one line per activity, to be further processed by R scripts (see the R directory)
- The script assumes a specific data directory, and will probably crash if that directory is not present. Sorry for that, change it to your own likings

