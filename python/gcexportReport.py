# python gcexportReport.py --username gerwinou --password []

# TODO:
# add weather info
# add gear info
# retrieve from modern interface
# prepare for R:
#				Mostly data issues:
# 				 - remove/correct outliers (absurd speeds and heartrates)


from urllib import urlencode
from datetime import datetime
from getpass import getpass
from sys import argv
from os.path import isdir
from os.path import isfile
from os import mkdir
from os import remove
from xml.dom.minidom import parseString
# import datetime
import os




import urllib2, cookielib, json
from fileinput import filename

import argparse
import zipfile

script_version = '1.0.0'
current_date = datetime.now().strftime('%Y-%m-%d')
activities_directory = './' + current_date + '_garmin_connect_export'

parser = argparse.ArgumentParser()

# TODO: Implement verbose and/or quiet options.
# parser.add_argument('-v', '--verbose', help="increase output verbosity", action="store_true")
parser.add_argument('--version', help="print version and exit", action="store_true")
parser.add_argument('--username', help="your Garmin Connect username (otherwise, you will be prompted)", nargs='?')
parser.add_argument('--password', help="your Garmin Connect password (otherwise, you will be prompted)", nargs='?')

args = parser.parse_args()

if args.version:
	print argv[0] + ", version " + script_version
	exit(0)

cookie_jar = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))

# url is a string, post is a dictionary of POST parameters, headers is a dictionary of headers.
def http_req(url, post=None, headers={}):
	request = urllib2.Request(url)
	request.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/1337 Safari/537.36')  # Tell Garmin we're some supported browser.
	for header_key, header_value in headers.iteritems():
		request.add_header(header_key, header_value)
	if post:
		post = urlencode(post)  # Convert dictionary to POST parameter string.
	response = opener.open(request, data=post)  # This line may throw a urllib2.HTTPError.

	# N.B. urllib2 will follow any 302 redirects. Also, the "open" call above may throw a urllib2.HTTPError which is checked for below.
	if response.getcode() != 200:
		raise Exception('Bad return code (' + response.getcode() + ') for: ' + url)

	return response.read()

print 'Welcome to Garmin Connect Reporter!'

username = args.username if args.username else raw_input('Username: ')
password = args.password if args.password else getpass()

# Maximum number of activities you can request at once.  Set and enforced by Garmin.
limit_maximum = 100

# URLs for various services.
url_gc_login     = 'https://sso.garmin.com/sso/login?service=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&webhost=olaxpw-connect04&source=https%3A%2F%2Fconnect.garmin.com%2Fen-US%2Fsignin&redirectAfterAccountLoginUrl=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&redirectAfterAccountCreationUrl=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&gauthHost=https%3A%2F%2Fsso.garmin.com%2Fsso&locale=en_US&id=gauth-widget&cssUrl=https%3A%2F%2Fstatic.garmincdn.com%2Fcom.garmin.connect%2Fui%2Fcss%2Fgauth-custom-v1.1-min.css&clientId=GarminConnect&rememberMeShown=true&rememberMeChecked=false&createAccountShown=true&openCreateAccount=false&usernameShown=false&displayNameShown=false&consumeServiceTicket=false&initialFocus=true&embedWidget=false&generateExtraServiceTicket=false'
url_gc_post_auth = 'https://connect.garmin.com/post-auth/login?'
url_gc_search    = 'http://connect.garmin.com/proxy/activity-search-service-1.0/json/activities?'
url_gc_gpx_activity = 'http://connect.garmin.com/proxy/activity-service-1.1/gpx/activity/'
url_gc_tcx_activity = 'http://connect.garmin.com/proxy/activity-service-1.1/tcx/activity/'
url_gc_original_activity = 'http://connect.garmin.com/proxy/download-service/files/activity/'

# Initially, we need to get a valid session cookie, so we pull the login page.
http_req(url_gc_login)

# Now we'll actually login.
post_data = {'username': username, 'password': password, 'embed': 'true', 'lt': 'e1s1', '_eventId': 'submit', 'displayNameRequired': 'false'}  # Fields that are passed in a typical Garmin login.
http_req(url_gc_login, post_data)

# Get the key.
# TODO: Can we do this without iterating?
login_ticket = None
for cookie in cookie_jar:
	if cookie.name == 'CASTGC':
		login_ticket = cookie.value
		break

if not login_ticket:
	raise Exception('Did not get a ticket cookie. Cannot log in. Did you enter the correct username and password?')

# Chop of 'TGT-' off the beginning, prepend 'ST-0'.
login_ticket = 'ST-0' + login_ticket[4:]

