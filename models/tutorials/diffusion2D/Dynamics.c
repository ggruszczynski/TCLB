// Model for solving the convection-diffusion equation:
// phi' = c*lap(phi)
// phi' = c * (phi_xx + phi_yy)

CudaDeviceFunction float2 Color() {
  float2 ret;
  ret.x = 0;
  ret.y = 1;
  return ret;
}

CudaDeviceFunction real_t getU() {
    return u(0,0);
  }

CudaDeviceFunction void Init() {
    u = Value;

 }

CudaDeviceFunction void Run() { 
  real_t lap_u = u(-1,0) + u(1,0) + u(0,-1) + u(0,1) - 4*u(0,0);
  real_t temp = Speed * Speed * lap_u;
  u = u(0,0) + temp;

  if ((NodeType & NODE_BOUNDARY) == NODE_Dirichlet) 
    u = Value;
  }
}