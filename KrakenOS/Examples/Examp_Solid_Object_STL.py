#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example: single STL solid object in a telescope-like system.

This example loads a packaged STL prism-like object, places it in a reflective
system, and traces non-sequential rays through the solid geometry.

What this example teaches:
- how to load packaged STL geometry with `importlib.resources`
- how to attach STL geometry to `Solid_3d_stl`
- how `NsTrace` is used for solid-object interactions
- how `NsLimit` and `energy_probability` affect non-sequential tracing

Required packaged file:
- `KrakenOS/Examples/Prisma.stl`

Expected output:
- a 3D view of the telescope-like system and traced rays
- the effective focal length printed to the console

Didactic note:
- the commented debug print is intentionally left as an optional inspection
  point inside the ray loop.

Units:
- distances are in millimeters
- wavelengths are in micrometers
"""

# import os
import numpy as np
from importlib import resources


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
import KrakenOS as Kos

P_Obj = Kos.surf()
P_Obj.Thickness = 2.000000000000000E+003
P_Obj.Glass = "AIR"
P_Obj.Diameter = 6.796727741707513E+002 * 2.0
P_Obj.Drawing = 0


M1 = Kos.surf()
M1.Rc = -6.0E+003
M1.Thickness = -1.774190000000000E+003 + 1.853722901194000E+000
M1.k = -1.6+000
M1.Glass = "MIRROR"
M1.Diameter = 6.63448E+002 * 2.0
M1.InDiameter = 228.6 * 2.0
M1.DespY = 0.0
M1.TiltX = 0.0000
M1.AxisMove = 1


M2 = Kos.surf()
M2.Rc = -6.00E+003
M2.Thickness = -M1.Thickness
M2.k = -3.4782E+001
M2.Glass = "MIRROR"
M2.Diameter = 3.0E+002 * 2.0


Vertex = Kos.surf()
Vertex.Thickness = 130.0
Vertex.Glass = "AIR"
Vertex.Diameter = 600.0
Vertex.Drawing = 0


file = resources.files("KrakenOS") / "Examples" / "Prisma.stl"


objeto = Kos.surf()
objeto.Diameter = 118.0 * 2.0
objeto.Solid_3d_stl = file
objeto.Thickness = 600
objeto.Glass = "BK7"
objeto.TiltX = 55
objeto.TiltY = 0
objeto.TiltZ = 45
objeto.DespX = 0
objeto.DespY = 0
objeto.AxisMove = 0


P_Ima = Kos.surf()
P_Ima.Rc = 0
P_Ima.Thickness = 100.0
P_Ima.Glass = "AIR"
P_Ima.Diameter = 500.0
P_Ima.Drawing = 1


A = [P_Obj, M1, M2, Vertex, objeto, P_Ima]
configuracion_1 = Kos.Setup()


Telescope = Kos.system(A, configuracion_1)
Rays = Kos.raykeeper(Telescope)


Telescope.energy_probability = 1
Telescope.NsLimit = 10


W = 0.633
tam = 5
rad = 6.56727741707513E+002
tsis = len(A) + 2
for gg in range(0, 10):
    for j in range(-tam, tam + 1):
        # j=0
        for i in range(-tam, tam + 1):
            x_0 = (i / tam) * rad
            y_0 = (j / tam) * rad
            r = np.sqrt((x_0 * x_0) + (y_0 * y_0))
            if r < rad:
                tet = 0.0
                pSource_0 = [x_0, y_0, 0.0]
# Optional didactic debug print:
# Uncomment while studying the ray loop, but leave disabled for normal runs.
                # print("-...............")
                dCos = [0.0, np.sin(np.deg2rad(tet)), np.cos(np.deg2rad(tet))]
                W = 0.633
                Telescope.NsTrace(pSource_0, dCos, W)
                Rays.push()

# # ______________________________________#

Kos.display3d(Telescope, Rays, 0)
print(Telescope.EFFL)
