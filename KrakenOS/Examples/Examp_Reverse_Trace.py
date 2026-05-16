#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example: reverse tracing through a simple doublet.

This example traces an on-axis ray forward through a compact doublet, then
starts from the image-plane hit point and traces backward toward the object
plane with `RvTrace`.

What this example teaches:
- how a normal forward `Trace` records image-plane coordinates
- how `RvTrace` can propagate from image space back toward object space
- how to choose `StopSurf` as the last real optical surface before the image
  plane in this compact example

Expected output:
- forward image-plane hit coordinates
- reverse-traced object-plane coordinates
- the difference between the original source and reverse-traced source

Units:
- distances are in millimeters
- wavelengths are in micrometers
"""

import sys
from pathlib import Path

import numpy as np


sys.path.append(str(Path(__file__).resolve().parents[2]))
import KrakenOS as Kos


def build_doublet():
    object_plane = Kos.surf(Thickness=10.0, Glass="AIR", Diameter=30.0)

    first_surface = Kos.surf()
    first_surface.Rc = 92.847
    first_surface.Thickness = 6.0
    first_surface.Glass = "BK7"
    first_surface.Diameter = 30.0

    second_surface = Kos.surf()
    second_surface.Rc = -30.716
    second_surface.Thickness = 3.0
    second_surface.Glass = "F2"
    second_surface.Diameter = 30.0

    last_lens_surface = Kos.surf()
    last_lens_surface.Rc = -78.197
    last_lens_surface.Thickness = 97.376
    last_lens_surface.Glass = "AIR"
    last_lens_surface.Diameter = 30.0

    image_plane = Kos.surf(Thickness=0.0, Glass="AIR", Diameter=5.0)
    image_plane.Name = "Image plane"

    return Kos.system(
        [object_plane, first_surface, second_surface, last_lens_surface, image_plane],
        Kos.Setup(),
    )


system = build_doublet()
wavelength = 0.55
source = np.asarray([0.0, 0.0, 0.0])
forward_direction = [0.0, 0.0, 1.0]

system.Trace(source, forward_direction, wavelength)
image_hit = np.asarray(system.XYZ[-1])

print("Forward trace valid:", bool(system.val))
print("Forward image-plane hit [x, y, z]:", [float(value) for value in image_hit])

# In this five-surface system, surface 3 is the last lens surface before the
# image plane. Reverse tracing starts at the image point and walks back through
# surfaces 3, 2, 1, and 0.
stop_surface = 3
reverse_direction = [0.0, 0.0, -1.0]

system.RvTrace(image_hit, reverse_direction, wavelength, stop_surface)
reverse_source = np.asarray(system.XYZ[-1])
source_error = reverse_source - source

print("Reverse trace valid:", bool(system.val))
print("Reverse-traced object point [x, y, z]:", [float(value) for value in reverse_source])
print("Reverse source error [dx, dy, dz]:", [float(value) for value in source_error])
print("Reverse surface order:", [int(value) for value in system.SURFACE])
