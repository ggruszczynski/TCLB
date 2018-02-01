# Model for solving the wave equation as a system of first order DE's
# u'' = c(u_xx + u_yy)

AddField(name="u", dx=c(-1,1), dy=c(-1,1)) # same as AddField(name="u", stencil2d=1)
AddField(name="v", dx=c(-1,1), dy=c(-1,1))

AddQuantity(name="U")

AddSetting(name="Speed")
AddSetting(name="Viscosity")
AddSetting(name="Value", zonal=TRUE)

AddNodeType(name="Dirichlet", group="BOUNDARY")
