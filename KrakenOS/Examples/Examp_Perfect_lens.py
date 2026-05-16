#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ideal thin-lens element.

This example builds a simple system from ideal thin-lens surfaces. It is meant
as a lightweight way to understand KrakenOS thin-lens behavior before moving to
full refractive surface definitions.

Key ideas:
- assigning ideal focal power with `Thin_Lens`
- tracing a circular grid of rays through the ideal elements
- plotting the final local coordinates at the image plane

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
P_Obj.Thickness = 50
P_Obj.Glass = "AIR"
P_Obj.Diameter = 30.0


L1a = Kos.surf()
L1a.Thin_Lens = 100
L1a.Thickness = 150
L1a.Rc = 0.0
L1a.Glass = "AIR"
L1a.Diameter = 30.0


L1b = Kos.surf()
L1b.Thin_Lens = 50.
L1b.Thickness = 100.
L1b.Rc = 0.0
L1b.Glass = "AIR"
L1b.Diameter = 30.0


P_Ima = Kos.surf()
P_Ima.Rc = 0.0
P_Ima.Thickness = 0.0
P_Ima.Glass = "AIR"
P_Ima.Diameter = 100.0
P_Ima.Name = "Image plane"


A = [P_Obj, L1a, L1b, P_Ima]
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


Kos.display3d(Doblete, RayosT, 0)
X, Y, Z, L, M, N = Rayos1.pick(-1)


plt.plot(X, Y, 'x')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Stop Diagram')
plt.axis('square')
plt.show()


print("--- %s seconds ---" % (time.time() - start_time))
