setwd("~/Documents/Data Analysis/data/cycling")
library(plyr)
library(ggplot2)
library(lubridate)
library(scales)

garminReport <-"activities.csv"
gdata <- read.csv(garminReport,sep=";",dec = ",",na.strings = "",header=T)

plot(jitter(gdata$AverageHeartRate) ~ jitter(gdata$AverageSpeed))
regrline <- lm(gdata$AverageHeartRate ~ AverageSpeed,gdata)
abline(regrline, lwd=3, col="red")
summary(regrline)