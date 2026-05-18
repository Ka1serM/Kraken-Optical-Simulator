#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example: doublet lens pupil rays traced as a bundle.

This example follows the same optical layout used in
``Examp_Doublet_Lens_Pupil.py``.  The difference is that the ray set generated
by ``PupilCalc.Pattern2Field()`` is traced in two ways:

- the classic KrakenOS loop, calling ``system.Trace()`` one ray at a time;
- the experimental internal ``trace_bundle()`` helper, tracing all pupil rays
  together as arrays.

The pupil tool already returns ray origins and direction cosines as arrays:
``x, y, z, L, M, N``.  That makes it a natural source for bundle tracing.

Didactic note:
- ``trace_bundle()`` is still experimental and is not imported from
  ``KrakenOS.__init__``.  It is used here explicitly to test the future
  ray-bundle workflow without changing the public ``system.Trace()`` API.
"""

import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[2]))

import KrakenOS as Kos
from KrakenOS.BundleTrace import trace_bundle


def build_doublet_pupil_system():
    # Object plane.
    p_obj = Kos.surf()
    p_obj.Rc = 0.0
    p_obj.Thickness = 100.0
    p_obj.Glass = "AIR"
    p_obj.Diameter = 30.0
    p_obj.Name = "P_Obj"

    # First lens surface.
    l1a = Kos.surf()
    l1a.Rc = 9.284706570002484e1
    l1a.Thickness = 6.0
    l1a.Glass = "BK7"
    l1a.Diameter = 30.0

    # Second lens surface.
    l1b = Kos.surf()
    l1b.Rc = -3.071608670000159e1
    l1b.Thickness = 3.0
    l1b.Glass = "F2"
    l1b.Diameter = 30.0

    # Air gap before pupil and image plane.
    l1c = Kos.surf()
    l1c.Rc = -7.819730726078505e1
    l1c.Thickness = 9.737604742910693e1 - 40.0
    l1c.Glass = "AIR"
    l1c.Diameter = 30.0

    # Stop/pupil surface.
    pupil = Kos.surf()
    pupil.Rc = 0.0
    pupil.Thickness = 40.0
    pupil.Glass = "AIR"
    pupil.Diameter = 3.0
    pupil.Name = "Pupil"
    pupil.Nm_Pos = (-10, 10)

    # Image plane.
    p_ima = Kos.surf()
    p_ima.Rc = 0.0
    p_ima.Thickness = 0.0
    p_ima.Glass = "AIR"
    p_ima.Diameter = 20.0
    p_ima.Name = "P_Ima"
    p_ima.Nm_Pos = (-10, 10)

    surfaces = [p_obj, l1a, l1b, l1c, pupil, p_ima]
    return Kos.system(surfaces, Kos.Setup(), build=0)


def make_pupil_ray_bundle(system, wavelength):
    sup = 4
    aperture_value = 3.0
    aperture_type = "STOP"
    pupil = Kos.PupilCalc(system, sup, wavelength, aperture_type, aperture_value)

    print("Input pupil radius:")
    print(pupil.RadPupInp)
    print("Input pupil position:")
    print(pupil.PosPupInp)
    print("Output pupil radius:")
    print(pupil.RadPupOut)
    print("Output pupil position:")
    print(pupil.PosPupOut)
    print("Output pupil orientation:")
    print(pupil.DirPupSal)
    print("Airy disk diameter at focal distance (micrometers):")
    print(pupil.FocusAiryRadius)

    pupil.Samp = 10
    pupil.Ptype = "hexapolar"
    pupil.FieldType = "angle"

    origins = []
    directions = []
    for field_y in [2.0, -2.0]:
        pupil.FieldY = field_y
        x, y, z, l, m, n = pupil.Pattern2Field()

        # Keep this performance comparison away from the exact pupil rim.  Rays
        # on the normalized radius r = 1 boundary are useful for aperture tests,
        # but here they can expose tiny floating-point differences in aperture
        # inclusion.  The goal of this example is to compare scalar tracing with
        # bundled tracing for the same clean interior pupil ray set.
        normalized_radius = np.sqrt((pupil.Cordx * pupil.Cordx) + (pupil.Cordy * pupil.Cordy))
        interior = normalized_radius < 0.98

        origins.append(np.column_stack([x[interior], y[interior], z[interior]]))
        directions.append(np.column_stack([l[interior], m[interior], n[interior]]))

    return np.vstack(origins), np.vstack(directions)


def scalar_trace(system, origins, directions, wavelength):
    active = []
    final_hits = []
    final_directions = []

    start = time.perf_counter()
    for origin, direction in zip(origins, directions):
        system.Trace(origin, direction, wavelength)
        valid = system.val == 1
        active.append(valid)
        final_hits.append(np.asarray(system.XYZ[-1], dtype=float))
        if valid:
            final_directions.append(np.asarray(system.R_LMN[-1], dtype=float))
        else:
            final_directions.append(np.zeros(3))
    elapsed = time.perf_counter() - start

    return {
        "active": np.asarray(active, dtype=bool),
        "final_hits": np.asarray(final_hits, dtype=float),
        "final_directions": np.asarray(final_directions, dtype=float),
        "elapsed": elapsed,
    }


def bundle_trace(system, origins, directions, wavelength):
    start = time.perf_counter()
    result = trace_bundle(system, origins, directions, wavelength)
    result["elapsed"] = time.perf_counter() - start
    return result


def spot_metrics(points):
    cen_x = np.mean(points[:, 0])
    cen_y = np.mean(points[:, 1])
    dx = points[:, 0] - cen_x
    dy = points[:, 1] - cen_y
    radius = np.sqrt((dx * dx) + (dy * dy))
    return {
        "centroid": (cen_x, cen_y),
        "rms": np.sqrt(np.mean(radius * radius)),
        "max_radius": np.max(radius),
    }


def main():
    wavelength = 0.4

    # Use one system to compute the pupil-generated input bundle, and separate
    # systems for the scalar and bundle traces so their internal ray state is
    # independent.
    pupil_system = build_doublet_pupil_system()
    origins, directions = make_pupil_ray_bundle(pupil_system, wavelength)

    scalar_system = build_doublet_pupil_system()
    bundle_system = build_doublet_pupil_system()

    scalar = scalar_trace(scalar_system, origins, directions, wavelength)
    bundle = bundle_trace(bundle_system, origins, directions, wavelength)

    active = scalar["active"]
    max_hit_error = np.max(
        np.abs(bundle["final_hits"][active] - scalar["final_hits"][active])
    )
    max_direction_error = np.max(
        np.abs(bundle["final_directions"][active] - scalar["final_directions"][active])
    )

    scalar_metrics = spot_metrics(scalar["final_hits"][active])
    bundle_metrics = spot_metrics(bundle["final_hits"][active])
    speedup = scalar["elapsed"] / bundle["elapsed"] if bundle["elapsed"] > 0.0 else float("inf")

    print("\nDoublet pupil bundle tracing")
    print("Both traces use the same pupil-generated ray origins and directions.")
    print(f"Rays generated by PupilCalc: {len(origins)}")
    print(f"Active rays: {np.count_nonzero(active)}")
    print(f"Scalar Trace time: {scalar['elapsed']:.6f} s")
    print(f"Bundle Trace time: {bundle['elapsed']:.6f} s")
    print(f"Speedup: {speedup:.3f}x")
    print(f"Same active mask: {np.array_equal(bundle['active'], scalar['active'])}")
    print(f"Max final hit error: {max_hit_error:.3e} mm")
    print(f"Max final direction error: {max_direction_error:.3e}")
    print(f"Scalar RMS spot: {scalar_metrics['rms']:.6e} mm")
    print(f"Bundle RMS spot: {bundle_metrics['rms']:.6e} mm")

    fig, ax = plt.subplots(1, 1, figsize=(6, 5), constrained_layout=True)
    ax.plot(bundle["final_hits"][active, 0], bundle["final_hits"][active, 1], "x")
    ax.set_title("Doublet pupil rays traced as one bundle")
    ax.set_xlabel("image x [mm]")
    ax.set_ylabel("image y [mm]")
    ax.axis("equal")
    ax.grid(True, alpha=0.25)
    plt.show()


if __name__ == "__main__":
    main()
