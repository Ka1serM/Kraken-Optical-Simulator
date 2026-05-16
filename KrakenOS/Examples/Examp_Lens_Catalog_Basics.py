#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example: basic Zemax-style lens catalog loading.

This example loads the packaged THORLABS ZMF catalog, lists a few available
part numbers, converts one catalog entry to KrakenOS surfaces, and traces a
single on-axis ray through the converted lens.

What this example teaches:
- how to access packaged lens catalog files with `importlib.resources`
- how to read a ZMF catalog with `Kos.zmf2dict`
- how to convert a catalog entry with `Kos.cat2surf`
- how to inspect the resulting `surf` objects before building a system

Expected output:
- the number of catalog entries found
- a few example part numbers
- the converted surface prescription
- the final ray intersection at the image plane

Didactic note:
- the `display2d` call near the end is intentionally commented. Uncomment it
  to inspect the catalog lens layout graphically.

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

# `zmf2dict` prints the path of each catalog as it reads it. The example keeps
# the console focused on the didactic output below.
with contextlib.redirect_stdout(io.StringIO()):
    catalog = Kos.zmf2dict([catalog_path])

part_number = "AC254-050-A"
lens_data = catalog[part_number]
surfaces = Kos.cat2surf(lens_data, Thickness=50.0, Glass="AIR")

print("Catalog file:", catalog_path.name)
print("Number of loaded entries:", len(catalog))
print("First five part numbers:", list(catalog.keys())[:5])
print("Selected part number:", part_number)
print("Description:", lens_data.get("description"))
print("Converted surfaces:")

for index, surface in enumerate(surfaces):
    print(
        f"  {index}: Rc={surface.Rc:.6g}, "
        f"Thickness={surface.Thickness:.6g}, "
        f"Glass={surface.Glass}, "
        f"Diameter={surface.Diameter:.6g}"
    )

object_plane = Kos.surf(Thickness=20.0, Glass="AIR", Diameter=25.4)
image_plane = Kos.surf(Thickness=0.0, Glass="AIR", Diameter=25.4)
image_plane.Name = "Image plane"

system = Kos.system([object_plane] + surfaces + [image_plane], Kos.Setup())
rays = Kos.raykeeper(system)

system.Trace([0.0, 0.0, 0.0], [0.0, 0.0, 1.0], 0.55)
rays.push()

print("Trace valid:", bool(system.val))
print("Image-plane hit [x, y, z]:", [float(value) for value in system.XYZ[-1]])

# Optional didactic display:
# Kos.display2d(system, rays, 0)
