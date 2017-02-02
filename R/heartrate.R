setwd("/Users/gb/logs/")
library(ggplot2)
library(reshape2)
library(plyr)

# the following function is needed to plot multiple graphs on one page 
multiplot <- function(..., plotlist=NULL, cols) {
  require(grid)
  
  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)
  
  numPlots = length(plots)
  
  # Make the panel
  plotCols = cols                          # Number of columns of plots
  plotRows = ceiling(numPlots/plotCols) # Number of rows needed, calculated from # of cols
  
  # Set up the page
  grid.newpage()
  pushViewport(viewport(layout = grid.layout(plotRows, plotCols)))
  vplayout <- function(x, y)
    viewport(layout.pos.row = x, layout.pos.col = y)
  
  # Make each plot, in the correct location
  for (i in 1:numPlots) {
    curRow = ceiling(i/plotCols)
    curCol = (i-1) %% plotCols + 1
    print(plots[[i]], vp = vplayout(curRow, curCol ))
  }
  
}


# declare the file to read
hr1 <-"heartbeat3.csv" 

# read it in as a dataset
hrset1 <- read.csv(hr1,sep=":",dec = ".",na.strings = "NV",header=T) 

# Define the date field as a date in the correct format
hrset1$date <-as.Date( hrset1$date, format="%Y-%m-%d")

# discard unneeded columns by keeping the needed ones, and putting them in the right order
y1 <-hrset1[,c("date","zone3Cal","zone2Cal","zone1Cal","zone0Cal")]

# melt the data to get the desired long format
res1 <-melt(y1,id.vars = c("date"),variable.name = "Zone",value.name = "Calories")

# subset the data into separate sets per month
x1 <-res1[format.Date(res1$date,"%m")=="01",]
x2 <-res1[format.Date(res1$date,"%m")=="02",]
x5 <-res1[format.Date(res1$date,"%m")=="05",]

#x1 <-hrset1[format.Date(hrset1$date,"%m")=="01",c("date","zone3Cal","zone2Cal","zone1Cal","zone0Cal")]
#x2 <-hrset1[format.Date(hrset1$date,"%m")=="02",c("date","zone3Cal","zone2Cal","zone1Cal","zone0Cal")]

# melt the data to get the desired long format
#res1 <-melt(x1,id.vars = c("date"),variable.name = "Zone",value.name = "Calories")
#res2 <-melt(x2,id.vars = c("date"),variable.name = "Zone",value.name = "Calories")

# plot as a stacked plot, per month
p1 <-ggplot() + geom_col(aes(y=Calories,x=format(date, "%d"),fill =Zone),data=x1)
p2 <-ggplot() + geom_col(aes(y=Calories,x=format(date,"%d"),fill =Zone),data=x2)
p5 <-ggplot() + geom_col(aes(y=Calories,x=format(date,"%d"),fill =Zone),data=x5)


multiplot(p1, p2, p5,cols=2)