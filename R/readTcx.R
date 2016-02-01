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
colnames(df)=c("Elevation","DateTime","HeartRate","Longitude","Latitude")
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

# Haversine formula is appropriate for calculating distances from lat/long
EarthRad=6371000
haverDist<-function(aLong,aLat,bLong,bLat){
  dLat=2*pi*(bLat-aLat)/360.0; dLon=2*pi*(bLong-aLong)/360.0
  a=(sin(dLat/2))^2+cos(2*pi*aLat/360)*cos(2*pi*bLat/360)*(sin(dLon/2)^2)
  return(EarthRad*2*atan2(sqrt(a),sqrt(1-a)))
}

# Calculate northings and eastings
df$East=haverDist(df[1,"Longitude"],df[1,"Latitude"],df$Longitude,df[1,"Latitude"])*sign(df$Longitude-df[1,"Longitude"])
df$North=haverDist(df[1,"Longitude"],df[1,"Latitude"],df[1,"Longitude"],df$Latitude)*sign(df$Latitude-df[1,"Latitude"])

# Calculate changes in position for each dt
for (x in 2:(length(df$DateTime)-1)) {
  sEast=sign(df[x,"Longitude"]-df[1,"Longitude"])
  sNorth=sign(df[x,"Latitude"]-df[1,"Latitude"])
  df$dEast[x]=sEast*haverDist(df[x-1,"Longitude"],df[1,"Latitude"],df[x,"Longitude"],df[1,"Latitude"])
  df$dNorth[x]=sNorth*haverDist(df[1,"Longitude"],df[x-1,"Latitude"],df[1,"Longitude"],df[x,"Latitude"])
  df$dUp[x]=df$Elevation[x]-df$Elevation[x-1]
  # 2D distance (ignoring hills)
  df$dDist2D[x]=haverDist(df[x-1,"Longitude"],df[x-1,"Latitude"],df[x,"Longitude"],df[x,"Latitude"])
}

df$dDist=sqrt(df$dNorth^2+df$dEast^2+df$dUp^2)
df$Dist=cumsum(df$dDist)
df$Dist2D=cumsum(df$dDist2D)

# Fit a spline function to the GPS coordinates & elevation
east=splinefun(df$Seconds,df$East)
north=splinefun(df$Seconds,df$North)
up=splinefun(df$Seconds,df$Elevation)
dist=splinefun(df$Seconds,df$Dist)
hr=approxfun(df$Seconds,df$HeartRate) # Some gaps in heart rate record, linear interpolation more robust

# Do finite centred differencing to give smoothest rate/gradient estimates
df$Speed=rep(0,length(df$Seconds))
df$Gradient=rep(0,length(df$Seconds))
for(x in 2:(length(df$Seconds)-1)){
  Dt=df[x+1,"Seconds"]-df[x-1,"Seconds"]
  Dd=df[x+1,"Dist"]-df[x-1,"Dist"]
  df[x,"Speed"]=Dd/Dt # m/s
  df[x,"Gradient"]=(df[x+1,"Elevation"]-df[x-1,"Elevation"])/Dd # m/m
}
df[1,"Speed"]=df[2,"Speed"]
df[length(df$Seconds),"Speed"]=df[length(df$Seconds)-1,"Speed"]
df[1,"Gradient"]=df[2,"Gradient"]
df[length(df$Seconds),"Gradient"]=df[length(df$Seconds)-1,"Gradient"]

# Smooth speed as it is unrealistically noisy
df$Speed=smooth(df$Speed)

# Fit a spline function to rate
speed=splinefun(df$Seconds,df$Speed)
pace<-function(t) sapply(1/speed(t),max,0)
ppace<-function(t) 1000*pace(t)/60

# Update dataframe with speed and pace
df$Speed=speed(df$Seconds)
df$Pace=pace(df$Seconds)