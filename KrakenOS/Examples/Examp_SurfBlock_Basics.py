#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example: reusable lens assemblies with SurfBlock.

This example loads two packaged THORLABS catalog entries, wraps them as
`SurfBlock` components, aligns them with explicit air gaps, and traces a small
ray fan through the assembled relay.

What this example teaches:
- how `SurfBlock` turns a catalog entry into a reusable component
- how `alignment` expands a mixed list of surfaces and blocks
- how named blocks can receive spacing through the `Distances` dictionary

Expected output:
- the expanded surface sequence
- the number of rays traced
- the final image-plane hit for the last traced ray

Didactic note:
- the `display2d` call near the end is intentionally commented. Uncomment it
  to inspect the assembled relay graphically.

Units:
- distances are in millimeters
- wavelengths are in micrometers
"""

import contextlib
import io
import sys
from importlib import resources
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parents[2]))
import KrakenOS as Kos


catalog_path = resources.files("KrakenOS") / "LensCat" / "THORLABS.ZMF"
with contextlib.redirect_stdout(io.StringIO()):
    catalog = Kos.zmf2dict([catalog_path])

object_plane = Kos.surf(Diameter=25.4, Thickness=20.0)
image_plane = Kos.surf(Diameter=25.4, Thickness=0.0, Name="Image plane")

lens_list = [
    object_plane,
    Kos.SurfBlock(catalog["AC254-050-A"], name="achromat"),
    Kos.SurfBlock(catalog["LA1509-A"], name="plano_convex"),
    image_plane,
]

distances = {
    "achromat": 35.0,
    "plano_convex": 50.0,
}

surfaces = Kos.alignment(lens_list, distances)

print("Expanded surface sequence:")
for index, surface in enumerate(surfaces):
    name = surface.Name if surface.Name else "(unnamed)"
    print(
        f"  {index}: {name}, "
        f"Thickness={surface.Thickness:.6g}, "
        f"Glass={surface.Glass}, "
        f"Diameter={surface.Diameter:.6g}"
    )

system = Kos.system(surfaces, Kos.Setup())
rays = Kos.raykeeper(system)

for y_source in [-2.0, 0.0, 2.0]:
    system.Trace([0.0, y_source, 0.0], [0.0, 0.0, 1.0], 0.55)
    rays.push()

print("Number of traced rays:", rays.nrays)
print("Last trace valid:", bool(system.val))
print("Last image-plane hit [x, y, z]:", [float(value) for value in system.XYZ[-1]])

# Optional didactic display:
# Kos.display2d(system, rays, 0)
