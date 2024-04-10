ADJOINT=0
TEST=FALSE
OPT="(Outflow+debug)*autosym"

# debug: Enables tracking of momentum and force globals 

# Boundary Conditions:
# Outflow: 
# 	This is used for outflow boundaries, it is made as an
# 	option as it requires additional fields for calculations
# 	so results in a slower code.
# autosym:
# 	Allows symmetry node type flags introduced in v6.2
