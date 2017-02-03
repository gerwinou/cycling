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
hr <-"heartbeat.csv" 

# read it in as a dataset
hrset <- read.csv(hr,sep=":",dec = ".",na.strings = "NV",header=T) 

# Define the date field as a date in the correct format
hrset$date <-as.Date( hrset$date, format="%Y-%m-%d")

# discard unneeded columns by keeping the needed ones, and putting them in the right order
y <-hrset[,c("date","zone3Cal","zone2Cal","zone1Cal","zone0Cal")]

# melt the data to get the desired long format
res <-melt(y,id.vars = c("date"),variable.name = "Zone",value.name = "Calories")

# subset the data into separate sets per month
x1 <-res[format.Date(res$date,"%m")=="01",]
x2 <-res[format.Date(res$date,"%m")=="02",]
x3 <-res[format.Date(res$date,"%m")=="03",]
x4 <-res[format.Date(res$date,"%m")=="04",]
x5 <-res[format.Date(res$date,"%m")=="05",]

# plot as a stacked plot, per month
p1 <-ggplot() + geom_col(aes(y=Calories,x=format(date, "%d"),fill =Zone),data=x1)
p1 <-p1 + labs(x = "January")

p2 <-ggplot() + geom_col(aes(y=Calories,x=format(date,"%d"),fill =Zone),data=x2)
p2 <-p2 + labs(x = "February")

p3 <-ggplot() + geom_col(aes(y=Calories,x=format(date,"%d"),fill =Zone),data=x3)
p3 <-p3 + labs(x = "March")

p4 <-ggplot() + geom_col(aes(y=Calories,x=format(date,"%d"),fill =Zone),data=x4)
p4 <-p4 + labs(x = "April")

p5 <-ggplot() + geom_col(aes(y=Calories,x=format(date,"%d"),fill =Zone),data=x5)
p5 <-p5 + labs(x = "May")


multiplot(p1, p2, p3, p4, p5,cols=2)