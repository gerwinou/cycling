import datetime
import os



csv_filename = '../data/activities.csv'

if csv_filename:
    timestamp = str(datetime.date.today())
    print(timestamp)
    os.rename(csv_filename, csv_filename + "." + timestamp)