
#setwd("~/TCLB/")
setwd("D:/STUDIA/MEIL_MGR/MSc/WYNIKI_reference/Filip_ref/output_FilipRefCase/")

#setwd("E:/LBM/WYNIKI_optymalizacja")
rm(list=ls()) # clear the workspace


#tab = read.csv("lid_withVeloControl_Log_P00_00000000.csv")
#tab = read.csv("lid_constVelo_100k_v0000_Log_P00_00000000.csv")
#tab = read.csv("REF_ADJ_50k_Sin2T_50k_v0100_Log_P00_00000000.csv")

tab = read.csv("Filip_refCase_Log_P00_00000000.csv")

#tab = read.csv("lid_Log_Sin2Pi_50k_velo0100.csv")

plot(tab$Iteration,tab$NMovingWallForce,type="l",
     main="Force", xlab="time steps", ylab="F")
grid(nx = NULL, ny = NULL, col = "lightgray", lty = "dotted")

plot(tab$Iteration,tab$TotalTempSqr/tab$CountCells,type="l",
     main="Mix quality", xlab="time steps", ylab="mix quality")
grid(nx = NULL, ny = NULL, col = "lightgray", lty = "dotted")

#plot(tab$Iteration,tab$SWallForce,type="l")

plot(tab$Iteration,tab$MovingWallVelocity.DefaultZone,type="l",
     main="Lid Velocity", xlab="time steps", ylab="u")
grid(nx = NULL, ny = NULL, col = "lightgray", lty = "dotted")


plot(tab$Iteration,tab$MovingWallPower,type="l",
     main="Power", xlab="time steps", ylab="power")
grid(nx = NULL, ny = NULL, col = "lightgray", lty = "dotted")

plot(tab$Iteration,cumsum(tab$MovingWallPower)*tab$Iteration[1], type="l",
     main="Cumulative Work", xlab="time steps", ylab="cumulative work")
grid(nx = NULL, ny = NULL, col = "lightgray", lty = "dotted")


work = sum(tab$MovingWallPower)*tab$Iteration[1]
mix_quality = tail(tab$TotalTempSqr, n=1) / tail(tab$CountCells, n=1) 
