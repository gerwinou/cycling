setwd("~/Downloads/IGI_templates/")

library(rjson)
library(jsonlite)
library(RCurl)
#library(RJSONIO)

json_file <- "http://uinames.com/api/?region=netherlands&amount=250"
document <- fromJSON(json_file)

#dat <- do.call(rbind, lapply(document$features, 
                            # function(x) data.frame(x$properties)))