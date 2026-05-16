#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telescope made from ideal thin lenses.

This example builds a simplified telescope using ideal thin lenses. It is a
compact teaching case for pupil sampling, field angle, and basic telescope
ray geometry without the extra complexity of real glass surfaces.

Key ideas:
- creating ideal objective and eyepiece surfaces with `Thin_Lens`
- sampling three field angles through `PupilCalc`
- displaying the resulting telescope layout in 2D

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
import scipy

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

def BestFocus(X, Y, Z, L, M, N, system, mod=1):
    delta_Z = 0
    ZZ = (L, M, N, X, Y)
    v = scipy.optimize.fsolve(R_RMS_delta, delta_Z, args=ZZ)
    if mod ==1:
        system.SDT[-2].Thickness = system.SDT[-2].Thickness + v[0]
        system.SetData()
        system.SetSolid()
    return system, v[0]


P_Obj = Kos.surf(Thickness = 120, Diameter = 120)
L1 = Kos.surf(Thin_Lens = 1000.0, Thickness =1000.0 + 20, Diameter = 120)
L1.Name = "Objective"
L1.Nm_Pos = (-20,100)
L2 = Kos.surf(Thin_Lens = 20.0, Thickness = 50.0, Diameter = 20.0)
L2.Name = "Eyepiece"
# L2.Nm_Pos = (-20,100)
P_Ima = Kos.surf(Diameter = 60.0, Name = "i")

A = [P_Obj, L1, L2, P_Ima]
config_1 = Kos.Setup()

Lens = Kos.system(A, config_1)
Rays = Kos.raykeeper(Lens)

Surf, W, AperVal, AperType = 1, 0.45, L1.Diameter, "EPD"
P = Kos.PupilCalc(Lens, Surf, W, AperType, AperVal)
P.Samp, P.Ptype, P.FieldType = 1, "fanx", "angle"

P.FieldX = 0.25
x, y, z, L, M, N = P.Pattern2Field()
Kos.TraceLoop(x, y, z, L, M, N, W, Rays, clean = 0)

P.FieldX = 0.0
x, y, z, L, M, N = P.Pattern2Field()
Kos.TraceLoop(x, y, z, L, M, N, W, Rays, clean = 0)


P.FieldX = -0.25
x, y, z, L, M, N = P.Pattern2Field()
Kos.TraceLoop(x, y, z, L, M, N, W, Rays, clean = 0)

Kos.display2d(Lens, Rays, 1, arrow=1)


x,y,z,l,m,n = Rays.pick(-1, coordinates="global")
print(l)
print(m)
print(n)
