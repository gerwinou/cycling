setwd("/Users/gb/logs/")
library(ggplot2)
library(reshape2)

hr <-"heartbeat.csv"
hrset <- read.csv(hr,sep=":",dec = ".",na.strings = "NV",header=T)
#res <-melt(hrset,id.vars=c("zone0Min","zone1Min","zone2Min","zone3Min"))

x <-hrset[,c("date","zone0Cal","zone1Cal","zone2Cal","zone3Cal")]

res <-melt(x)

p4 <-ggplot() + geom_col(aes(y=value,x=date,fill =variable),data=res)