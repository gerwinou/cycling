setwd("/Users/gb/logs/")
library(ggplot2)
library(reshape2)
library(plyr)

# using a custom function from the file below for multiplotting
# putting function in file can be done with dump
source("myFunctions.R")

# declare the file to read
hr2 <-"heartbeat.csv" 

# read it in as a dataset, define date as Date, and all else as numeric. colClasses is not ideal, look for alt.
hrset2 <- read.csv(hr2,sep=":",dec = ".",na.strings = "NV",header=T,colClasses=c('Date',rep('numeric',9)))

# discard unneeded columns by keeping the needed ones, and putting them in the right order
hrset2 <-hrset2[,c("date","resthr")]

# melt the data to get the desired long format
#res <-melt(hrset,id.vars = c("date"),variable.name = "Zone",value.name = "Calories")

# subset the data into separate sets per month
y1 <-hrset2[format.Date(hrset2$date,"%m")=="01",]
y2 <-hrset2[format.Date(hrset2$date,"%m")=="02",]
y3 <-hrset2[format.Date(hrset2$date,"%m")=="03",]
y4 <-hrset2[format.Date(hrset$date,"%m")=="04",]
y5 <-hrset2[format.Date(hrset$date,"%m")=="05",]
y6 <-hrset2[format.Date(hrset$date,"%m")=="06",]
y7 <-hrset2[format.Date(hrset$date,"%m")=="07",]
y8 <-hrset2[format.Date(hrset$date,"%m")=="08",]
y9 <-hrset2[format.Date(hrset$date,"%m")=="09",]
y10 <-hrset2[format.Date(hrset$date,"%m")=="10",]
y11 <-hrset2[format.Date(hrset$date,"%m")=="11",]
y12 <-hrset2[format.Date(hrset$date,"%m")=="12",]

lowEnd = 48
highEnd = 63
# plot as a line plot, per month
#q1 <-ggplot() + geom_hline(aes(y=resthr,x=format(date,"%d")),data=y1)
q1 <-ggplot() + geom_line(data = y1,aes(x=date, y=resthr))
q1 <-q1 + labs(x = "January")
q1<- q1 +ylim(c(lowEnd,highEnd))

q2 <-ggplot() + geom_line(data = y2,aes(x=date, y=resthr))
q2 <-q2 + labs(x = "February")
q2<- q2 +ylim(c(lowEnd,highEnd))

q3 <-ggplot() + geom_line(data = y3,aes(x=date, y=resthr))
q3 <-q3 + labs(x = "March")
q3<- q3 +ylim(c(lowEnd,highEnd))

q4 <-ggplot() + geom_line(data = y4,aes(x=date, y=resthr))
q4 <-q4 + labs(x = "April")
q4<- q4 +ylim(c(lowEnd,highEnd))

q5 <-ggplot() + geom_line(data = y5,aes(x=date, y=resthr))
q5 <-q5 + labs(x = "May")
q5<- q5 +ylim(c(lowEnd,highEnd))

q6 <-ggplot() + geom_line(data = y6,aes(x=date, y=resthr))
q6 <-q6 + labs(x = "Juni")
q6<- q6 +ylim(c(lowEnd,highEnd))

q7 <-ggplot() + geom_line(data = y7,aes(x=date, y=resthr))
q7 <-q7 + labs(x = "July")
q7<- q7 +ylim(c(lowEnd,highEnd))

q8 <-ggplot() + geom_line(data = y8,aes(x=date, y=resthr))
q8 <-q8 + labs(x = "August")
q8<- q8 +ylim(c(lowEnd,highEnd))

q9 <-ggplot() + geom_line(data = y9,aes(x=date, y=resthr))
q9 <-q9 + labs(x = "September")
q9<- q9 +ylim(c(lowEnd,highEnd))

q10 <-ggplot() + geom_line(data = y10,aes(x=date, y=resthr))
q10 <-q10 + labs(x = "October")
q10<- q10 +ylim(c(lowEnd,highEnd))

q11 <-ggplot() + geom_line(data = y11,aes(x=date, y=resthr))
q11 <-q11 + labs(x = "November")
q11<- q11 +ylim(c(lowEnd,highEnd))

q12 <-ggplot() + geom_line(data = y12,aes(x=date, y=resthr))
q12 <-q12 + labs(x = "December")
q12<- q12 +ylim(c(lowEnd,highEnd))

multiplot(q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, cols=2)
