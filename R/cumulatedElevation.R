setwd("~/Documents/Data Analysis/")
library(plyr)
library(ggplot2)
library(lubridate)

# Note: some rows have no value, in this case the cumsum function stops at the last value, hence the plot stops there as well

garminReport <-"data/cycling/activities.csv"
data <- read.csv(garminReport,sep=";",dec = ",",na.strings = "",header=T)

data$BeginTimestamp<-as.Date(data$BeginTimestamp)
data<-data[order(data$BeginTimestamp),]

data$Date <- as.Date(data$BeginTimestamp)
cumu <- ddply(data,.(year(Date)),transform, cumElevation = cumsum(ElevationGain))

p <- ggplot(cumu, aes(x = week(Date), y = cumElevation, color = factor(year(Date)))) + geom_line(size=2)
p <- p + xlab("Weeks") + xlim(0,52)
 
p <- p + ggtitle("Cumulated elevation, per year")
p <- p + scale_color_discrete(name = "Legend (Year)")
p <- p + scale_y_continuous(breaks=seq(round(min(cumu$cumElevation)),round(max(cumu$cumElevation)),2500))  # Ticks from min to max, every 1
p