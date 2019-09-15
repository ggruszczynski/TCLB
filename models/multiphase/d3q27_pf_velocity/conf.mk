ADJOINT=0
TEST=FALSE
OPT="(OutFlow+BGK+CM+RT)*autosym"
# OutFlow: convective and neumann BC for east facing in x plane are 
# 	   implemented, but require additional memory access so 
# 	   are left as an option.
# BGK: If for some reason a single relaxation time is desired for the 
#      hydrodynamic population then use this.
# CM: Casaded operator, in the hope that this may improve stability
#     in more dynamic flows.
# RT: Ren Temporal Correction
#	Utilises the previous velocity and phase value at each cell
#	to ensure consistency of recovered Allen-Cahn eqn.
