clear all

% Simulation parameters
sim.dt = 20e-6;

% Load Parameters
ld_1.p0 = 500;
ld_1.R = 172.379;

% changed Parameters to adapt to DS001 Parameters'List
DS001_Pmax = 500;
DS001_p0 = 500;
DS001_kf = 0;
DS001_f0 = 50;
DS001_tf = 340*sqrt(2);
DS001_kP = (DS001_f0/DS001_Pmax)*3;
kq_vsi_1 = 1e-3;
phi0_vsi_1 = pi/4;
w0_vsi_1 = 2*pi*DS001_f0;
DS001_tP = 100e-3;
tq_vsi_1 = 10e-3;
L_vsi_1 = 2e-3;
R_vsi_1 = 1e-1;
DS001_Kp = phi0_vsi_1*180/pi;
DS001_Ki = 1;

% VSI 2 Parameters
pmax_vsi_2 = 2000;
p0_vsi_2 = 500;
q0_vsi_2 = 0;
f0_vsi_2 = 50;
v0_vsi_2 = 340*sqrt(2);
kp_vsi_2 = (f0_vsi_2/pmax_vsi_2)*3/1000;
kq_vsi_2 = 1e-3;
phi0_vsi_2 = pi/4;
w0_vsi_2 = 2*pi*f0_vsi_2;
tp_vsi_2 = 100e-3;
tq_vsi_2 = 10e-3;
L_vsi_2 = 2e-3;
R_vsi_2 = 1e-1;
phi0Deg_vsi_2 = phi0_vsi_2*180/pi;
on_vsi_2 = 1;



