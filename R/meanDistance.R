setwd("~/Documents/Data Analysis/cycling")
library(plyr)
library(ggplot2)
library(lubridate)

garminReport <-"data/activities.csv"
temp <- read.csv(garminReport,sep=";",dec = ",",na.strings = "",header=T)

temp$BeginTimestamp<-as.Date(temp$BeginTimestamp)
data<-temp[order(temp$BeginTimestamp),]
data$Date <- as.Date(data$BeginTimestamp)
distance <- ddply(data,.(year(data$Date)),transform, m=mean(Distance))


p <- ggplot(distance, aes(x = month(data$Date,label=FALSE,abbr=TRUE), y = m, color = factor(year(Date)))) 

p <-p + geom_line(size=2)
# p <- p + theme(panel.background = element_rect(fill = 'green', colour = 'red'))
p <- p + theme_bw()
p <- p + xlab("Month")
p <- p + ylab("Avg Distance")  
p <- p + ggtitle("Average Distance per ride over the years")
p <- p + scale_color_discrete(name = "Legend (Year)")
#p <- p + scale_x_date(date_breaks(width = "1 month"))
p <- p + scale_y_continuous(breaks=seq(min(round(distance$Distance)),round(max(distance$Distance)),5))  # Ticks from min to max, every 1
p

