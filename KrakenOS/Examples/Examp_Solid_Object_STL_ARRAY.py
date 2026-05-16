#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example: generated array of solid mirror elements.

This example builds an array of small PyVista cube elements, combines them into
one solid object, and traces one ray per array element with non-sequential
reflection.

What this example teaches:
- how to generate solid geometry programmatically with PyVista
- how to combine many elements into one object for `Solid_3d_stl`
- how a solid mirror array can be tested with non-sequential tracing

Expected output:
- a Matplotlib spot plot
- a 3D view of the generated mirror array and traced rays

Didactic note:
- STL/VTK solid elements in non-sequential mode are approximate. This example is
  best treated as a lighting or geometry demonstration; the ideal spot diagram
  should collapse toward a dot.
- the STL save lines are intentionally commented to avoid generating local
  files during a normal run.

Units:
- distances are in millimeters
- wavelengths are in micrometers
"""

import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
import KrakenOS as Kos

P_Obj = Kos.surf()
P_Obj.Thickness = 7000.0
P_Obj.Glass = "AIR"
P_Obj.Diameter = 5000
P_Obj.Drawing = 1


n = 11
Lx = 100.0
Ly = 100.0
Lz = 0.1
focal = 5000.0

element0 = pv.Cube(center=(0.0, 0.0, 0.0), x_length=0.1, y_length=0.1, z_length=0.1, bounds=None)
for A in range(-n, n + 1):
    for B in range(-n, n + 1):

        element1 = pv.Cube(center=( 0.0, 0.0, 0.0), x_length=Lx, y_length=Ly, z_length=Lz,)
        v = [A * Lx , B * Ly, 0]
        Ty =  0.5 * np.rad2deg(np.arctan2(A * Lx, focal))
        Tx = -0.5 * np.rad2deg(np.arctan2(B * Ly, focal))


        try:
            element1.rotate_x(Tx, inplace = True)
            element1.rotate_y(Ty, inplace = True)
            element1.translate(v, inplace = True)
        except:

            element1.rotate_x(Tx)
            element1.rotate_y(Ty)
            element1.translate(v)


        element0 = element0 + element1

# Optional didactic export:
# Uncomment these lines to save the generated solid for inspection in CAD tools.
# element0.save("salida.stl")
# direc = r"salida.stl"


objeto = Kos.surf()
objeto.Diameter = 118.0 * 2.0
objeto.Solid_3d_stl = element0
objeto.Thickness = -5000
objeto.Glass = "MIRROR"
objeto.TiltX = 0
objeto.TiltY = 0
objeto.DespX = 0
objeto.DespY = 0
objeto.AxisMove = 0


P_Ima = Kos.surf()
P_Ima.Rc = 0
P_Ima.Thickness = -1.0
P_Ima.Glass = "AIR"
P_Ima.Diameter = 200.0
P_Ima.Drawing = 1
P_Ima.Name = "Image plane"


A = [P_Obj, objeto, P_Ima]
configur = Kos.Setup()


MirrorArray = Kos.system(A, configur)
Rays = Kos.raykeeper(MirrorArray)


W = 0.633


for A in range(-n, n + 1):
    for B in range(-n, n + 1):


        x_0 = A * Lx
        y_0 = B * Ly
        r = np.sqrt((x_0 * x_0) + (y_0 * y_0))
        tet = 0.0
        pSource_0 = [x_0, y_0, 0.0]
        dCos = [0.0, np.sin(np.deg2rad(tet)), np.cos(np.deg2rad(tet))]
        MirrorArray.NsTrace(pSource_0, dCos, W)
        if np.shape(MirrorArray.NAME)[0] != 0:
            if MirrorArray.NAME[-1] == "Image plane":
                plt.plot(MirrorArray.Hit_x[-1], MirrorArray.Hit_y[-1], '.', c="g")
                Rays.push()


plt.axis('square')
plt.show()
Kos.display3d(MirrorArray, Rays, 0)
