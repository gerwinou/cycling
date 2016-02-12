setwd("~/Documents/Data Analysis/")
library(ggplot2)
library(XML)
library(plyr)

filename <-"data/cycling/activity_1023323355.tcx"
doc <- xmlParse(filename)

#

nodes <- getNodeSet(doc, "//ns:Trackpoint", "ns")
mydf <- plyr::ldply(nodes, as.data.frame(xmlToList)) 
mydf<-setNames(mydf,c('time','lat','long','alt','distance','bmp','cadence'))

mycols <-c("alt","distance")
mydf2<- mydf[mycols]
mydf2$alt<-as.integer(as.character(mydf2$alt))
                 
mydf2$distance<-as.integer(as.character(mydf2$distance))

#qplot(distance,alt,data=mydf2)
#g <- ggplot(mydf2,aes(distance,alt))
#g<- g + geom_point(alpha=0.3, color="red") 
#g<- g + geom_line()
#g<- g + geom_smooth(method="lm")
#g<- g + geom_smooth()
#g