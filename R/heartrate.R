setwd("/Users/gb/logs/")
library(ggplot2)
library(reshape2)
library(plyr)

# using a custom function from the file below for multiplotting
# putting function in file can be done with dump
source("myFunctions.R")

# declare the file to read
hr <-"heartbeat.csv" 

# read it in as a dataset, define date as Date, and all else as numeric. colClasses is not ideal, look for alt.
hrset <- read.csv(hr,sep=":",dec = ".",na.strings = "NV",header=T,colClasses=c('Date',rep('numeric',9)))
#hrset <- read.csv(hr,sep=":",dec = ".",na.strings = "NV",header=T) 


# Define the date field as a date in the correct format
# hrset$date <-as.Date( hrset$date, format="%Y-%m-%d")

# discard unneeded columns by keeping the needed ones, and putting them in the right order
y <-hrset[,c("date","zone3Cal","zone2Cal","zone1Cal","zone0Cal")]

# melt the data to get the desired long format
res <-melt(y,id.vars = c("date"),variable.name = "Zone",value.name = "Calories")

# subset the data into separate sets per month
x1 <-res[format.Date(res$date,"%m")=="01",]
x2 <-res[format.Date(res$date,"%m")=="02",]
x3 <-res[format.Date(res$date,"%m")=="03",]
x4 <-res[format.Date(res$date,"%m")=="04",]
x5 <-res[format.Date(res$date,"%m")=="05",]

# plot as a stacked plot, per month
p1 <-ggplot() + geom_col(aes(y=Calories,x=format(date, "%d"),fill =Zone),data=x1)
p1 <-p1 + labs(x = "January")

p2 <-ggplot() + geom_col(aes(y=Calories,x=format(date,"%d"),fill =Zone),data=x2)
p2 <-p2 + labs(x = "February")

p3 <-ggplot() + geom_col(aes(y=Calories,x=format(date,"%d"),fill =Zone),data=x3)
p3 <-p3 + labs(x = "March")

p4 <-ggplot() + geom_col(aes(y=Calories,x=format(date,"%d"),fill =Zone),data=x4)
p4 <-p4 + labs(x = "April")

p5 <-ggplot() + geom_col(aes(y=Calories,x=format(date,"%d"),fill =Zone),data=x5)
p5 <-p5 + labs(x = "May")


multiplot(p1, p2, p3, p4, p5,cols=2)
