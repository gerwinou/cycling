setwd("~/Documents/Data Analysis/")
library(ggplot2)

strava_effort1 <-"data/cycling/speed2.csv"
#data1 <- read.csv(strava_effort1,sep=",",dec = ".",na.strings = "",header=T)

strava_effort2 <-"data/cycling/heartrate.csv"
data2 <- read.csv(strava_effort2,sep=",",dec = ".",na.strings = "",header=T)

test <- data.frame(
  distance = data2$distance,
  altitude = data2$altitude
)

g<-ggplot(test,aes(x=distance,y=altitude)) + geom_area(color='grey', fill = 'lightgrey', alpha = 0.5)
g