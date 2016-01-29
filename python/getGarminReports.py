# https://connect.garmin.com/modern/proxy/userstats-service/activities/monthly/gerwinou?fromMonthStartDate=2009-01-03&untilMonthStartDate=2012-12-28&metricId=3&grpParentActType=false&actTypeId=2
# python gcexport.py -d ~/MyActivities -c all -f original  --username gerwinou --password []


from urllib import urlencode
from datetime import datetime
from getpass import getpass
from sys import argv
from os.path import isdir
from os.path import isfile
from os import mkdir
from os import remove
from xml.dom.minidom import parseString

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

# parser.add_argument('-d', '--directory', nargs='?', default=activities_directory,
#	help="the directory to export to (default: './YYYY-MM-DD_garmin_connect_export')")

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

print 'Welcome to Garmin Connect Report Generator.'

# Create directory for data files.
#if isdir(args.directory):
#	print 'Warning: Output directory already exists. Will skip already-downloaded files and append to the CSV file.'

username = args.username if args.username else raw_input('Username: ')
password = args.password if args.password else getpass()

# Maximum number of activities you can request at once.  Set and enforced by Garmin.
limit_maximum = 100

# URLs for various services.
url_gc_login     = 'https://sso.garmin.com/sso/login?service=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&webhost=olaxpw-connect04&source=https%3A%2F%2Fconnect.garmin.com%2Fen-US%2Fsignin&redirectAfterAccountLoginUrl=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&redirectAfterAccountCreationUrl=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&gauthHost=https%3A%2F%2Fsso.garmin.com%2Fsso&locale=en_US&id=gauth-widget&cssUrl=https%3A%2F%2Fstatic.garmincdn.com%2Fcom.garmin.connect%2Fui%2Fcss%2Fgauth-custom-v1.1-min.css&clientId=GarminConnect&rememberMeShown=true&rememberMeChecked=false&createAccountShown=true&openCreateAccount=false&usernameShown=false&displayNameShown=false&consumeServiceTicket=false&initialFocus=true&embedWidget=false&generateExtraServiceTicket=false'
url_gc_post_auth = 'https://connect.garmin.com/post-auth/login?'
# url_gc_search    = 'http://connect.garmin.com/proxy/activity-search-service-1.0/json/activities?'
# url_gc_gpx_activity = 'http://connect.garmin.com/proxy/activity-service-1.1/gpx/activity/'
# url_gc_tcx_activity = 'http://connect.garmin.com/proxy/activity-service-1.1/tcx/activity/'
url_gc_original_activity = 'http://connect.garmin.com/proxy/download-service/files/activity/'

USERNAME = args.username
PASSWORD = args.password

# MetricID  1 = calories (in joules)
# MetricID  2 = avg cadence
# MetricID  3 = avg heartrate
# MetricID  4 = avg pace
# MetricID  5 = heartrate

# MetricID  7 = avg speed
# MetricID 13 = max heartrate

# MetricID 16 = # of activities
# MetricID 17 = total distance
# MetricID 18 = total duration

url_gc_report = 'https://connect.garmin.com/modern/proxy/userstats-service/activities/weekly/'+ USERNAME + '?fromWeekStartDate=2009-01-01&untilWeekStartDate=2016-01-04&metricId=2&grpParentActType=true'
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

# The following should become a function that gets the data per metric, now it is only doing cadence, filename should be adapted accordingly

METRIC_ID = str(2) # Get avg cadence per week
url_gc_report = 'https://connect.garmin.com/modern/proxy/userstats-service/activities/weekly/'+ USERNAME + '?fromWeekStartDate=1970-01-01' \
																										   '&untilWeekStartDate=2016-01-04' \
																										   '&metricId='+ METRIC_ID+'' \
																																   '&grpParentActType=true'

result = http_req(url_gc_report)
json_results = json.loads(result)  # TODO: Catch possible exceptions here.


csv_filename = '../data/cadence.csv'
csv_file = open(csv_filename, 'w')
csv_file.write('startDateOfWeek,avgCadence\n')

# Pull out just the list of activities.
activities = json_results['groupedMetrics']['cycling']['metricsMap']['ACTIVITY_AVERAGE_BIKE_CADENCE']

for a in activities:
		#print a
		# Display which entry we're working on.
		#print 'Garmin Connect startDateOfWeek: ' + a['startDateOfWeek']
		#print a['value']
		csv_file.write(a['startDateOfWeek']+','+ str(a['value']) + '\n')
		#print a['activity']['activityName']['value']
		#print '\t' + a['activity']['beginTimestamp']['display'] + ',',


print 'processing results ... '



#print result

# csv_filename = '../data/report.json'
# csv_file = open(csv_filename, 'w')
# csv_file.write(result)
csv_file.close()

print 'Done!'

