"""
Custom source distribution function.

This example defines several source probability distributions and traces the
generated rays through a simple mirror system. Change `examp` to compare a
solar-like profile, sinc profile, flat distribution, parabolic distribution, or
Gaussian seeing profile.

Key ideas:
- defining a custom source function for `SourceRnd`
- converting sampled source coordinates into traced rays
- plotting only rays that reach the image surface

The `Rays.push()` and 3D display calls are intentionally commented. They are
useful when debugging the full ray set, but they make the example heavier.

Units are the KrakenOS example defaults: distances in millimeters and
wavelengths in micrometers unless the code states otherwise.
"""

import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv
import scipy


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
import KrakenOS as Kos
P_Obj = Kos.surf()

P_Obj.Thickness = 5000.0
P_Obj.Glass = "AIR"
P_Obj.Diameter = 6.796727741707513E+002 * 2.0
P_Obj.Drawing = 0

######################################################################################


objeto = Kos.surf()
objeto.Rc = -12000
objeto.k = -1
objeto.Diameter = 2500
objeto.Thickness = -6000
objeto.Glass = "MIRROR"

P_Ima = Kos.surf()
P_Ima.Rc = 0
P_Ima.Thickness = -1.0
P_Ima.Glass = "AIR"
P_Ima.Diameter = 6000.0
P_Ima.Drawing = 1
P_Ima.Name = "Image plane"

A = [P_Obj, objeto, P_Ima]

configur = Kos.Setup()
Telescope = Kos.system(A, configur)
Rays = Kos.raykeeper(Telescope)

W = 0.633
Sun = Kos.SourceRnd()

examp = 4
if examp == 0:
    # Sun distribution
    def f(x):
        teta = x
        FI = np.zeros_like(teta)
        Arg2 = np.argwhere(teta > (4.65 / 1000.0))
        FI = np.cos(0.326 * teta) / np.cos(0.308 * teta)

        Chi2 = .03
        k = 0.9 * np.log(13.5 * Chi2) * np.power(Chi2, -0.3)
        r = (2.2 * np.log(0.52 * Chi2) * np.power(Chi2, 0.43)) - 1.0
        FI[Arg2] = np.exp(k) * np.power(teta[Arg2] * 1.0e3, r)
        return FI


    Sun.field = 20 * np.rad2deg((4.65 / 1000.0))

if examp == 1:
    # Sinc function
    def f(x):
        Wh = 0.025
        r = (x * 90.0 / 0.025) * np.pi
        res = np.sin(r) / r
        return res


    Sun.field = 0.025 * 3

if examp == 2:
    # Flat
    def f(x):
        res = 1
        return res


    Sun.field = 1.2 / (2. * 3600.)

if examp == 3:
    # Parabolic
    def f(x):
        r = (x * 90.0 / 0.025)
        res = r ** 2
        return res


    Sun.field = 1.2 / (2. * 3600.)

if examp == 4:
    # Gaussian (Seeing)
    def f(x):
        x = np.rad2deg(x)
        seing = 1.2 / 3600.0
        sigma = seing / 2.3548
        mean = 0
        standard_deviation = sigma
        y = scipy.stats.norm(mean, standard_deviation)
        res = y.pdf(x)
        return res


    Sun.field = 4 * 1.2 / (2.0 * 3600.0)

Sun.fun = f
Sun.dim = 3000
Sun.num = 10000
L, M, N, X, Y, Z = Sun.rays()

Xr = np.zeros_like(L)
Yr = np.zeros_like(L)
Nr = np.zeros_like(L)

con = 0
con2 = 0
for i in range(0, Sun.num):
    if con2 == 10:
        print(100. * i / Sun.num)
        con2 = 0

    pSource_0 = [X[i], Y[i], Z[i]]
    dCos = [L[i], M[i], N[i]]
    Telescope.Trace(pSource_0, dCos, W)

    Xr[con] = Telescope.Hit_x[-1]
    Yr[con] = Telescope.Hit_y[-1]
    Nr[con] = Telescope.SURFACE[-1]
    con = con + 1
    con2 = con2 + 1
    # Optional didactic ray storage for 3D visualization:
    # Rays.push()

args = np.argwhere(Nr == 2)
plt.plot(Xr[args], Yr[args], '.', c="g", markersize=1)

# axis labeling
plt.xlabel('x')
plt.ylabel('y')

# figure name
plt.title('Spot diagram')
plt.axis('square')
plt.show()

# Optional didactic display:
# Kos.display3d(Telescope, Rays, 0)
