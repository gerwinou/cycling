import fitbitFunctions as f

start = '2016-01-10'
end = '2016-01-31'

def main():

    res = f.getHeartbeatSeries(start, end)
    print res

if __name__ == "__main__":
    main()
