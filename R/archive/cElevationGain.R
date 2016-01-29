setwd("~/Documents/Data Analysis/cycling")

require(ggplot2)
require(reshape2)

garminReport <-"data/activities.csv"
garmin <- read.csv(garminReport,sep=";",dec = ",",na.strings = "",header=T)

el2015 = strftime(garmin$Begin.Timestamp,"%Y") == 2015
el2015sub = subset(garmin,subset = el2015)

el2014 = strftime(garmin$Begin.Timestamp,"%Y") == 2014
el2014sub = subset(garmin,subset = el2014)

months = strftime(el2015sub$Begin.Timestamp,"%m")

dd <- data.frame(months, cumsum(el2015sub$Distance)) 
dd.agg <- aggregate(el2015sub$Distance ~ months, dd, FUN = sum)
#dd.agg <- aggregate(amt ~ mo + yr, dd, FUN = sum)
#plot ((dd.agg))
#ggplot(aes(x='month',y='distance'),data = dd.agg) + geom_line()
#df <- data.frame(events= 1:83,y2015=cumsum(el2015sub$Distance),y2014=cumsum(el2014sub$Distance))
#df <- melt(df,id.vars = 'events', variable.name = 'Year')
#ggplot(df,aes(events,value )) + geom_jitter(aes(colour = Year))
#ggplot(df,aes(events,value )) + geom_jitter(aes(colour = Year))
#plot.ts(df)
