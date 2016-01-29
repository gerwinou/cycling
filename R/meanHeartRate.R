setwd("~/Documents/Data Analysis/cycling")
library(plyr)
library(ggplot2)
library(lubridate)
library(scales)

garminReport <-"data/activities.csv"
data <- read.csv(garminReport,sep=";",dec = ",",na.strings = "",header=T)

data$BeginTimestamp<-as.Date(data$BeginTimestamp)
data<-data[order(data$BeginTimestamp),]
data$Date <- as.Date(data$BeginTimestamp)
avgHR <- ddply(data,.(year(Date)),transform, mHR=mean(AverageHeartRate,na.rm = TRUE))

p<-ggplot(avgHR, aes(x = year(Date), y = mHR, color = factor(year(Date)))) 
#p<-ggplot(avgHR, aes(x = year(BeginTimestamp), y = mHR, color = factor(year(BeginTimestamp))))
p <- p + geom_point(size = 5)
p <- p + xlab("year")
p <- p + ylab("Avg Heart Rate")  
p <- p + ggtitle("Average Heart Rate over the years")
p <- p + scale_color_discrete(name = "Legend (Year)")
p <- p + scale_y_continuous(breaks=seq(round(min(avgHR$mHR)),round(max(avgHR$mHR)),3))  # Ticks from min to max, every 1
#p<- p + scale_x_date(labels = date_format("%m"), breaks = date_breaks("months"))
#p <- p + text(6,2,row.names(avgHR$mHR))
p <- p + axis(1,at = seq(2009,2016, by = 1))
p
