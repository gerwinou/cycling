setwd("~/Documents/Data Analysis/")
library(ggplot2)
library(XML)
filename <-"data/cycling/activity_1023323355.tcx"

doc <- xmlParse(filename, useInternalNodes = TRUE)
top <- xmlRoot(doc)

# Note that the data is taken from a lap, which is the third node in the XML.
# If there is only one lap in the file, the [[3]] should be replaced by a [[2]]

# Another limitation is that position is not correctly recorded
data=toString.XMLNode(top[[1]][[1]][[3]][[10]])
df=as.data.frame(xmlToDataFrame(data))
#with (df,plot(Cadence))
#title(main="title")
  
dev.off
    
# with type, line, dot, step etc. can be configured
plot(df$HeartRateBpm)
title(main="Heartrate during ride")
#,xlab("datapoints"),ylab("HeartRate"))
#xlab("datapoints")
#ylab("HeartRate")
  #points(df$HeartRateBpm,col="blue",pch=1)
#points(df$Cadence,col="red",pch=8)
#legend("topright",pch=c(17,8),col=c("blue","red"),legend=c("HR","Cadence"))


