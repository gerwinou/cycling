setwd("~/Documents/Data Analysis/cycling")
library(plyr)
library(ggplot2)
library(lubridate)

garminReport <-"data/activities.csv"
temp <- read.csv(garminReport,sep=";",dec = ",",na.strings = "",header=T)

temp$Begin.Timestamp<-as.Date(temp$Begin.Timestamp)
data<-temp[order(temp$Begin.Timestamp),]
#data$Date <- as.Date(data$Date)
#cumu <- ddply(data,.(year(Date)),transform, cumRain = cumsum(Rainfall))
#ggplot(cumu, aes(x = month(Date,label=FALSE,abbr=TRUE), y = cumRain, color = factor(year(Date)))) + geom_line() 

data$Date <- as.Date(data$Begin.Timestamp)
cumu <- ddply(data,.(year(Date)),transform, cumDistance = cumsum(Distance))
#ggplot(cumu, aes(x = month(Date,label = TRUE, abbr= FALSE), y = cumDistance, color = factor(year(Date)))) + geom_crossbar(aes(ymin=0,ymax=600))
#ggplot(cumu, aes(x = month(Date,label = TRUE, abbr= FALSE), y = cumDistance, color = factor(year(Date)))) + geom_smooth(aes(group=1))
#ggplot(cumu, aes(x = months(Date,label=TRUE,abbr = TRUE), y = cumDistance, color = factor(year(Date)))) + geom_line()
ggplot(cumu, aes(x = week(Date), y = cumDistance, color = factor(year(Date)))) + geom_line()


#data$Date <- as.Date(data$Date)
#cumu <- ddply(data,.(year(Date)),transform, cumRain = cumsum(Rainfall))
#ggplot(cumu, aes(x = yday(Date), y = cumRain, color = factor(year(Date)))) + geom_line() 


#data$year <- as.numeric(format(as.Date(data$Date), format="%Y"))
#ddply(data,.(year),transform,cumRain = cumsum(Rainfall))->cumu
#ggplot(cumu, aes(Date,cumRain))+geom_point() 