http_req(url_gc_post_auth + 'ticket=' + login_ticket)

# We should be logged in now.

csv_filename = '../../data/cycling/activities.csv'

if csv_filename:
    timestamp = str(datetime.today())
    print current_date
    os.rename(csv_filename , csv_filename + "." + current_date)

csv_file = open(csv_filename, 'w')

# Write header to CSV file
#csv_file.write('Activity ID,Activity Name,Description,Begin Timestamp,Begin Timestamp (Raw Milliseconds),End Timestamp,End Timestamp (Raw Milliseconds),Device,Activity Parent,Activity Type,Event Type,Activity Time Zone,Max. Elevation,Max. Elevation (Raw),Begin Latitude (Decimal Degrees Raw),Begin Longitude (Decimal Degrees Raw),End Latitude (Decimal Degrees Raw),End Longitude (Decimal Degrees Raw),Average Moving Speed,Average Moving Speed (Raw),Max. Heart Rate (bpm),Average Heart Rate (bpm),Max. Speed,Max. Speed (Raw),Calories,Calories (Raw),Duration (h:m:s),Duration (Raw Seconds),Moving Duration (h:m:s),Moving Duration (Raw Seconds),Average Speed,Average Speed (Raw),Distance,Distance (Raw),Max. Heart Rate (bpm),Min. Elevation,Min. Elevation (Raw),Elevation Gain,Elevation Gain (Raw),Elevation Loss,Elevation Loss (Raw)\n')
csv_file.write('ActivityID;'
			   'ActivityName;'
			   'Description;'
			   'BeginTimestamp;'
			   'EndTimestamp;'
			   'Device;'
			   'ActivityParent;'
			   'ActivityType;'
			   'EventType;'
			   'ActivityTimeZone;'
			   'MaxElevation;'
			   'BeginLatitude;'
			   'BeginLongitude;'
			   'EndLatitude;'
			   'EndLongitude;'
			   'AverageMovingSpeed;'
			   'MaxHeartRate;'
			   'AverageHeartRate;'
			   'MaxSpeed;'
			   'Calories;'
			   'Duration;'
			   'MovingDuration;'
			   'AverageSpeed;'
			   'Distance;'
			   'MinHeartRate;'
			   'MinElevation;'
			   'ElevationGain;'
			   'AvgCadence;'
			   'MaxCadence;'
			   'maxElevationCorrected;'
			   'minElevationCorrected;'
			   'gainElevationCorrected\n')

# 	# To determine the number of activities, first download one,
# 	# then the result of that request will tell us how many are available
# 	# so we will modify the variables then.
total_to_download = 1
download_all = True

total_downloaded = 0

