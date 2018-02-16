#setwd("~/TCLB/Wyniki_R")
setwd("D:/STUDIA/MEIL_MGR/MSc/WYNIKI_optymalizacja/mix_last1000_50k_eps_2T")
#setwd("/media/muaddieb/Worker/LBM/WYNIKI_optymalizacja/mix_last1000_50k_eps_2T")

rm(list=ls()) # clear the workspace
opttab = read.csv("optimalMixing_50k_eps1E_5_Log_P00_00000000.csv")


plot(opttab$Iteration, opttab$TotalTempSqr/opttab$CountCells, col=opttab$Optimization,
     main="Mix quality ZLEEE in subsequent optimization cycles", xlab="iteration", ylab="mix quality",cex.lab=1.4, cex.axis=1.4, cex.main=1.4) 
grid(nx = NULL, ny = NULL, col = "lightgray", lty = "dotted")

plot(opttab$Iteration, opttab$MovingWallPower, col=opttab$Optimization,
     main="Work in subsequent optimization cycles", xlab="iteration", ylab="work",cex.lab=1.4, cex.axis=1.4, cex.main=1.4) 
grid(nx = NULL, ny = NULL, col = "lightgray", lty = "dotted")

plot(opttab$Iteration, opttab$MovingWallPower/(126*127*1000), col=opttab$Optimization,
     main="Work_norm in subsequent optimization cycles", xlab="iteration", ylab="work_norm",cex.lab=1.4, cex.axis=1.4, cex.main=1.4) 
grid(nx = NULL, ny = NULL, col = "lightgray", lty = "dotted")

plot(opttab$Iteration, -opttab$Objective/(126*127*1000), col=opttab$Optimization, 
     main="Objective in subsequent optimization cycles", xlab="iteration", ylab="Objective",cex.lab=1.4, cex.axis=1.4, cex.main=1.4)# dzielimy przez liczbe komorek 126*127 i ostatnie 250 iteracji z ktorych bierzemy wage
grid(nx = NULL, ny = NULL, col = "lightgray", lty = "dotted")

lastTab=aggregate(opttab, list(opttab$Optimization), tail, 1)
# plot(-lastTab$Objective/(126*127*1000),  main="Objective - final value", xlab="optimization number", ylab="Objective",cex.lab=1.4, cex.axis=1.4, cex.main=1.4)
# grid(nx = NULL, ny = NULL, col = "lightgray", lty = "dotted")

WeightWorks_norm = lastTab$MovingWallPowerInObj.MW * lastTab$MovingWallPower/(126*127*1000)  #(lastTab$Objective - lastTab$MovingWallPowerInObj.MW * lastTab$MovingWallPower)
Temps_norm = (lastTab$Objective - lastTab$MovingWallPowerInObj.MW * lastTab$MovingWallPower)/(126*127*1000)
J = WeightWorks_norm + Temps_norm

plot (-WeightWorks_norm, main="Work with weight - final value", xlab="optimization number", ylab="work",cex.lab=1.4, cex.axis=1.4, cex.main=1.4) 
grid(nx = NULL, ny = NULL, col = "lightgray", lty = "dotted")

plot(-Temps_norm, main=" Mix quality = \n Mix quality - final value", xlab="optimization number", ylab="mix quality",cex.lab=1.4, cex.axis=1.4, cex.main=1.4)
grid(nx = NULL, ny = NULL, col = "lightgray", lty = "dotted")

plot(-J, main="Objective - final value", xlab="optimization number", ylab="J",cex.lab=1.4, cex.axis=1.4, cex.main=1.4)
grid(nx = NULL, ny = NULL, col = "lightgray", lty = "dotted")

plot (c(0,20),c(0,0.14),type="n", # sets the x and y axes scales 
      main="Objective and components",
      xlab="optimization cycle",ylab="Objective", # adds titles to the axes
      cex.lab=1.4, cex.axis=1.4, cex.main=1.4) # scales the font
points(lastTab$Group.1,-J,col="red",lwd=2.5) # adds a line for J
points(lastTab$Group.1,-Temps_norm,col="blue",lwd=2.5) # adds a line for mix quality
points(lastTab$Group.1,-WeightWorks_norm,col="green",lwd=2.5) # adds a line for work
legend(14, 0.14, # places a legend at the appropriate place 
       c("objective","mix quality", "work with weight"), # puts text in the legend 
       lty=c(1,1,1), # gives the legend appropriate symbols (lines)
       lwd=c(2.5,2.5,2.5),col=c("red","blue","green"), cex=1.1) # gives the legend lines the correct color and width
grid(nx = NULL, ny = NULL, col = "lightgray", lty = "dotted")

# plot(-WeightWorks_norm, -Temps_norm, main="mixQuality(work) in subsequent optimization cycles", xlab="work", ylab="mix quality")
# grid(nx = NULL, ny = NULL, col = "lightgray", lty = "dotted")


lastJ= -J[20]
lastWork = lastTab$MovingWallPower[20]
lastMixQuality = -Temps_norm[20]
lastWork_norm = -WeightWorks_norm[20]

# lastTab$MovingWallPowerInObj.MW[20]* lastWork_norm + lastMixQuality
# 
 firstJ= -J[1]
 firstWork = lastTab$MovingWallPower[1]
 firstMixQuality = -Temps_norm[1]

##################################################3