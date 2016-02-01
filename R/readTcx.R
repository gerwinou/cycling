setwd("~/Documents/Data Analysis/")

library(XML)
filename <-"data/cycling/activity_1023323355.gpx"

doc <- xmlParse(filename, useInternalNodes = TRUE)
top <- xmlRoot(doc)
title=toString.XMLNode(top[[2]][[1]][[1]])
description=toString.XMLNode(top[[2]][[2]][[1]])
data=toString.XMLNode(top[[2]][[3]])
#names(top["trk"][[1]][[2]])

if(data=="NULL") data=toString.XMLNode(top[[2]][[2]])
if(data=="NULL") data=toString.XMLNode(top[[2]][[1]])

# Fill a data frame with interesting data
df=as.data.frame(xmlToDataFrame(data,c("numeric", "character", "integer")))
if(toString.XMLNode(top[[2]][[3]])=="NULL") {
  if(toString.XMLNode(top[[2]][[2]])=="NULL") {
    attribs=xmlSApply(top[[2]][[1]],xmlAttrs)
  }else{
    attribs=xmlSApply(top[[2]][[2]],xmlAttrs)
  }
}else{
  attribs=xmlSApply(top[[2]][[3]],xmlAttrs)
}
df$lon=as.numeric(attribs[1,])
df$lat=as.numeric(attribs[2,])
colnames(df)=c("Elevation","DateTime","HeartRate", "Longitude","Latitude")
df$Elevation=as.numeric(df$Elevation)
df$HeartRate=as.integer(df$HeartRate)
#df$cad=as.integer(df$cad)
df$DateTime=as.character(df$DateTime)
# Convert timestamp to number of seconds since start of run
date=substr(df$DateTime[1],1,10)
Time=substr(df$DateTime,12,19)
T0=strptime(Time[1],"%H:%M:%S")
Time=as.numeric(strptime(Time,"%H:%M:%S")-T0)
df$Seconds=Time

# Initialise columns
df$dNorth=0; df$dEast=0; df$dUp=0;
df$North=0; df$East=0; df$dDist=0; 
df$dDist2D=0; df$Dist2D=0
