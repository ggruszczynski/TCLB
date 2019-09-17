source("lib/lattice.R")

x = c(0,1,-1);
P = expand.grid(x=0:2,y=0:2,z=0:2)
U = expand.grid(x,x,x)


######DEFINE DENSITIES######
# Use g for velocity based population.
gname = paste0("g", P$x, P$y, P$z)
AddDensity(
	name 	= gname,
	dx   	= U[,1],
	dy	= U[,2],
	dz	= U[,3],
	comment	= paste0("Hydrodynamic population g",1:27-1),
	group	= "g"
)
# Use h for interface population.
hname = paste0("h", P$x, P$y, P$z)
AddDensity(
	name 	= hname,
	dx   	= U[,1],
	dy	= U[,2],
	dz	= U[,3],
	comment	= paste0("Allen-Cahn population h",1:27-1),
	group	= "h"
)

if (Options$OutFlow){
	AddDensity( name=paste("gold",0:26,sep=""), dx=0,dy=0,dz=0,group="gold")
	AddDensity( name=paste("hold",0:26,sep=""), dx=0,dy=0,dz=0,group="hold")
}

AddDensity(name="U", dx=0, dy=0, dz=0, group="Vel")
AddDensity(name="V", dx=0, dy=0, dz=0, group="Vel")
AddDensity(name="W", dx=0, dy=0, dz=0, group="Vel")

AddDensity(name="nw_x", dx=0, dy=0, dz=0, group="nw")
AddDensity(name="nw_y", dx=0, dy=0, dz=0, group="nw")
AddDensity(name="nw_z", dx=0, dy=0, dz=0, group="nw")

AddField("PhaseF",stencil3d=1, group="PF")

if (Options$OutFlow){
	for (d in rows(DensityAll)) {
		AddField( name=d$name, dx=-d$dx-1, dy=-d$dy, dz=-d$dz )
	}
	# Assuming outflow from x-boundary
	AddField(name="U",dx=c(-1,0,0))
}

if (Options$RT){
	AddDensity(name="PhaseF_old",dx=0, dy=0, dz=0, group="PF")
}

if (Options$filter){
	AddField( name="U", stencil3d=1 ) 
	AddField( name="V", stencil3d=1 ) 
	AddField( name="W", stencil3d=1 ) 
}

######DEFINE STAGES and ACTIONS######
# Stages - processes to run for initialisation and each iteration
AddStage("PhaseInit" , "Init", save=Fields$name=="PhaseF")
AddStage("WallInit"  , "Init_wallNorm", save=Fields$group=="nw")
AddStage("calcWall"  , "calcWallPhase", save=Fields$name=="PhaseF", load=DensityAll$group=="nw")

if (Options$OutFlow){
    AddStage("BaseInit"  , "Init_distributions", save=Fields$group %in% c("g","h","Vel","gold","hold","PF"))
    AddStage("calcPhase" , "calcPhaseF",	 save=Fields$name=="PhaseF", 
                                                 load=DensityAll$group %in% c("g","h","Vel","gold","hold","nw"))
    AddStage("BaseIter"  , "Run"       ,         save=Fields$group %in% c("g","h","Vel","nw","gold","hold","nw"), 
	                                         load=DensityAll$group %in% c("g","h","Vel","nw","gold","hold","nw"))
} else { 
    AddStage("BaseInit"  , "Init_distributions", save=Fields$group %in% c("g","h","Vel","PF"))
    AddStage("calcPhase" , "calcPhaseF",	 save=Fields$name=="PhaseF", 
					         load=DensityAll$group %in% c("g","h","Vel","nw") )
    AddStage("BaseIter"  , "Run"       ,         save=Fields$group %in% c("g","h","Vel","nw"), 
	                                	 load=DensityAll$group %in% c("g","h","Vel","nw"))
}
AddAction("Iteration", c("BaseIter", "calcPhase", "calcWall"))
AddAction("Init"     , c("PhaseInit","WallInit" , "calcWall","BaseInit"))

