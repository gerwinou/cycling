setwd("~/Documents/Data Analysis/")
library(ggplot2)
library(ggmap)
library(XML)
library(plyr)

filename <-"data/cycling/activity_1082141434.tcx" # 6 tracks, with Mooker Schans, Zwarteweg, Brandenberg en Holdeurn
doc <- xmlParse(filename)

nodes <- getNodeSet(doc, "//ns:Trackpoint", "ns")

mydf <- plyr::ldply(nodes, as.data.frame(xmlToList)) 

# The following method does not work, as the order of the data varies. This seems a problem of plyr, not the clas Garmin file 
#mydf<-setNames(mydf,c('time','distance','bpm','cadence','lat','long','alt'))

mydf<-rename(mydf, c("value.Value"="bpm", "value.Cadence"="cadence","value.Position.LongitudeDegrees"="lon","value.Position.LatitudeDegrees"="lat"))
mydf$lat<- as.integer(mydf$lat)
mydf$lon<- as.integer(mydf$lon)
mydf$distance <- as.integer(as.character(mydf$value.DistanceMeters))
mydf$alt <- as.integer(as.character(mydf$value.AltitudeMeters))
mydf$time <- as.POSIXct(mydf$value.Time, format='%Y-%m-%dT%H:%M:%S.000Z')

mydf$distdiff <- c("NA", diff(mydf$distance))
mydf$timediff <- c("NA", diff(mydf$time))
mydf$altdiff <- c("NA", diff(mydf$alt))

mydf$distdiff <- as.integer(mydf$distdiff)
mydf$timediff <- as.integer(mydf$timediff)
mydf$altdiff <- as.integer(mydf$altdiff)

mydf$speed <- (mydf$distdiff / mydf$timediff) * 3.6
mydf$slope <- (mydf$altdiff / mydf$distdiff)
mydf$climbspeed <- (mydf$altdiff) / mydf$timediff

longi <- c(5.5,6)
latit <- c(51.7,51.9)
df <- as.data.frame(cbind(longi,latit))

cords <- as.data.frame(cbind.data.frame(mydf$lon,mydf$lat))
cords<- rename(cords,c("mydf$lon"="lon","mydf$lat"="lat"))
# getting the map
mapgb<- get_map(location = c(lon = mean(df$longi), lat = mean(df$latit)), zoom = 11,maptype = "terrain", scale = 2)

# plotting the map with some points on it
ggmap(mapgb) + geom_point(data = cords, aes(x = cords$lon, y = cords$lat), color="red",size = 5, shape = 21) 
#ggmap(mapgb) + geom_line(data = cords, aes(x = lon, y = lat,color = "red",alpha = "0.8"), size = 5) 


# ggmap + guides(fill=FALSE, alpha=FALSE, size=FALSE)
