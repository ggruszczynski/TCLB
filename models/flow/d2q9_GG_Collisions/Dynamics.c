/*-------------------------------------------------------------*/
/*  CLB - Cudne LB - Stencil Version                           */
/*     CUDA based Adjoint Lattice Boltzmann Solver             */
/*     Author: Lukasz Laniewski-Wollk                          */
/*     Developed at: Warsaw University of Technology - 2012    */
/*-------------------------------------------------------------*/

/*
Model created by Travis Mitchell 10-03-2016. Purpose of model is
to give an introduction into model creation in TCLB, tutorial 
file is available upon request.

Model solves d2q9 files via applying the single relaxation time
BGK-lattice Boltzmann method
*/

CudaDeviceFunction float2 Color() {
// used for graphics - can usually ignore function
        float2 ret;
        vector_t u = getU();
        ret.x = sqrt(u.x*u.x + u.y*u.y);
        ret.y = 1;
        return ret;
}

CudaDeviceFunction void Init() {
// Initialise the velocity at each node 
	vector_t u;
    u.x = Velocity_x; u.y = Velocity_y;  
	real_t d = Density;

	SetEquilibrium(f, d, u);
}
 
CudaDeviceFunction void Run() {
// This defines the dynamics that we run at each node in the domain.
    switch (NodeType & NODE_BOUNDARY) {
	case NODE_Solid:
	case NODE_Wall:
		BounceBack();
		break;
	case NODE_EVelocity:
		EVelocity();
		break;
	case NODE_WPressure:
		WPressure();
		break;
	case NODE_WVelocity:
		WVelocity();
		break;
	case NODE_EPressure:
		EPressure();
		break;

    }
	if (NodeType & NODE_MRT) 
	{
	// Set as if MRT as majority of examples specify
	// solution zone as MRT box, so avoid changing 
	// input files.
		//CollisionBGK();
		CollisionCM();
	}
}