# This while loop will download data from the server in multiple chunks, if necessary.
while total_downloaded < total_to_download:
	# Maximum of 100... 400 return status if over 100.  So download 100 or whatever remains if less than 100.
	if total_to_download - total_downloaded > 100:
		num_to_download = 100
	else:
		num_to_download = total_to_download - total_downloaded

	search_params = {'start': total_downloaded, 'limit': num_to_download}
	# Query Garmin Connect
	result = http_req(url_gc_search + urlencode(search_params))
	json_results = json.loads(result)  # TODO: Catch possible exceptions here.


	search = json_results['results']['search']

	if download_all:
		# Modify total_to_download based on how many activities the server reports.
		total_to_download = int(search['totalFound'])
		# Do it only once.
		download_all = False

	# Pull out just the list of activities.
	activities = json_results['results']['activities']

	# Process each activity.
	for a in activities:
		if a['activity']['activityType']['display']  == 'Cycling':
			# Display which entry we're working on.
			print 'Garmin Connect activity: [' + a['activity']['activityId'] + ']',
			print a['activity']['activityName']['value']
			print '\t' + a['activity']['beginTimestamp']['display'] + ',',
			if 'sumElapsedDuration' in a['activity']:
				print a['activity']['sumElapsedDuration']['display'] + ',',
			else:
				print '??:??:??,',
			if 'sumDistance' in a['activity']:
				print a['activity']['sumDistance']['withUnit']
			else:
				print '0.00 Miles'

			# Write stats to CSV.
			# The exact format of the data must be modified below (replace dots to be compatible with R integer interpretation etc.)
			empty_record = ';'		# test to see if this solves N/A issues with Elevation.Gain

			csv_record = ''

			csv_record += empty_record if 'activityId' not in a['activity'] else a['activity']['activityId'] + ';'
			csv_record += empty_record if 'activityName' not in a['activity'] else a['activity']['activityName']['value'] + ';'
			csv_record += empty_record if 'activityDescription' not in a['activity'] else a['activity']['activityDescription']['value'] + ';'
			csv_record += empty_record if 'beginTimestamp' not in a['activity'] else a['activity']['beginTimestamp']['value'] + ';'
			csv_record += empty_record if 'endTimestamp' not in a['activity'] else a['activity']['endTimestamp']['value'] + ';'
			csv_record += empty_record if 'device' not in a['activity'] else a['activity']['device']['display'] + ' ' + a['activity']['device']['version'] + ';'
			csv_record += empty_record if 'activityType' not in a['activity'] else a['activity']['activityType']['parent']['display'] + ';'
			csv_record += empty_record if 'activityType' not in a['activity'] else a['activity']['activityType']['display'] + ';'
			csv_record += empty_record if 'eventType' not in a['activity'] else a['activity']['eventType']['display'] + ';'
			csv_record += empty_record if 'activityTimeZone' not in a['activity'] else a['activity']['activityTimeZone']['display'] + ';'
			csv_record += '0,0;' if 'maxElevation' not in a['activity'] else  a['activity']['maxElevation']['display'].replace('.','') + ';'
			csv_record += empty_record if 'beginLatitude' not in a['activity'] else a['activity']['beginLatitude']['value'] + ';'
			csv_record += empty_record if 'beginLongitude' not in a['activity'] else a['activity']['beginLongitude']['value'] + ';'
			csv_record += empty_record if 'endLatitude' not in a['activity'] else a['activity']['endLatitude']['value'] + ';'
			csv_record += empty_record if 'endLongitude' not in a['activity'] else a['activity']['endLongitude']['value'] + ';'
			csv_record += empty_record if 'weightedMeanMovingSpeed' not in a['activity'] else  a['activity']['weightedMeanMovingSpeed']['display'] + ';'
			csv_record += empty_record if 'maxHeartRate' not in a['activity'] else a['activity']['maxHeartRate']['display'] + ';'
			csv_record += empty_record if 'weightedMeanHeartRate' not in a['activity'] else  a['activity']['weightedMeanHeartRate']['display'] + ';'
			csv_record += empty_record if 'maxSpeed' not in a['activity'] else a['activity']['maxSpeed']['display'] + ';'
			csv_record += empty_record if 'sumEnergy' not in a['activity'] else  a['activity']['sumEnergy']['display'].replace('.', '') + ';'
			csv_record += empty_record if 'sumElapsedDuration' not in a['activity'] else a['activity']['sumElapsedDuration']['display'] + ';'
			csv_record += empty_record if 'sumMovingDuration' not in a['activity'] else a['activity']['sumMovingDuration']['display'] + ';'
			csv_record += empty_record if 'weightedMeanSpeed' not in a['activity'] else a['activity']['weightedMeanSpeed']['display'] + ';'
			csv_record += empty_record if 'sumDistance' not in a['activity'] else  a['activity']['sumDistance']['display'] + ';'
			csv_record += empty_record if 'minHeartRate' not in a['activity'] else  a['activity']['minHeartRate']['display'] + ';'
			csv_record += empty_record if 'minElevation' not in a['activity'] else  a['activity']['minElevation']['display'].replace('.','') + ';'
			csv_record += '0;' if 'gainElevation' not in a['activity'] else  a['activity']['gainElevation']['display'].replace('.','') + ';'
			csv_record += empty_record if 'weightedMeanBikeCadence' not in a['activity'] else a['activity']['weightedMeanBikeCadence']['display'] + ';'
			csv_record += empty_record if 'maxBikeCadence' not in a['activity'] else a['activity']['maxBikeCadence']['display'] + ';'
			csv_record += '0;' if 'maxCorrectedElevation' not in a['activity'] else a['activity']['maxCorrectedElevation']['display'].replace('.','')[:-2] + ';' # in cm
			csv_record += '0;' if 'minCorrectedElevation' not in a['activity'] else a['activity']['minCorrectedElevation']['display'].replace('.','')[:-2] + ';'# in cm
			csv_record += '0' if 'gainCorrectedElevation' not in a['activity'] else a['activity']['gainCorrectedElevation']['display'].replace('.','')[:-2] # in cm
			# removed ; from last record if empty, to allow allows same number of fields in file


			csv_record += '\n'

			csv_file.write(csv_record.encode('utf8'))

	total_downloaded += num_to_download
# End while loop for multiple chunks.

csv_file.close()

print 'Done!'

