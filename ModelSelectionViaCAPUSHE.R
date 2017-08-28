library(capushe)
#data(datacapushe)
#capushe(datacapushe)
#plot(capushe(datacapushe))

setwd('desktop');
getwd();
#setwd('EMAlgo');

library(xlsx)
data=read.xlsx(file="Slope\ heuristics\ data.xls",sheetIndex =1, header=TRUE)
ddse = DDSE(data)
djump = Djump(data)

plot(capushe(data))




plot(ddse)
pdf(file="DDSEonNIPSAdjustedEM.pdf",width=8.5,height=11) 

savePlotpdfdev.off()

png(filename="DDSEonNIPSAdjustedEM.pdf")

summary(ddse)
summary(djump)
