
setwd("~/Documents/Data Analysis/")
library(ggplot2)
library(XML)
library(plyr)

filename <-"data/cycling/activity_1023323355.tcx"
doc <- xmlParse(filename)
#class(doc)
#xmltop = xmlRoot(doc)
#name <-xmlName(xmltop)
#size <- xmlSize(xmltop)
#n1<- xmlName(xmltop[[1]])
tracks <- xmltop[['Activities']][['Activity']][['Lap']]
test <-ldply(xmlToList(tracks), data.frame)