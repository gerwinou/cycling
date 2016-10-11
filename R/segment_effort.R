setwd("~/Documents/Data Analysis/")
library(plyr)
library(ggplot2)
library(lubridate)

# Note: some rows have no value, in this case the cumsum function stops at the last value, hence the plot stops there as well

strava_effort1 <-"data/cycling/1588450431.csv"
data1 <- read.csv(strava_effort1,sep=",",dec = ".",na.strings = "",header=T)

strava_effort2 <-"data/cycling/3330852149.csv"
data2 <- read.csv(strava_effort2,sep=",",dec = ".",na.strings = "",header=T)

plot(data1$heartrate,type="o",col='red')
lines(data2$heartrate,type="o",col='blue')

plot(data1$velocity,type="o",col='orange')
lines(data2$velocity,type="o",col='green')