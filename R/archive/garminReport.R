plotsetwd("~/Documents/Data Analysis/cycling")
garminReport <-"data/activities.csv"
gReport <- read.csv(garminReport,sep=";",dec = ",",na.strings = "",header=T)

# mean(gReport$Max..Elevation, na.rm = TRUE) : calculate without missing values
#v <-gReport$Distance
#> v > 100 # returns all data bigger than 100
# sum (v>100) # returns number of elements bigger than 100
# plot(cumsum(v)) # plot the cumulative sum. Need to aggregate by month per year

# barplot(t(rowsum(gReport$Distance,strftime(gReport$Begin.Timestamp,"%Y/%m"))))
#> short.date = strftime(gReport$Begin.Timestamp,"%Y/%m")
#> aggr.stat = aggregate(gReport$Distance ~ short.date, FUN = sum) # this can not be plotted, because date is not numeric

#x <- as.POSIXct(c("2011-02-01", "2011-02-01", "2011-02-01"))
#mo <- strftime(x, "%m")
#yr <- strftime(x, "%Y")
#amt <- runif(3)
#dd <- data.frame(mo, yr, amt)

#dd.agg <- aggregate(amt ~ mo + yr, dd, FUN = sum)
# str(gReport) # shows structure

# testsub <-subset(gReport,gReport$Average.Heart.Rate==145)
# View(testsub)

# sub = strftime(gReport$Begin.Timestamp,"%Y") == 2015
# testsub = subset(gReport,subset = sub)

