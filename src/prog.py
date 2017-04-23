#!../my_project/bin/python3

import argparse
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

# Parse arguments

parser = argparse.ArgumentParser(description="Run simulation of electric circuit")

parser.add_argument("-r", "--resistance", type=float, default=3,
                    help="Value of resistance in the circuit in ohms. Default: 3 ohm")
parser.add_argument("-c", "--capacitance", type=float, default=0.5,
                    help="Value of capacitance in the circuit in farads. Default: 1/2 F")
parser.add_argument("-i", "--inductance", type=float, default=1,
                    help="Value of inductance in the circuit in henry. Default: 1 H")

parser.add_argument("-u", "--input", type=str, choices=["step", "impulse"], default='step',
                    help="Input function of the circuit (Current source) in A. Default: step")

parser.add_argument("--vc", type=float, default=0,
                    help="Initial vc value. Default: 0")
parser.add_argument("--il", type=float, default=0,
                    help="Initial il value. Default: 0")

parser.add_argument("--step", type=float, default=0.1,
                    help="Time step for simulation in seconds. Default: 0.1s")

parser.add_argument("--simtime", type=float, default=10,
                    help="Time of simulation in seconds. Default: 10s")

args = parser.parse_args()

R = args.resistance
L = args.inductance
C = args.capacitance
ustr = args.input
vc0 = args.vc
il0 = args.il
dt = args.step
T = args.simtime

# Show information to user
print("VARIABLES FOR SIMULATION")
print("R =", R, "ohm")
print("L =", L, "H")
print("C =", C, "F")
print("input: ", ustr)
print("vc0 =", vc0, "V")
print("il0 =", il0, "A")
print("time step:", dt, "s")
print("timulation time:", T, "s")
print("")

# Simulate the system

# initial conditions
x0 = np.array([vc0, il0])

# matrices for continuous state space
A = np.array([[0, -1/C], [1/L, -R/L]])
B = np.array([[1/C], [0]])
C = np.array([[0, R]])
D = np.array([[0]])

# create time array
t = np.arange(0, T+dt, dt)

# create input array
if ustr == "step":
    u = np.ones(len(t))
elif ustr == "impulse":
    u = np.zeros(len(t))
    u[0] = 1

# continuous system
contsys = signal.lti(A, B, C, D)
# convert to discrete system
sys = contsys.to_discrete(dt)
# get response
t, y, x = sys.output(u, t=t, x0=x0)

# Plot results

tinput = np.zeros(len(t)+1)
tinput[0] = -dt
tinput[1:] = t
uinput = np.zeros(len(t)+1)
uinput[1:] = u
u[0] = 0
plt.plot(t, u, label="Input current (A)")
plt.plot(t, y, label="Output voltage (V)")
plt.plot(t, x[:, 0], label="Voltage of the capacitor (V)")
plt.plot(t, x[:, 1], label="Current of the inductor (A)")

plt.xlabel("time (s)")

if ustr == "step":
    plt.title("Step response of circuit")
elif ustr == "impulse":
    plt.title("Impulse response of circuit")

plt.legend()

plt.figure()

plt.title("XY plot of the state variables")
plt.plot(x[:, 0], x[:, 1])
plt.xlabel("Voltage of the capacitor (V)")
plt.ylabel("Current of the inductor (H)")

plt.show()

