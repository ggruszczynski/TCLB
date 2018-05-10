## Model for d2q9 SRT BKG-LBM
#     Density - performs streaming operation for us
#	

# Add the particle distribution functions as model Densities:
AddDensity( name="f[0]", dx= 0, dy= 0)
AddDensity( name="f[1]", dx= 1, dy= 0)
AddDensity( name="f[2]", dx= 0, dy= 1)
AddDensity( name="f[3]", dx=-1, dy= 0)
AddDensity( name="f[4]", dx= 0, dy=-1)
AddDensity( name="f[5]", dx= 1, dy= 1)
AddDensity( name="f[6]", dx=-1, dy= 1)
AddDensity( name="f[7]", dx=-1, dy=-1)
AddDensity( name="f[8]", dx= 1, dy=-1)

# Add the quantities we wish to be exported
#    These quantities must be defined by a function in Dynamics.c
AddQuantity( name="U",unit="m/s", vector=TRUE )
AddQuantity( name="Rho",unit="kg/m3" )

# Add the settings which describes system constants defined in a .xml file
AddSetting( name="omega",     comment='inverse of relaxation time')
AddSetting( name="viscosity", omega='1.0/(3*viscosity+0.5)',       default=0.16666666, comment='kinematic viscosity')

AddSetting( name="omega_bulk", comment='inverse of bulk relaxation time')
AddSetting( name="bulk_visc",  omega_bulk='1.0/(3*bulk_visc+0.5)', default=0.16666666, comment='bulk viscosity')

AddSetting( name="Velocity_x",default=0, comment='inlet/outlet/init velocity in x', zonal=TRUE )
AddSetting( name="Velocity_y",default=0, comment='inlet/outlet/init velocity in y', zonal=TRUE )
AddSetting( name="GravitationX",default=0, comment='body/external acceleration', zonal=TRUE)
AddSetting( name="GravitationY",default=0, comment='body/external acceleration', zonal=TRUE)
AddSetting( name="Density",default=1, comment='Density')

AddNodeType(name="EPressure", group="BOUNDARY")
AddNodeType(name="WPressure", group="BOUNDARY")
AddNodeType(name="WVelocity", group="BOUNDARY")
AddNodeType(name="EVelocity", group="BOUNDARY")
