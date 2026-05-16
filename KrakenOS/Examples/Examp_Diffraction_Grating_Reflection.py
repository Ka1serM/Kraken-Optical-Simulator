#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example: reflection diffraction grating.

This example adds a reflective grating surface after a lens group and traces a
multi-wavelength ray bundle to show angular separation by diffraction order.

What this example teaches:
- how to use `Glass = "MIRROR"` for a reflective grating
- how `Grating_D`, `Diff_Ord`, and `Grating_Angle` are assigned
- how wavelength changes the diffracted ray direction

Expected output:
- a 3D view of the reflected and diffracted ray bundle

Didactic note:
- the commented `Surface_type` line is an optional low-level experiment and is
  not required for the standard example.

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
L1a.Rc = 5.513435044607768E+001
L1a.Thickness = 6.0
L1a.Glass = "BK7"
L1a.Diameter = 30.0


L1b = Kos.surf()
L1b.Rc = -4.408716526030626E+001
L1b.Thickness = 3.0
L1b.Glass = "F2"
L1b.Diameter = 30


L1c = Kos.surf()
L1c.Rc = -2.246906271406796E+002
L1c.Thickness = 9.737871661422000E+001 - 50.0
L1c.Glass = "AIR"
L1c.Diameter = 30


Dif_Obj = Kos.surf()
Dif_Obj.Rc = 0.0
Dif_Obj.Thickness = -50
Dif_Obj.Glass = "MIRROR"
Dif_Obj.Diameter = 30.0
Dif_Obj.Grating_D = 1.0
Dif_Obj.Diff_Ord = 1
Dif_Obj.Grating_Angle = 45.0
# Optional low-level experiment:
# The standard grating behavior is already defined by the fields above.
# Dif_Obj.Surface_type = 1


P_Ima = Kos.surf()
P_Ima.Rc = 0.0
P_Ima.Name = "Image plane"
P_Ima.Thickness = 0.0
P_Ima.Glass = "AIR"
P_Ima.Diameter = 300.0
P_Ima.Drawing = 0


A = [P_Obj, L1a, L1b, L1c, Dif_Obj, P_Ima]
configuracion_1 = Kos.Setup()


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


Kos.display3d(Doblete, Rayos, 1)
