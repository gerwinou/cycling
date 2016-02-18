setwd("~/Documents/Data Analysis/")
library(ggplot2)
library(XML)
filename <-"data/cycling/activity_1023323355.tcx"

doc <- xmlParse(filename, useInternalNodes = TRUE)
#top <- xmlRoot(doc)

path = toString.XMLNode(top[[1]][[1]][[3]][[10]])
xml_extract = doc[[path]]

ds<-data.frame(starttime=xpathSApply(xml_extract, "//Lap", xmlGetAttr, "StartTime"),
    #      name=xpathSApply(xml_extract, "//COMPARISON/NAME", xmlValue),
    #      dich_name=xpathSApply(xml_extract, "//COMPARISON/DICH_SUBGROUP/NAME", xmlValue),
    #      ci_end=xpathSApply(xml_extract, "//COMPARISON/DICH_SUBGROUP/DICH_DATA", xmlGetAttr, "CI_END"),
    #      ci_end=xpathSApply(xml_extract, "//COMPARISON/DICH_SUBGROUP/DICH_DATA", xmlGetAttr, "CI_START")
)