import fitbitFunctions as f
import json
import logging

start = '2016-01-15'
end = '2016-01-25'

logging.config.fileConfig('fitbitlogging.conf')
logger = logging.getLogger('fitbitClient')


def main():

    res = f.getHeartbeatSeries(start, end)
    a = json.loads(res)

    lengte = len(a["activities-heart"])
    #print(lengte)
    #print a["activities-heart"][k]["value"]["heartRateZones"][0]["caloriesOut"]

    dt  = "NV"
    rhr = "NV"
    zone0_name = "Out of Range"
    zone0_caloriesOut = "NV"
    zone0_minutes = "NV"

    for i in range(lengte):
        try:
            dt  = a["activities-heart"][i]["dateTime"]
            rhr = a["activities-heart"][i]['value']["restingHeartRate"]
            zone0_caloriesOut = a["activities-heart"][i]["value"]["heartRateZones"][0]["caloriesOut"]
            zone0_minutes = a["activities-heart"][i]["value"]["heartRateZones"][0]["minutes"]


        except KeyError as e:
            logger.debug(e)
            #print e

        print (dt + ":" + str(rhr) + ":" + str(zone0_caloriesOut) + ":" + str(zone0_minutes))


if __name__ == "__main__":
    main()
