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