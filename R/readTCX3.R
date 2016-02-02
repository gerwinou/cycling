

setwd("~/Documents/Data Analysis/")

library(XML)
filename <-"data/cycling/activity_1023323355.tcx"

doc <- xmlParse(filename, useInternalNodes = TRUE)
top <- xmlRoot(doc)

data=toString.XMLNode(top[[1]][[1]][[3]][[10]])
df=as.data.frame(xmlToDataFrame(data))
plot(df$Cadence)