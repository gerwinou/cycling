setwd("/Users/gb/logs/")
library(ggplot2)
library(reshape2)
library(plyr)
library(gridExtra)
library(lubridate)

# using a custom function from the file below for multiplotting
# putting function in file can be done with dump
# function is deprecated however because of the use of gridExtra
source("myFunctions.R")

# declare the file to read
hr2 <-"heartbeat.csv" 

# read it in as a dataset, define date as Date, and all else as numeric. colClasses is not ideal, look for alt.
hrset2 <- read.csv(hr2,sep=":",dec = ".",na.strings = "NV",header=T,colClasses=c('Date',rep('numeric',9)))

# discard unneeded columns by keeping the needed ones, and putting them in the right order
hrset2 <-hrset2[,c("date","resthr")]

# declare constants for bottom and top of graph
lowEnd = 45
highEnd = 65

# function to subset the data
subSetter <-
  function(ds, monthnumber){
    ds[format.Date(ds$date,"%m") == monthnumber,]
  }

# function to plot the graphs
plotter <-
  function(dSet){
    ggplot() + geom_line(data = dSet,aes(x=date, y=resthr))  + labs(x = month(dSet$date, label=TRUE,abbr = FALSE)) + ylim(c(lowEnd,highEnd))
  }

# subset the data into separate sets per month
lijst <- c("01","02","03","04","05","06","07","08","09","10","11","12")# attempt to put everything in a loop (failed so far)

  


y1 = subSetter(hrset2,"01")
y2 = subSetter(hrset2,"02")
y3 = subSetter(hrset2,"03")
y4 = subSetter(hrset2,"04")
y5 = subSetter(hrset2,"05")
y6 = subSetter(hrset2,"06")
y7 = subSetter(hrset2,"07")
y8 = subSetter(hrset2,"08")
y9 = subSetter(hrset2,"09")
y10 = subSetter(hrset2,"10")
y11 = subSetter(hrset2,"11")
y12 = subSetter(hrset2,"12")

# plot as a line plot, per month
q1 = plotter(y1)
q2 = plotter(y2)
q3 = plotter(y3)
q4 = plotter(y4)
q5 = plotter(y5)
q6 = plotter(y6)
q7 = plotter(y7)
q8 = plotter(y8)
q9 = plotter(y9)
q10 = plotter(y10)
q11 = plotter(y11)
q12 = plotter(y12)

grid.arrange(q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12,ncol=2)