setwd("~/Documents/Data Analysis/")
library(ggplot2)
library(ggmap)
library(XML)
library(plyr)

filename <-"aab/data/VISConfig.xml" # 6 tracks, with Mooker Schans, Zwarteweg, Brandenberg en Holdeurn
doc <- xmlParse(filename)

#nodes <- getNodeSet(doc, "//ns:Trackpoint", "ns")
nodes <- getNodeSet(doc,"ConfigurationItem")

mydf <- plyr::ldply(nodes, as.data.frame(xmlToList)) 