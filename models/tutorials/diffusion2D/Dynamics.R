
AddField(name="u", dx=c(-1,1), dy=c(-1,1)) # same as AddField(name="u", stencil2d=1)


AddQuantity(name="U")

AddSetting(name="Speed")
AddSetting(name="Value", zonal=TRUE)

AddNodeType(name="Dirichlet", group="BOUNDARY")
