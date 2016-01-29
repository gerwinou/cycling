setwd("~/Documents/Data Analysis/cycling")
library(plyr)
library(ggplot2)
library(lubridate)

garminReport <-"data/activities.csv"
temp <- read.csv(garminReport,sep=";",dec = ",",na.strings = "",header=T)

temp$BeginTimestamp<-as.Date(temp$BeginTimestamp)
data<-temp[order(temp$BeginTimestamp),]

data$Date <- as.Date(data$BeginTimestamp)
maxHR <- ddply(data,.(year(Date)),transform, m=MaxHeartRate) 

p <- ggplot(maxHR, aes(x = year(Date), y = m, color = factor(year(Date)))) 
p <- p + geom_point(size = 3) 
p <- p + xlab("Year")
p <- p + ylab("Max Heart Rate")  
p <- p + ggtitle("Max Heart Rate over the years")
p <- p + scale_color_discrete(name = "Legend (Year)")
p