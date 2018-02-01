# Model for solving the convection-diffusion equation:
# phi' = -U * grad(phi) + c*lap(phi)
# phi' = -[ux,uy]' * [phi_x,phi_y] + c * (phi_xx + phi_yy)

AddField(name="phi", dx=c(-1,1), dy=c(-1,1)) # same as AddField(name="phi", stencil2d=1)
AddQuantity(name="Phi")

AddSetting(name="ux", comment="free stream velocity")
AddSetting(name="uy", comment="free stream velocity")
AddSetting(name="diff_coeff")
AddSetting(name="Value", zonal=TRUE)

AddNodeType(name="Dirichlet", group="BOUNDARY")
