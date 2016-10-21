setwd("~/Documents/Data Analysis/")
library(ggplot2)

strava_effort1 <-"data/cycling/speed2.csv"
#data1 <- read.csv(strava_effort1,sep=",",dec = ".",na.strings = "",header=T)

strava_effort2 <-"data/cycling/heartrate.csv"
data2 <- read.csv(strava_effort2,sep=",",dec = ".",na.strings = "",header=T)

#plot(data1$effort.0,type="l",col='red')
#lines(data1$effort.1,type="l",col='red')
#par(new=TRUE)
#plot(data2$distance,type="l",col='green')
#par(new=TRUE)
plot(data2$altitude,type="l",
     col='darkgrey',
     xlab = "distance",
     ylab = "altitude",
     main = "Strava analysis",
     ylim = c(10,100),
     col.main = "darkgray",
     cex.axis = 0.6, # fontsize of the x-axis
     )
     
#par(new=TRUE)
#plot(data2$effort0,type="l",col='blue', xlab = "", ylab = "", ylim=c(110,180))
#lines(data2$effort1,type="l",col='orange')

#lines(data2$effort.4,type="o",col='black')
