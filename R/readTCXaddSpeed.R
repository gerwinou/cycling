setwd("~/Documents/Data Analysis/")
library(ggplot2)
library(XML)
library(plyr)

#filename <-"data/cycling/activity_1023323355.tcx" # Dijkrondje
filename <-"data/cycling/activity_820645325.tcx" # Stelvio
doc <- xmlParse(filename)

nodes <- getNodeSet(doc, "//ns:Trackpoint", "ns")

mydf <- plyr::ldply(nodes, as.data.frame(xmlToList)) 

# The following method does not work, as the order of the data varies. This seems a problem of plyr, not the Garmin file 
#mydf<-setNames(mydf,c('time','distance','bpm','cadence','lat','long','alt'))

mydf<-rename(mydf, c("value.Value"="bpm", "value.Cadence"="cadence"))

mydf$distance <- as.integer(as.character(mydf$value.DistanceMeters))
mydf$alt <- as.integer(as.character(mydf$value.AltitudeMeters))
mydf$time <- as.POSIXct(mydf$value.Time, format='%Y-%m-%dT%H:%M:%S.000Z')

mydf$distdiff <- c("NA", diff(mydf$distance))
mydf$timediff <- c("NA", diff(mydf$time))
mydf$altdiff <- c("NA", diff(mydf$alt))

mydf$distdiff <- as.integer(mydf$distdiff)
mydf$timediff <- as.integer(mydf$timediff)
mydf$altdiff <- as.integer(mydf$altdiff)

mydf$speed <- (mydf$distdiff / mydf$timediff) * 3.6
mydf$slope <- (mydf$altdiff / mydf$distdiff)
mydf$climbspeed <- (mydf$altdiff) / mydf$timediff

#qplot(distance,alt,data=mydf2)
#g <- ggplot(mydf,aes(distance,speed))
g <- ggplot()
#g<- g + geom_point(alpha=0.3, color="red") 
#g<- g + geom_line(data =mydf,aes(x=distance,y=speed))
#g<- g + geom_line(data =mydf,aes(x=distance,y=alt, color="blue"))
g<- g + geom_line(data =mydf,aes(x=distance,y=speed, color="blue"))
#g<- g + geom_line(data =mydf,aes(x=distance,y=speed, color="red"))
#g<- g + geom_smooth(method="lm")
g<- g + geom_smooth()
g
