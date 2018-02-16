#setwd("~/TCLB/")
setwd("D:/STUDIA/MEIL_MGR/MSc/WYNIKI_optymalizacja/mix_last1000_50k_eps_2T")
#setwd("/media/muaddieb/Worker/LBM/WYNIKI_optymalizacja/mix_last1000_50k_eps_2T/")
rm(list=ls()) # clear the workspace
#MovingWallVelocity-MW_optimalControl
stab = read.csv("probka.csv", header = FALSE)
ster= t(stab[stab$V1 == "SET",-1]) # -1 - skip first column

title1 = paste("Optimal Lid Velocity in subsequent iterations")
matplot(ster, type="l", main=title1, xlab="time steps", ylab="u",cex.lab=1.4, cex.axis=1.4, cex.main=1.4)
grid(nx = NULL, ny = NULL, col = "lightgray", lty = "dotted")

n <- 20 # optimization iteration
eps <- 1E+3#1E-0 # weight of work
title2 = paste("Optimal Lid Velocity \n ",n," optimization iterations \n 'weight of work' = ",eps)
matplot(ster[,n], type="l", main=title2, xlab="time steps", ylab="u",cex.lab=1.4, cex.axis=1.4, cex.main=1.4)
grid(nx = NULL, ny = NULL, col = "lightgray", lty = "dotted")

# grad = t(stab[stab$V1 == "GRAD",-1]) # -1 - skip first column
# matplot(grad[,n], type="l", main="grad", xlab="time steps", ylab="grad",cex.lab=1.4, cex.axis=1.4, cex.main=1.4)

# ostatnie$x <- ster[,20]
# ostatnie$t <-  # write.csv(ostatnie, file = "MyData.csv",row.names=FALSE)
# 
# smoke$x <- matrix(c(ster[,20]),ncol=1)
# 
# smoke <- matrix(c(51,43,22,92,28,21,68,22,9),ncol=1)
# smoke[2,] <-matrix(c(51,43,22,92,28,21,68,22,9),ncol=1)
# colnames(smoke) <- c("High","Low")

####################################################
# require(data.table) # library containing fread
# ftab = fread("MovingWallVelocity-MW_optimalControl.csv" , header = FALSE)
# fter = t(ftab[ftab$V1 == "SET",-1]) # -1 - skip first column

# cos = tab[tab$V1 == "SET",-1]
# fcos = ftab[ftab$V1 == "SET",-1]
