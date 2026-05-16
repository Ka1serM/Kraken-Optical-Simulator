#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example: micro-lens array as an extra surface shape.

This example approximates a micro-lens array by folding local coordinates into
repeated cells and evaluating a conic-like sag function in each cell.

What this example teaches:
- how a custom `ExtraData` function can describe repeated surface cells
- how the coefficient list controls pitch, curvature, and conic behavior
- how to keep a 3D display active while leaving 2D plotting optional

Expected output:
- a 3D view of rays interacting with the micro-lens array surface

Didactic note:
- the 2D display call is intentionally commented. Uncomment it if you want a
  simpler projection after inspecting the 3D geometry.

Units:
- distances are in millimeters
- wavelengths are in micrometers
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
import KrakenOS as Kos
import numpy as np
import matplotlib.pyplot as plt


P_Obj = Kos.surf()
P_Obj.Rc = 0.0
P_Obj.Thickness = 10
P_Obj.Glass = "AIR"
P_Obj.Diameter = 30.0


L1a = Kos.surf()
L1a.Rc = 55.134 * 0
L1a.Thickness = 2.0
L1a.Glass = "BK7"
L1a.Diameter = 30.0


L1c = Kos.surf()
L1c.Thickness = 40
L1c.Glass = "AIR"
L1c.Diameter = 30


def f(x, y, E):
    DeltaX = E[0] * np.rint(x / E[0])
    DeltaY = E[0] * np.rint(y / E[0])
    x = x - DeltaX
    y = y - DeltaY
    s = np.sqrt((x * x) + (y * y))
    c = 1.0 / E[1]
    InRoot = 1 - (E[2] + 1.0) * c * c * s * s
    z = (c * s * s / (1.0 + np.sqrt(InRoot)))
    return z


coef = [3.0, -3, 0]
L1c.ExtraData = [f, coef]
L1c.Res = 2


P_Ima = Kos.surf()
P_Ima.Rc = 0.0
P_Ima.Thickness = 0.0
P_Ima.Glass = "AIR"
P_Ima.Diameter = 300.0
P_Ima.Name = "Image plane"


A = [P_Obj, L1a, L1c, P_Ima]
Config_1 = Kos.Setup()


Lens = Kos.system(A, Config_1)
Rays = Kos.raykeeper(Lens)


Wav = 0.45
for i in range(-100, 100 + 1):
    pSource = [0.0, i / 10., 0.0]
    dCos = [0.0, 0.0, 1.0]
    Lens.Trace(pSource, dCos, Wav)
    Rays.push()


Kos.display3d(Lens, Rays, 1)
# Optional didactic display:
# Uncomment this line to inspect the same ray bundle in a 2D projection.
# Kos.display2d(Lens, Rays, 0)
