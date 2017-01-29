import fitbitFunctions as f
import json

start = '2016-01-01'
end = '2016-12-31'

def main():

    res = f.getHeartbeatSeries(start, end)
    a = json.loads(res)

    lengte = len(a["activities-heart"])
    #print(lengte)
    for i in range(lengte):
        try:
            dt  = a["activities-heart"][i]["dateTime"]
            rhr = a["activities-heart"][i]['value']["restingHeartRate"]

        except:
            rhr = "NV"
            #print a["activities-heart"][i]["dateTime"] + ";" + "NV"

        print (dt + ":" + str(rhr))


if __name__ == "__main__":
    main()
