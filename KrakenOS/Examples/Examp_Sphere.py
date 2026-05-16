#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spherical surface example.

This example traces a small ray fan from a spherical mirror and prints the
computed reflection coefficients. It also demonstrates loading a metal coating
resource from the installed KrakenOS package.

Key ideas:
- loading packaged metal data with `importlib.resources`
- assigning a mirror coating model
- using `PupilCalc` to trace a simple ray fan
- inspecting S and P polarization reflection outputs

Units are the KrakenOS example defaults: distances in millimeters and
wavelengths in micrometers unless the code states otherwise.
"""

import numpy as np
from importlib import resources


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
M1.k = -1.0 * 0
M1.Glass = "MIRROR"
M1.Diameter = 2000
M1.CoatingMet = 0


P_Ima = Kos.surf()
P_Ima.Glass = "AIR"
P_Ima.Diameter = 1600.0
P_Ima.Drawing = 0
P_Ima.Name = "Image plane"


A = [P_Obj, M1, P_Ima]
configuracion_1 = Kos.Setup()

MATERIAL_PATH = resources.files("KrakenOS") / "Cat" / "Gold.csv"

configuracion_1.LoadMetal(MATERIAL_PATH, "Gold", 1)


Espejo = Kos.system(A, configuracion_1)
Rayos = Kos.raykeeper(Espejo)


W = 0.5876
Surf = 1
AperVal = M1.Diameter
AperType = "EPD"
fieldType = "angle"

Pup = Kos.PupilCalc(Espejo, Surf, W, AperType, AperVal)
Pup.Samp =1
Pup.Ptype = "fany"
Pup.FieldY = 0
x, y, z, L, M, N = Pup.Pattern2Field()
Rayos = Kos.raykeeper(Espejo)


Kos.TraceLoop(x, y, z, L, M, N, W, Rayos, clean = 1)
Kos.display3d(Espejo, Rayos, 0)


# Optional didactic inspection:
# print(Rayos.TP)
# print(Rayos.TS)
print(Rayos.RS[0], Rayos.RS[1], Rayos.RS[2])
print(Rayos.RP[0], Rayos.RP[1], Rayos.RP[2])


# Kos.n_wave_dispersion(configuracion_1, "BK7", 0.4)

# configuracion_1.NAMES
# configuracion_1.CAT
# configuracion_1.NAMES
# configuracion_1.NM
# configuracion_1.ED
# configuracion_1.CD
# configuracion_1.TD
# configuracion_1.OD
# configuracion_1.LD
# configuracion_1.IT


# [Dispersion_Formula, MIL, Nd, Vd, *_] = NM[r]


# x,y,z,l,m,n = Rayos.pick(-1, coordinates="local")
