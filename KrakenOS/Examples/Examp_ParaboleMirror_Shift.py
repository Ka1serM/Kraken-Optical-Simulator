#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example: shifted parabolic mirror.

This example traces a ray bundle on a shifted parabolic mirror and evaluates
the resulting spot size.

What this example teaches:
- how to model a mirror with `Glass = "MIRROR"`
- how `ShiftY` moves the surface function relative to the aperture
- how to extract local ray data and estimate an RMS spot radius

Expected output:
- a 2D layout of the mirror system
- a printed RMS-like spot metric
- a spot diagram plotted with Matplotlib

Didactic note:
- the commented pickle block is intentionally left as an optional experiment
  for saving and reloading a full system object. It is disabled by default
  because it creates a local file and is not needed for the optical result.

Units:
- distances are in millimeters
- wavelengths are in micrometers
"""

import numpy as np
import pickle


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
import KrakenOS as Kos

P_Obj = Kos.surf()
P_Obj.Thickness = 1000.0
P_Obj.Diameter = 300
P_Obj.Drawing = 0


M1 = Kos.surf()
M1.Rc = -2 * P_Obj.Thickness
M1.Thickness = M1.Rc / 2
M1.k = -1.0
M1.Glass = "MIRROR"
M1.Diameter = 300
M1.ShiftY = 200
# M1.DerPres= 0.04

aa = 100
bb = 100


P_Ima = Kos.surf()
P_Ima.Glass = "AIR"
P_Ima.Diameter = 1600.0
P_Ima.Drawing = 0
P_Ima.Name = "Image plane"


A = [P_Obj, M1, P_Ima]
configuracion_1 = Kos.Setup()


Espejo = Kos.system(A, configuracion_1)

# Espejo = Kos.system_Lite(A, configuracion_1)


# Optional didactic serialization experiment:
# Uncomment this block to save and reload the full system object with pickle.
# with open('mi_objeto.pkl', 'wb') as archivo_salida:
#     # Save the system object to a local pickle file.
#     pickle.dump(Espejo, archivo_salida)

# with open('mi_objeto.pkl', 'rb') as archivo_entrada:
#     Espejo = pickle.load(archivo_entrada)


Rayos = Kos.raykeeper(Espejo)


tam = 15
rad = 150.0
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
            Espejo.Trace(pSource_0, dCos, W)
            Rayos.push()


Kos.display2d(Espejo, Rayos, 0)


def R_RMS_delta(Z1, L, M, N, X0, Y0):
    X1 = ((L / N) * Z1) + X0
    Y1 = ((M / N) * Z1) + Y0
    cenX = np.mean(X1)
    cenY = np.mean(Y1)
    x1 = (X1 - cenX)
    y1 = (Y1 - cenY)
    R2 = ((x1 * x1) + (y1 * y1))
    R_RMS = np.sqrt(np.mean(R2))
    return R_RMS

x,y,z,l,m,n = Rayos.pick(-1, coordinates="local")

print(R_RMS_delta(z, l, m, n, x, y))
X, Y, Z, L, M, N = Rayos.pick(-1)


import matplotlib.pyplot as plt
plt.plot(X, Y, 'x')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Spot Diagram')
plt.axis('square')
plt.show()
