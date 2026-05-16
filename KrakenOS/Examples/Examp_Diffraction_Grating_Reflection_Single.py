#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example: single-ray reflection grating trace.

This example traces one ray through a reflective diffraction grating at several
wavelengths, making the sign convention and diffracted coordinates easy to
inspect.

What this example teaches:
- how to define a reflective grating with `Glass = "MIRROR"`
- how grating spacing in micrometers relates to line density
- how the image-plane intersection changes with wavelength

Expected output:
- printed image-plane coordinates for each wavelength
- a 3D view of the traced diffracted rays

Units:
- distances are in millimeters
- wavelengths and grating spacing are in micrometers
"""

import numpy as np


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
import KrakenOS as Kos

P_Obj = Kos.surf()
P_Obj.Rc = 0.0
P_Obj.Thickness = 250
P_Obj.Glass = "AIR"
P_Obj.Diameter = 30.0


Dif_Obj = Kos.surf()
Dif_Obj.Rc = 0.0
Dif_Obj.Thickness = -250
Dif_Obj.Glass = "MIRROR"
Dif_Obj.Diameter = 30.0
Dif_Obj.Grating_D = 1000/600
Dif_Obj.Diff_Ord = 1
Dif_Obj.Grating_Angle = 0.0


P_Ima = Kos.surf()
P_Ima.Rc = 0.0
P_Ima.Name = "Image plane"
P_Ima.Thickness = 0.0
P_Ima.Glass = "AIR"
P_Ima.Diameter = 1000.0
P_Ima.Drawing = 0


A = [P_Obj, Dif_Obj, P_Ima]
configuracion_1 = Kos.Setup()


Doblete = Kos.system(A, configuracion_1)
Rayos = Kos.raykeeper(Doblete)


pSource_0 = [0, 0, 0.0]
tet = 0
dCos = [0.0, np.sin(np.deg2rad(tet)), np.cos(np.deg2rad(tet))]
w = np.linspace(.35, .90, 10)
for W in w:
    Doblete.Trace(pSource_0, dCos, W)
    print(Doblete.XYZ[-1])
    Rayos.push()


Kos.display3d(Doblete, Rayos, 1)
