#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flat non-sequential coated surface.

This example uses non-sequential tracing with coating tables on a compact
doublet-like geometry. The file name keeps its historical spelling so existing
links do not break.

Key ideas:
- assigning coating tables with `[R, A, W, THETA]`
- enabling probabilistic surface behavior with `energy_probability`
- tracing repeated non-sequential paths for a small ray fan

Units are the KrakenOS example defaults: distances in millimeters and
wavelengths in micrometers unless the code states otherwise.
"""

import numpy as np


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
import KrakenOS as Kos

P_Obj = Kos.surf()
P_Obj.Rc = 0.0
P_Obj.Thickness = 0
P_Obj.Glass = "AIR"
P_Obj.Diameter = 30.0


P_Obj2 = Kos.surf()
P_Obj2.Rc = 0.0
P_Obj2.Thickness = 10
P_Obj2.Glass = "AIR"
P_Obj2.Diameter = 100.0


L1a = Kos.surf()
L1a.Rc = 9.284706570002484E+001
L1a.Thickness = 6.0
L1a.Glass = "BK7"
L1a.Diameter = 30.0
L1a.Axicon = 0
R = [[0.0, 0.0, 0.0],
     [0.0, 0.0, 0.0]]

A = [[0.0, 0.0, 0.0],
     [0.0, 0.0, 0.0]]

W = [0.35, 0.45, 0.55]

THETA = [0, 45]

L1a.Coating = [R, A, W, THETA]

L1b = Kos.surf()
L1b.Rc = -3.071608670000159E+001
L1b.Thickness = 3.0
L1b.Glass = "F2"
L1b.Diameter = 30
L1b.Coating = [R, A, W, THETA]


L1c = Kos.surf()
L1c.Rc = -7.819730726078505E+001
L1c.Thickness = 9.737604742910693E+001
L1c.Glass = "AIR"
L1c.Diameter = 30
L1c.Coating = [R, A, W, THETA]


P_Ima = Kos.surf()
P_Ima.Rc = 0.0
P_Ima.Thickness = 0.0
P_Ima.Glass = "MIRROR"
P_Ima.Diameter = 30.0
P_Ima.DespZ = 10
P_Ima.TiltX = 6.


A = [P_Obj, P_Obj2, L1a, L1b, L1c, P_Ima]
configuracion_1 = Kos.Setup()


Doblete = Kos.system(A, configuracion_1)
Rayos = Kos.raykeeper(Doblete)


Doblete.energy_probability = 1  # Use 0 for transmission-only behavior.
Doblete.NsLimit


tam = 10
rad = 14.0
tsis = len(A) - 1
for nsc in range(0, 10):
    for j in range(-tam, tam + 1):
        x_0 = (0 / tam) * rad
        y_0 = (j / tam) * rad
        r = np.sqrt((x_0 * x_0) + (y_0 * y_0))
        if r < rad:
            tet = 0.0
            pSource_0 = [x_0, y_0, 0.0]
            dCos = [0.0, np.sin(np.deg2rad(tet)), np.cos(np.deg2rad(tet))]
            W = 0.4
            Doblete.NsTrace(pSource_0, dCos, W)
            Rayos.push()


Kos.display3d(Doblete, Rayos, 2)