######DEFINE OUTPUTS######
AddQuantity(name="Rho",unit="kg/m3")
AddQuantity(name="PhaseField",unit="1")
AddQuantity(name="U",	  unit="m/s",vector=T)
AddQuantity(name="P",	  unit="Pa")
AddQuantity(name="Normal", unit=1, vector=T)
######DEFINE INPUTS######
# Inputs: Fluid Properties
AddSetting(name="tau_l", comment='relaxation time (low density fluid)')
AddSetting(name="tau_h", comment='relaxation time (high density fluid)')
AddSetting(name="Viscosity_l", tau_l='(3*Viscosity_l)', default=0.16666666, comment='kinematic viscosity')
AddSetting(name="Viscosity_h", tau_h='(3*Viscosity_h)', default=0.16666666, comment='kinematic viscosity')
AddSetting(name="Density_h", default=1, comment='High density')
AddSetting(name="Density_l", default=1, comment='Low  density')
AddSetting(name="VelocityX", default=0.0, comment='inlet/outlet/init velocity', zonal=T)
AddSetting(name="VelocityY", default=0.0, comment='inlet/outlet/init velocity', zonal=T)
AddSetting(name="VelocityZ", default=0.0, comment='inlet/outlet/init velocity', zonal=T)
AddSetting(name="Pressure" , default=0.0, comment='inlet/outlet/init density', zonal=T)
AddSetting(name="GravitationX", default=0.0, comment='applied (rho)*GravitationX')
AddSetting(name="GravitationY", default=0.0, comment='applied (rho)*GravitationY')
AddSetting(name="GravitationZ", default=0.0, comment='applied (rho)*GravitationZ')
AddSetting(name="BuoyancyX", default=0.0, comment='applied (rho_h-rho)*BuoyancyX')
AddSetting(name="BuoyancyY", default=0.0, comment='applied (rho_h-rho)*BuoyancyY')
AddSetting(name="BuoyancyZ", default=0.0, comment='applied (rho_h-rho)*BuoyancyZ')
# Inputs: Interface Properties
AddSetting(name="PhaseField_h", default=1, comment='PhaseField in Liquid')
AddSetting(name="PhaseField_l", default=0, comment='PhaseField gas')
AddSetting(name="PhaseField", default=1, comment='Initial PhaseField distribution', zonal=T)
AddSetting(name="IntWidth", default=5, comment='Anti-diffusivity coeff')
AddSetting(name="omega_phi", comment='one over relaxation time (phase field)')
AddSetting(name="M", omega_phi='1.0/(3*M+0.5)', default=0.02, comment='Mobility')
AddSetting(name="sigma", default=1e-5, comment='surface tension')
# Inputs: Three point interface Properties
AddSetting(name="ContactAngle", radAngle='ContactAngle*3.1415926535897/180', default=90, comment='Contact angle in degrees', zonal=T)
AddSetting(name="radAngle", comment='Conversion to rads for calcs')
# Inputs: Domain initialisation
AddSetting(name="RTI_Characteristic_Length", default=-999, comment='Use for RTI instability')

AddSetting(name="Radius", default="0.0", comment='Diffuse Sphere Radius')
AddSetting(name="CenterX", default="0.0", comment='Diffuse sphere center_x')
AddSetting(name="CenterY", default="0.0", comment='Diffuse sphere center_y')
AddSetting(name="CenterZ", default="0.0", comment='Diffuse sphere center_z')
AddSetting(name="BubbleType",default="1.0", comment='droplet(1.0) or bubble(-1.0)?!')

AddSetting(name="DonutTime", default="0.0", comment='Radius of a Torus - initialised to travel along x-axis')
AddSetting(name="Donut_h",   default="0.0", comment='Half donut thickness, i.e. the radius of the cross-section')
AddSetting(name="Donut_D",   default="0.0", comment='Dilation factor along the x-axis')
AddSetting(name="Donut_x0",  default="0.0", comment='Position along x-axis')

# Velocity Tracking on Centerline:
#AddSetting(name="xyzTrack", default=1,comment='x<-1, y<-2, z<-3')
#AddNodeType("Centerline",group="ADDITIONALS")
#AddNodeType("Edgeline",group="ADDITIONALS")
# Allow for smoothing of sharp interface initiation by diffusion
AddNodeType("Smoothing",group="ADDITIONALS")
#  For RTI interface tracking
#AddNodeType("Spiketrack",group="ADDITIONALS")
#AddNodeType("Saddletrack",group="ADDITIONALS")
#AddNodeType("Bubbletrack",group="ADDITIONALS")

AddNodeType(name="MovingWall_N", group="BOUNDARY")
AddNodeType(name="MovingWall_S", group="BOUNDARY")
AddNodeType(name="NVelocity", group="BOUNDARY")
if (Options$CM){
AddNodeType(name="CM", group="COLLISION")
}
if (Options$OutFlow){
AddNodeType(name="ENeumann", group="BOUNDARY")
AddNodeType(name="EConvect", group="BOUNDARY")
}
#AddGlobal("InterfacePositionOne",comment='trackPosition - of low /high density interface')
#AddGlobal("InterfacePositionTwo",comment='trackPosition - of high/low  density interface')
#AddGlobal("Vfront",comment='velocity infront of bubble')
#AddGlobal("Vback",comment='velocity behind bubble')
#AddGlobal("RTISpike", comment='SpikeTracker ')
#AddGlobal("RTIBubble",comment='BubbleTracker')
#AddGlobal("RTISaddle",comment='SaddleTracker')

# Globals - table of global integrals that can be monitored and optimized
#AddGlobal(name="PressureLoss", comment='pressure loss', unit="1mPa")
#AddGlobal(name="OutletFlux", comment='pressure loss', unit="1m2/s")
#AddGlobal(name="InletFlux", comment='pressure loss', unit="1m2/s")
AddGlobal(name="BubbleFront", op="MAX", comment='Maximum location in X direction of interface')
AddGlobal(name="TotalDensity", comment='Mass conservation check', unit="1kg/m3")
AddGlobal(name="KineticEnergy",comment='Measure of kinetic energy', unit="J")

#AddGlobal(name="GasTotalVelocity", comment='use to determine avg velocity of bubbles', unit="m/s")
AddGlobal(name="GasTotalVelocityX", comment='use to determine avg velocity of bubbles', unit="m/s")
AddGlobal(name="GasTotalVelocityY", comment='use to determine avg velocity of bubbles', unit="m/s")
AddGlobal(name="GasTotalVelocityZ", comment='use to determine avg velocity of bubbles', unit="m/s")
AddGlobal(name="GasCells",	   comment='use in line with GasTotalVelocity to determine average velocity', unit="1")
AddGlobal(name="CoM_X", comment='Centre of mass in X')
AddGlobal(name="CoM_Y", comment='Centre of mass in Y')
AddGlobal(name="CoM_Z", comment='Centre of mass in Z')