CudaDeviceFunction void relax_central_moments(real_t f_in[9], real_t tau, vector_t Fhydro, vector_t u)
{
	real_t ux2 = u.x*u.x;
	real_t uy2 = u.y*u.y;
	real_t uxuy = u.x*u.y;
	
	real_t s_v = 1./tau;
	real_t m00 = f_in[0] + f_in[1] + f_in[2] + f_in[3] + f_in[4] + f_in[5] + f_in[6] + f_in[7] + f_in[8];
	real_t temp[9];
	for (int i = 0; i < 9; i++) {
		temp[i] = f_in[i];}
	
	//raw moments from density-probability functions
	//[m00, m10, m01, m20, m02, m11, m21, m12, m22]
	f_in[0] = temp[0] + temp[1] + temp[2] + temp[3] + temp[4] + temp[5] + temp[6] + temp[7] + temp[8];
	f_in[1] = temp[1] - temp[3] + temp[5] - temp[6] - temp[7] + temp[8];
	f_in[2] = temp[2] - temp[4] + temp[5] + temp[6] - temp[7] - temp[8];
	f_in[3] = temp[1] + temp[3] + temp[5] + temp[6] + temp[7] + temp[8];
	f_in[4] = temp[2] + temp[4] + temp[5] + temp[6] + temp[7] + temp[8];
	f_in[5] = temp[5] - temp[6] + temp[7] - temp[8];
	f_in[6] = temp[5] + temp[6] - temp[7] - temp[8];
	f_in[7] = temp[5] - temp[6] - temp[7] + temp[8];
	f_in[8] = temp[5] + temp[6] + temp[7] + temp[8];
	
	//central moments from raw moments
	temp[0] = f_in[0];
	temp[1] = -f_in[0]*u.x + f_in[1];
	temp[2] = -f_in[0]*u.y + f_in[2];
	temp[3] = f_in[0]*ux2 - 2*f_in[1]*u.x + f_in[3];
	temp[4] = f_in[0]*uy2 - 2*f_in[2]*u.y + f_in[4];
	temp[5] = f_in[0]*uxuy - f_in[1]*u.y - f_in[2]*u.x + f_in[5];
	temp[6] = -f_in[0]*ux2*u.y + 2*f_in[1]*uxuy + f_in[2]*ux2 - f_in[3]*u.y - 2*f_in[5]*u.x + f_in[6];
	temp[7] = -f_in[0]*u.x*uy2 + f_in[1]*uy2 + 2*f_in[2]*uxuy - f_in[4]*u.x - 2*f_in[5]*u.y + f_in[7];
	temp[8] = f_in[0]*ux2*uy2 - 2*f_in[1]*u.x*uy2 - 2*f_in[2]*ux2*u.y + f_in[3]*uy2 + f_in[4]*ux2 + 4*f_in[5]*uxuy - 2*f_in[6]*u.y - 2*f_in[7]*u.x + f_in[8];
	
	//collision in central moments space
	f_in[0] = m00;
	f_in[1] = Fhydro.x/2;
	f_in[2] = Fhydro.y/2;
	f_in[3] = (m00/3.)*(-s_v/2 + 0.25) + (m00/3.)*(s_v/2 + 0.25) + temp[3]*(-s_v/2 + 0.75) + temp[4]*(s_v/2 - 0.25);
	f_in[4] = (m00/3.)*(-s_v/2 + 0.25) + (m00/3.)*(s_v/2 + 0.25) + temp[3]*(s_v/2 - 0.25) + temp[4]*(-s_v/2 + 0.75);
	f_in[5] = temp[5]*(-s_v + 1);
	f_in[6] = (Fhydro.y/3.)/2;
	f_in[7] = (Fhydro.x/3.)/2;
	f_in[8] = (m00/9.);
	
	//back to raw moments
	temp[0] = f_in[0];
	temp[1] = f_in[0]*u.x + f_in[1];
	temp[2] = f_in[0]*u.y + f_in[2];
	temp[3] = f_in[0]*ux2 + 2*f_in[1]*u.x + f_in[3];
	temp[4] = f_in[0]*uy2 + 2*f_in[2]*u.y + f_in[4];
	temp[5] = f_in[0]*uxuy + f_in[1]*u.y + f_in[2]*u.x + f_in[5];
	temp[6] = f_in[0]*ux2*u.y + 2*f_in[1]*uxuy + f_in[2]*ux2 + f_in[3]*u.y + 2*f_in[5]*u.x + f_in[6];
	temp[7] = f_in[0]*u.x*uy2 + f_in[1]*uy2 + 2*f_in[2]*uxuy + f_in[4]*u.x + 2*f_in[5]*u.y + f_in[7];
	temp[8] = f_in[0]*ux2*uy2 + 2*f_in[1]*u.x*uy2 + 2*f_in[2]*ux2*u.y + f_in[3]*uy2 + f_in[4]*ux2 + 4*f_in[5]*uxuy + 2*f_in[6]*u.y + 2*f_in[7]*u.x + f_in[8];
	
	//back to density-probability functions
	f_in[0] = temp[0] - temp[3] - temp[4] + temp[8];
	f_in[1] = temp[1]/2 + temp[3]/2 - temp[7]/2 - temp[8]/2;
	f_in[2] = temp[2]/2 + temp[4]/2 - temp[6]/2 - temp[8]/2;
	f_in[3] = -temp[1]/2 + temp[3]/2 + temp[7]/2 - temp[8]/2;
	f_in[4] = -temp[2]/2 + temp[4]/2 + temp[6]/2 - temp[8]/2;
	f_in[5] = temp[5]/4 + temp[6]/4 + temp[7]/4 + temp[8]/4;
	f_in[6] = -temp[5]/4 + temp[6]/4 - temp[7]/4 + temp[8]/4;
	f_in[7] = temp[5]/4 - temp[6]/4 - temp[7]/4 + temp[8]/4;
	f_in[8] = -temp[5]/4 - temp[6]/4 + temp[7]/4 + temp[8]/4;
	
}

CudaDeviceFunction void CollisionBGK() {
	// Here we perform a single relaxation time collision operation.
	// pu* = pu + rG
	// BGK
	real_t d = getRho();
	vector_t u;
	u.x = ( f[8]-f[7]-f[6]+f[5]-f[3]+f[1] )/d + GravitationX/omega;
	u.y = (-f[8]-f[7]+f[6]+f[5]-f[4]+f[2] )/d + GravitationY/omega;

	real_t f_eq[9];
    SetEquilibrium(f_eq,  d, u); //stores equilibrium distribution in feq[0]-feq[8]

    for (int i=0; i< 9; i++) {
        f[i] = f[i] + omega*(f_eq[i]-f[i]);	
	}
}

CudaDeviceFunction void CollisionCM() {
	// --- central moments ---
    real_t d = getRho();
    vector_t force; 
    force.x= GravitationX;
	force.y= GravitationY;
	
    vector_t u;
    u.x = ( f[8]-f[7]-f[6]+f[5]-f[3]+f[1] )/d +  GravitationX/(2*d);
    u.y = (-f[8]-f[7]+f[6]+f[5]-f[4]+f[2] )/d +  GravitationY/(2*d);

    relax_central_moments(f, 1./omega, force, u);
}

