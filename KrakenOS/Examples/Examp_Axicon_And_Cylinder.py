#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example: axicon combined with cylindrical power.

This example combines an axicon term with a cylindrical contribution on the
same surface to show how nonstandard surface parameters interact.

What this example teaches:
- how `Axicon` and `Cylinder_Rxy_Ratio` can be combined
- how a conic constant and cylindrical ratio change the ray bundle
- how to visualize the combined surface effect in 3D

Expected output:
- a 3D view of the multi-wavelength ray bundle after the combined surface

Units:
- distances are in millimeters
- wavelengths are in micrometers
"""

import numpy as np


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
import KrakenOS as Kos

configuracion_1 = Kos.Setup()


P_Obj = Kos.surf()
P_Obj.Rc = 0.0
P_Obj.Thickness = 10
P_Obj.Glass = "AIR"
P_Obj.Diameter = 30.0


L1a = Kos.surf()
L1a.Rc = 0
L1a.Thickness = 26.0
L1a.Glass = "BK7"
L1a.Diameter = 30.0


L1c = Kos.surf()
L1c.Rc = 0.
L1c.K = -1
L1c.Thickness = 9.737604742910693E+001
L1c.Axicon = (-35.0)
L1c.ShiftY = 0
L1c.Cylinder_Rxy_Ratio = 0
L1c.Glass = "AIR"
L1c.Diameter = 30


P_Ima = Kos.surf()
P_Ima.Rc = 0.0
P_Ima.Thickness = 0.0
P_Ima.Glass = "AIR"
P_Ima.Diameter = 100.0
P_Ima.Name = "Image plane"


A = [P_Obj, L1a, L1c, P_Ima]


Doblete = Kos.system(A, configuracion_1)
Rayos = Kos.raykeeper(Doblete)


tam = 5
rad = 10.0
tsis = len(A) - 1
for i in range(-tam, tam + 1):
    for j in range(-tam, tam + 1):
        x_0 = (i / tam) * rad
        y_0 = (j / tam) * rad
        r = np.sqrt((x_0 * x_0) + (y_0 * y_0))
        if r < rad:
            tet = 0.0
            pSource_0 = [x_0, y_0, 0.0]
            dCos = [0.0, np.sin(np.deg2rad(tet)), np.cos(np.deg2rad(tet))]
            W = 0.4
            Doblete.Trace(pSource_0, dCos, W)
            Rayos.push()
            W = 0.5
            Doblete.Trace(pSource_0, dCos, W)
            Rayos.push()
            W = 0.6
            Doblete.Trace(pSource_0, dCos, W)
            Rayos.push()


Kos.display3d(Doblete, Rayos, 0)
