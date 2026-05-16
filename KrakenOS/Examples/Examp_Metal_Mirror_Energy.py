#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example: metal mirror energy terms.

This example compares the reflected and transmitted energy terms for a simple
spherical mirror using the default aluminum data and a loaded gold material
table. It is intentionally small so the output focuses on `CoatingMet`, `RP`,
`RS`, `TP`, `TS`, and `TT`.

What this example teaches:
- how metal data are selected with `CoatingMet`
- how to load an additional metal table with `Setup.LoadMetal`
- how S and P reflection/transmission terms are stored after a trace

Expected output:
- aluminum mirror energy terms
- gold mirror energy terms

Units:
- distances are in millimeters
- wavelengths are in micrometers
"""

import sys
from importlib import resources
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parents[2]))
import KrakenOS as Kos


def as_float_list(values):
    """Convert NumPy scalar values to plain Python floats for clean printing."""
    return [float(value) for value in values]


def trace_mirror(coating_index):
    setup = Kos.Setup()
    gold_path = resources.files("KrakenOS") / "Cat" / "Gold.csv"
    setup.LoadMetal(gold_path, "Gold", 1)

    object_plane = Kos.surf(Thickness=100.0, Diameter=10.0)
    object_plane.Drawing = 0

    mirror = Kos.surf()
    mirror.Rc = -200.0
    mirror.Thickness = -100.0
    mirror.Glass = "MIRROR"
    mirror.Diameter = 20.0
    mirror.CoatingMet = coating_index

    image_plane = Kos.surf(Thickness=0.0, Glass="AIR", Diameter=20.0)
    image_plane.Drawing = 0
    image_plane.Name = "Return plane"

    system = Kos.system([object_plane, mirror, image_plane], setup)
    system.Trace([0.0, 0.0, 0.0], [0.0, 0.0, 1.0], 0.5876)

    return {
        "valid": bool(system.val),
        "RP": as_float_list(system.RP),
        "RS": as_float_list(system.RS),
        "TP": as_float_list(system.TP),
        "TS": as_float_list(system.TS),
        "TT": float(system.TT),
    }


aluminum = trace_mirror(0)
gold = trace_mirror(1)

print("Aluminum mirror terms:", aluminum)
print("Gold mirror terms:", gold)
print("Aluminum first-surface average reflection:", (aluminum["RP"][0] + aluminum["RS"][0]) / 2.0)
print("Gold first-surface average reflection:", (gold["RP"][0] + gold["RS"][0]) / 2.0)
