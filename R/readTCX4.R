setwd("~/Documents/Data Analysis/")

library(XML)
filename <-"data/cycling/activity_1023323355.tcx"
doc <- xmlParse(filename, useInternalNodes = T)


top <- xmlRoot(doc)

data=top[[1]][[1]][[3]][[10]][[1]]

ds<- as.data.frame(xmlToDataFrame(data))


