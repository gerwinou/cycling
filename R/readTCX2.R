library(XML)
filename <-"data/cycling/activity_1023323355.gpx"

doc <- xmlParse(filename, useInternalNodes = TRUE)
top <- xmlRoot(doc)
title=toString.XMLNode(top[[2]][[1]][[1]])
description=toString.XMLNode(top[[2]][[2]][[1]])
data=toString.XMLNode(top[[2]][[2]])

df=as.data.frame(xmlToDataFrame(data,c("numeric", "character", "integer")))

attribs=xmlSApply(top[[2]][[2]],xmlAttrs)
attribs1=xmlSApply(top[[2]][[2]][[2]],xmlAttrs)