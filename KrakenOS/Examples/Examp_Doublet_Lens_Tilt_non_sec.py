#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example: tilted doublet with non-sequential tracing.

This example uses `NsTrace` to follow rays through a tilted doublet system
where surface order is handled by the non-sequential solver.

What this example teaches:
- when to use `NsTrace` instead of sequential `Trace`
- how `build = 0` can be used for a lighter non-sequential setup
- how `energy_probability` is enabled for non-sequential propagation

Expected output:
- a 3D view of the non-sequential traced rays

Units:
- distances are in millimeters
- wavelengths are in micrometers
"""

import numpy as np


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
import KrakenOS as Kos

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
L1a.AxisMove = 1
L1a.TiltX = 13.0
L1a.DespZ = 5.0


L1b = Kos.surf()
L1b.Rc = (-3.071608670000159E+001)
L1b.Thickness = 3.0
L1b.Glass = "F2"
L1b.Diameter = 30


L1c = Kos.surf()
L1c.Rc = (-7.819730726078505E+001)
L1c.Thickness = 9.737604742910693E+001
L1c.Glass = "AIR"
L1c.Diameter = 30


P_Ima = Kos.surf()
P_Ima.Rc = 0.0
P_Ima.Thickness = 0.0
P_Ima.Glass = "AIR"
P_Ima.Diameter = 1000.0
P_Ima.Name = "Image plane"


A = [P_Obj, L1a, L1b, L1c, P_Obj, L1a, L1b, L1c, P_Ima]
configuracion_1 = Kos.Setup()


Doblete = Kos.system(A, configuracion_1, build = 0)
Rayos = Kos.raykeeper(Doblete)
Doblete.energy_probability=1


tam = 30
rad = 18.0
tsis = len(A) - 1
for j in range(-tam, tam + 1):
    i = 0
    x_0 = (i / tam) * rad
    y_0 = (j / tam) * rad
    r = np.sqrt((x_0 * x_0) + (y_0 * y_0))
    if r < rad:
        tet = 0.0
        pSource_0 = [x_0, y_0, 0.0]
        dCos = [0.0, np.sin(np.deg2rad(tet)), np.cos(np.deg2rad(tet))]
        W = 0.4
        Doblete.NsTrace(pSource_0, dCos, W)
        Rayos.push()
        W = 0.5
        Doblete.NsTrace(pSource_0, dCos, W)
        Rayos.push()
        W = 0.6
        Doblete.NsTrace(pSource_0, dCos, W)
        Rayos.push()


Kos.display3d(Doblete, Rayos, 2)
