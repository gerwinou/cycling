

setwd("~/Documents/Data Analysis/")

library(XML)
filename <-"data/cycling/activity_1023323355.tcx"

doc <- xmlParse(filename, useInternalNodes = TRUE)
top <- xmlRoot(doc)

data=toString.XMLNode(top[[1]][[1]][[3]][[10]])
df=as.data.frame(xmlToDataFrame(data))
#plot(df$Cadence)
dfI <- as.integer(df$Cadence)
p <- ggplot(df) 

p <-p + geom_line(size=2)
# p <- p + theme(panel.background = element_rect(fill = 'green', colour = 'red'))
p <- p + theme_bw()
p <- p + xlab("Month")
p <- p + ylab("Avg Distance")  
p <- p + ggtitle("Average Distance per ride over the years")
p <- p + scale_color_discrete(name = "Legend (Year)")
#p <- p + scale_x_date(date_breaks(width = "1 month"))
#p <- p + scale_y_continuous(breaks=seq(min(round(distance$Distance)),round(max(distance$Distance)),5))  # Ticks from min to max, every 1
p
