import fitbitFunctions as f
import json
import logging

start = '2016-01-22'
end = '2016-01-23'

logging.config.fileConfig('fitbitlogging.conf')
logger = logging.getLogger('fitbitClient')
sep = ":"

def main():

    res = f.getHeartbeatSeries(start, end)
    a = json.loads(res)

    lengte = len(a["activities-heart"])
    #print(lengte)
    #print a["activities-heart"][k]["value"]["heartRateZones"][0]["caloriesOut"]

    dt  = "NV"
    rhr = "NV"
    #zone0_name = "Out of Range"
    zone0_caloriesOut = "NV"
    zone0_minutes = "NV"

    #zone0_name = "Fat Burn"
    zone1_caloriesOut = "NV"
    zone1_minutes = "NV"

    #zone0_name = "Cardio"
    zone2_caloriesOut = "NV"
    zone2_minutes = "NV"

    #zone0_name = "Peak"
    zone3_caloriesOut = "NV"
    zone3_minutes = "NV"


    for i in range(lengte):
        dt  = a["activities-heart"][i]["dateTime"]

        try:
            rhr = a["activities-heart"][i]['value']["restingHeartRate"]
        except KeyError as e:
            logger.debug(e)

        try:
            zone0_caloriesOut = int(a["activities-heart"][i]["value"]["heartRateZones"][0]["caloriesOut"])
        except KeyError as e:
            logger.debug(e)

        try:
            zone0_minutes = a["activities-heart"][i]["value"]["heartRateZones"][0]["minutes"]
        except KeyError as e:
            logger.debug(e)

        try:
            zone1_caloriesOut = int(a["activities-heart"][i]["value"]["heartRateZones"][1]["caloriesOut"])
        except KeyError as e:
            logger.debug(e)

        try:
            zone1_minutes = a["activities-heart"][i]["value"]["heartRateZones"][1]["minutes"]
        except KeyError as e:
            logger.debug(e)

        try:
            zone2_caloriesOut = int(a["activities-heart"][i]["value"]["heartRateZones"][2]["caloriesOut"])
        except KeyError as e:
            logger.debug(e)

        try:
            zone2_minutes = a["activities-heart"][i]["value"]["heartRateZones"][2]["minutes"]
        except KeyError as e:
            logger.debug(e)

        try:
            zone3_caloriesOut = int(a["activities-heart"][i]["value"]["heartRateZones"][3]["caloriesOut"])
        except KeyError as e:
            logger.debug(e)

        try:
            zone3_minutes = a["activities-heart"][i]["value"]["heartRateZones"][3]["minutes"]
        except KeyError as e:
            logger.debug(e)

        resultstring = dt + sep + str(rhr) + sep + str(zone0_caloriesOut) + sep + str(zone0_minutes)
        resultstring += sep + str(zone1_caloriesOut) + sep + str(zone1_minutes)
        resultstring += sep + str(zone2_caloriesOut) + sep + str(zone2_minutes)
        resultstring += sep + str(zone3_caloriesOut) + sep + str(zone3_minutes)
        #print (dt + ":" + str(rhr) + ":" + str(zone0_caloriesOut) + ":" + str(zone0_minutes))
        print(resultstring)

if __name__ == "__main__":
    main()
