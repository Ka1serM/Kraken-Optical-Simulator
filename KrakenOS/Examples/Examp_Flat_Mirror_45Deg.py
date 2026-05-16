#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flat mirror at 45 degrees.

This example sends a doublet ray bundle to a tilted flat mirror. It is a useful
coordinate and sign-convention check because the reflected bundle is displayed
both in the system layout and in a final spot plot.

Key ideas:
- inserting a flat `MIRROR` surface after a refractive group
- using `TiltX` and `AxisMove` to orient the fold mirror
- comparing three wavelengths after reflection

The 3D display line is intentionally commented because the 2D layout plus spot
diagram usually opens faster while editing the example.

Units are the KrakenOS example defaults: distances in millimeters and
wavelengths in micrometers unless the code states otherwise.
"""

import time
import matplotlib.pyplot as plt
import numpy as np

import sys


from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
import KrakenOS as Kos

start_time = time.time()


P_Obj = Kos.surf()
P_Obj.Rc = 0.0
P_Obj.Thickness = 10
P_Obj.Glass = "AIR"
P_Obj.Diameter = 30.0


L1a = Kos.surf()
L1a.Rc = 9.284706570002484E+001
L1a.Thickness = 6.0
L1a.Glass = "BK7"
L1a.Diameter = 30.0
L1a.Axicon = 0


L1b = Kos.surf()
L1b.Rc = -3.071608670000159E+001
L1b.Thickness = 3.0
L1b.Glass = "F2"
L1b.Diameter = 30


POS_ESP = -40
L1c = Kos.surf()
L1c.Rc = -7.819730726078505E+001
L1c.Thickness = 9.737604742910693E+001 + POS_ESP
L1c.Glass = "AIR"
L1c.Diameter = 30


Esp90 = Kos.surf()
Esp90.Thickness = POS_ESP
Esp90.Glass = "MIRROR"
Esp90.Diameter = 30.0
Esp90.Name = "45 degree fold mirror"
Esp90.TiltX = 45.
Esp90.AxisMove = 2.


P_Ima = Kos.surf()
P_Ima.Rc = 0.0
P_Ima.Thickness = 0.0
P_Ima.Glass = "AIR"
P_Ima.Diameter = 3.0
P_Ima.Name = "Image plane"


A = [P_Obj, L1a, L1b, L1c, Esp90, P_Ima]

config_1 = Kos.Setup()


Doblete = Kos.system(A, config_1)


Rayos1 = Kos.raykeeper(Doblete)
Rayos2 = Kos.raykeeper(Doblete)
Rayos3 = Kos.raykeeper(Doblete)
RayosT = Kos.raykeeper(Doblete)


tam = 10
rad = 10.0
tsis = len(A) - 1
for j in range(-tam, tam + 1):
    for i in range(-tam, tam + 1):
        x_0 = (i / tam) * rad
        y_0 = (j / tam) * rad
        r = np.sqrt((x_0 * x_0) + (y_0 * y_0))
        if r < rad:
            tet = 0.0
            pSource_0 = [x_0, y_0, 0.0]
            dCos = [0.0, np.sin(np.deg2rad(tet)), np.cos(np.deg2rad(tet))]
            W = 0.4
            Doblete.Trace(pSource_0, dCos, W)
            Rayos1.push()
            RayosT.push()
            W = 0.5
            Doblete.Trace(pSource_0, dCos, W)
            Rayos2.push()
            RayosT.push()
            W = 0.6
            Doblete.Trace(pSource_0, dCos, W)
            Rayos3.push()
            RayosT.push()


# Optional didactic display:
# Kos.display3d(Doblete, RayosT, 2)

system = Doblete
Kos.display2d(system, RayosT, 0)


# # ______________________________________#

X, Y, Z, L, M, N = Rayos1.pick(-1)
plt.plot(X, Z, 'x')
X, Y, Z, L, M, N = Rayos2.pick(-1)
plt.plot(X, Z, 'x')
X, Y, Z, L, M, N = Rayos3.pick(-1)
plt.plot(X, Z, 'x')
plt.xlabel('X')
plt.ylabel('Z')
plt.title('Spot Diagram')
plt.axis('square')
plt.show()
