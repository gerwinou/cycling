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
hr1 <-"heartbeat.csv" 
hr2 <-"heartbeat2.csv" 


# read it in as a dataset
hrset1 <- read.csv(hr1,sep=":",dec = ".",na.strings = "NV",header=T) 
hrset2 <- read.csv(hr2,sep=":",dec = ".",na.strings = "NV",header=T) 

# subset only the desired data (calories per zone)
x1 <-hrset1[,c("date","zone3Cal","zone2Cal","zone1Cal","zone0Cal")]
x2 <-hrset2[,c("date","zone3Cal","zone2Cal","zone1Cal","zone0Cal")]

# melt the data to get the desired long format
res1 <-melt(x1,variable.name = "Zone",value.name = "Calories")
res2 <-melt(x2,variable.name = "Zone",value.name = "Calories")


# plot as a stacked plot
p1 <-ggplot() + geom_col(aes(y=Calories,x=date,fill =Zone),data=res1)
p2 <-ggplot() + geom_col(aes(y=Calories,x=date,fill =Zone),data=res2)

multiplot(p1, p2, cols=2)