setwd("~/Documents/Data Analysis/cycling")
library(plyr)
library(ggplot2)
library(lubridate)

garminReport <-"data/activities.csv"
temp <- read.csv(garminReport,sep=";",dec = ",",na.strings = "",header=T)

# Note: 2012 has a very high outlier

temp$BeginTimestamp<-as.Date(temp$BeginTimestamp)
data<-temp[order(temp$BeginTimestamp),]
cbPalette <- c("#CAA9A7", "#CAA9A7", "#CAA9A7", "#CAA9A7", "#CAA9A7", "#CAA9A7", "#CAA9A7", "#CAA9A7","#CAA9A7")
data$Date <- as.Date(data$BeginTimestamp)
avgSpeed <- ddply(data,.(year(Date)),transform, m=mean(AverageSpeed))
ggplot(avgSpeed, aes(x = month(Date,label=FALSE,abbr=FALSE), y = m, color = factor(year(Date)))) + geom_line(size=2)

