setwd("~/Documents/Data Analysis/")
library(plyr)
library(ggplot2)
library(lubridate)

garminReport <-"data/cycling/activities.csv"
temp <- read.csv(garminReport,sep=";",dec = ",",na.strings = "",header=T)

temp$BeginTimestamp<-as.Date(temp$BeginTimestamp)
data<-temp[order(temp$BeginTimestamp),]
data$Date <- as.Date(data$BeginTimestamp)
cumu <- ddply(data,.(year(Date)),transform, cumDistance = cumsum(Distance))

ggplot(cumu, aes(x = week(Date), y = cumDistance, color = factor(year(Date)))) 

p <-ggplot(cumu, aes(x = week(Date), y = cumDistance, color = factor(year(Date)))) 
p <- p + geom_line(size=2)
p <- p + xlab("Weeks") + xlim(0,52)
##p <- p + ylab("Distance") + ylim(0,3000) 
p <- p + ggtitle("Cumulated distance, per year")
p <- p + scale_color_discrete(name = "Legend (Year)")
p <- p + scale_y_continuous(breaks=seq(round(min(cumu$cumDistance)),round(max(cumu$cumDistance)),1000))  # Ticks from min to max, every 1

p