CudaDeviceFunction void BounceBack() {
// Method to reverse distribution functions along the bounding nodes.
    real_t uf;
	uf = f[3];
	f[3] = f[1];
	f[1] = uf;
	uf = f[4];
	f[4] = f[2];
	f[2] = uf;
	uf = f[7];
	f[7] = f[5];
	f[5] = uf;
	uf = f[8];
	f[8] = f[6];
	f[6] = uf;
}
	

CudaDeviceFunction real_t getRho() {
// This function defines the macroscopic density at the current node.
	return f[8]+f[7]+f[6]+f[5]+f[4]+f[3]+f[2]+f[1]+f[0];
}

CudaDeviceFunction vector_t getU() {
// This function defines the macroscopic velocity at the current node.
	real_t d = f[8]+f[7]+f[6]+f[5]+f[4]+f[3]+f[2]+f[1]+f[0];
	vector_t u;
	// pv = pu + G/2
	u.x = ( f[8]-f[7]-f[6]+f[5]-f[3]+f[1] )/d + 0.5*GravitationX/d ;
	u.y = (-f[8]-f[7]+f[6]+f[5]-f[4]+f[2] )/d + 0.5*GravitationY/d ;
	u.z = 0;
	return u;
}

CudaDeviceFunction void SetEquilibrium(real_t f_eq[9], real_t d, vector_t u){
    f_eq[0] = ( 2. + ( -u.y*u.y - u.x*u.x )*3. )*d*2./9.;
    f_eq[1] = ( 2. + ( -u.y*u.y + ( 1 + u.x )*u.x*2. )*3. )*d/18.;
    f_eq[2] = ( 2. + ( -u.x*u.x + ( 1 + u.y )*u.y*2. )*3. )*d/18.;
    f_eq[3] = ( 2. + ( -u.y*u.y + ( -1 + u.x )*u.x*2. )*3. )*d/18.;
    f_eq[4] = ( 2. + ( -u.x*u.x + ( -1 + u.y )*u.y*2. )*3. )*d/18.;
    f_eq[5] = ( 1. + ( ( 1 + u.y )*u.y + ( 1 + u.x + u.y*3. )*u.x )*3. )*d/36.;
    f_eq[6] = ( 1. + ( ( 1 + u.y )*u.y + ( -1 + u.x - u.y*3. )*u.x )*3. )*d/36.;
    f_eq[7] = ( 1. + ( ( -1 + u.y )*u.y + ( -1 + u.x + u.y*3. )*u.x )*3. )*d/36.;
    f_eq[8] = ( 1. + ( ( -1 + u.y )*u.y + ( 1 + u.x - u.y*3. )*u.x )*3. )*d/36.;
}

CudaDeviceFunction void EVelocity()
{
    real_t rho, ru;
	real_t ux0 = Velocity_x;
	rho = ( f[0] + f[2] + f[4] + 2.*(f[1] + f[5] + f[8]) ) / (1. + ux0);
	ru = rho * ux0;
	f[3] = f[1] - (2./3.) * ru;
	f[7] = f[5] - (1./6.) * ru + (1./2.)*(f[2] - f[4]);
	f[6] = f[8] - (1./6.) * ru + (1./2.)*(f[4] - f[2]);
}

CudaDeviceFunction void WPressure()
{
        real_t ru, ux0;
	real_t rho = Density;
	ux0 = -1. + ( f[0] + f[2] + f[4] + 2.*(f[3] + f[7] + f[6]) ) / rho;
	ru = rho * ux0;

	f[1] = f[3] - (2./3.) * ru;
	f[5] = f[7] - (1./6.) * ru + (1./2.)*(f[4] - f[2]);
	f[8] = f[6] - (1./6.) * ru + (1./2.)*(f[2] - f[4]);
}

CudaDeviceFunction void WVelocity()
{
        real_t rho, ru;
	real_t u[2] = {Velocity_x,0.};
	rho = ( f[0] + f[2] + f[4] + 2.*(f[3] + f[7] + f[6]) ) / (1. - u[0]);
	ru = rho * u[0];
	f[1] = f[3] + (2./3.) * ru;
	f[5] = f[7] + (1./6.) * ru + (1./2.)*(f[4] - f[2]);
	f[8] = f[6] + (1./6.) * ru + (1./2.)*(f[2] - f[4]);
}

CudaDeviceFunction void EPressure()
{
        real_t ru, ux0;
	real_t rho = Density;
	ux0 = -1. + ( f[0] + f[2] + f[4] + 2.*(f[1] + f[5] + f[8]) ) / rho;
	ru = rho * ux0;

	f[3] = f[1] - (2./3.) * ru;
	f[7] = f[5] - (1./6.) * ru + (1./2.)*(f[2] - f[4]);
	f[6] = f[8] - (1./6.) * ru + (1./2.)*(f[4] - f[2]);
}

