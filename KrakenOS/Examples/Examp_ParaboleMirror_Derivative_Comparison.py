#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example: parabolic mirror image quality with analytical vs numerical slopes.

This example compares the same shifted parabolic mirror traced in two modes:

- analytical derivative mode, used automatically for conic/parabolic sag;
- numerical fallback mode, forced here only for comparison.

The optical model is intentionally close to ``Examp_ParaboleMirror_Shift.py``.
The comparison reports a simple RMS spot radius and plots both spot diagrams
side by side.

What this example teaches:
- a parabola is a conic surface, so KrakenOS can now use analytical sag slopes;
- the old finite-difference path is still available as a fallback;
- image quality can be compared from the traced ray data without changing the
  public ``system.Trace`` workflow.

Expected output:
- printed timing and RMS spot radius for both methods;
- side-by-side spot diagrams.
"""

import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[2]))
import KrakenOS as Kos


def build_parabolic_mirror_system(force_numerical_derivative=False):
    p_obj = Kos.surf()
    p_obj.Thickness = 1000.0
    p_obj.Diameter = 300.0
    p_obj.Drawing = 0

    mirror = Kos.surf()
    mirror.Rc = -2.0 * p_obj.Thickness
    mirror.Thickness = mirror.Rc / 2.0
    mirror.k = -1.0
    mirror.Glass = "MIRROR"
    mirror.Diameter = 300.0
    mirror.ShiftY = 200.0
    mirror.Name = "Shifted parabolic mirror"

    image = Kos.surf()
    image.Glass = "AIR"
    image.Diameter = 1600.0
    image.Drawing = 0
    image.Name = "Image plane"

    system = Kos.system([p_obj, mirror, image], Kos.Setup(), build=0)

    if force_numerical_derivative:
        # This is only for didactic comparison. It disables the new analytical
        # derivative route and forces KrakenOS to use the historical numerical
        # finite-difference derivative for every surface in this system.
        for surface in system.SDT:
            surface.sigma_derivative = lambda x, y, case: None

    return system


def trace_parabolic_mirror(system):
    rays = Kos.raykeeper(system)
    tam = 15
    radius = 150.0
    wavelength = 0.4

    start = time.perf_counter()
    for i in range(-tam, tam + 1):
        for j in range(-tam, tam + 1):
            x0 = (i / tam) * radius
            y0 = (j / tam) * radius
            if np.sqrt((x0 * x0) + (y0 * y0)) < radius:
                system.Trace([x0, y0, 0.0], [0.0, 0.0, 1.0], wavelength)
                rays.push()
    elapsed = time.perf_counter() - start

    return rays, elapsed


def spot_coordinates(rays):
    x, y, z, l, m, n = rays.pick(-1, coordinates="local")
    spot_x = ((l / n) * z) + x
    spot_y = ((m / n) * z) + y
    return np.asarray(spot_x), np.asarray(spot_y)


def spot_metrics(spot_x, spot_y):
    cen_x = np.mean(spot_x)
    cen_y = np.mean(spot_y)
    dx = spot_x - cen_x
    dy = spot_y - cen_y
    radius = np.sqrt((dx * dx) + (dy * dy))
    return {
        "centroid": (cen_x, cen_y),
        "rms": np.sqrt(np.mean(radius * radius)),
        "max_radius": np.max(radius),
    }


def run_case(label, force_numerical_derivative):
    system = build_parabolic_mirror_system(force_numerical_derivative)
    rays, elapsed = trace_parabolic_mirror(system)
    spot_x, spot_y = spot_coordinates(rays)
    metrics = spot_metrics(spot_x, spot_y)
    return {
        "label": label,
        "elapsed": elapsed,
        "rays": rays.nrays,
        "spot_x": spot_x,
        "spot_y": spot_y,
        "metrics": metrics,
    }


def plot_spot(ax, result):
    ax.plot(result["spot_x"], result["spot_y"], "x", markersize=4)
    ax.set_title(
        f"{result['label']}\n"
        f"RMS = {result['metrics']['rms']:.3e} mm"
    )
    ax.set_xlabel("x [mm]")
    ax.set_ylabel("y [mm]")
    ax.axis("equal")
    ax.grid(True, alpha=0.25)


def main():
    analytical = run_case("Analytical derivative", force_numerical_derivative=False)
    numerical = run_case("Numerical fallback", force_numerical_derivative=True)

    print("\nParabolic mirror derivative comparison")
    print(f"Rays traced: {analytical['rays']}")
    for result in [analytical, numerical]:
        centroid = result["metrics"]["centroid"]
        print(f"\n{result['label']}:")
        print(f"  time:       {result['elapsed']:.6f} s")
        print(f"  RMS spot:   {result['metrics']['rms']:.12e} mm")
        print(f"  max radius: {result['metrics']['max_radius']:.12e} mm")
        print(f"  centroid:   ({centroid[0]:.12e}, {centroid[1]:.12e}) mm")

    improvement = numerical["metrics"]["rms"] / analytical["metrics"]["rms"]
    print(f"\nRMS improvement factor: {improvement:.3f}x")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), constrained_layout=True)
    plot_spot(axes[0], analytical)
    plot_spot(axes[1], numerical)
    fig.suptitle("Shifted parabolic mirror spot comparison")
    plt.show()


if __name__ == "__main__":
    main()
