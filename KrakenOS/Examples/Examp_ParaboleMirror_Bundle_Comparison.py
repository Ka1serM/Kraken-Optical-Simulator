#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example: shifted parabolic mirror traced with and without ray bundles.

This example is a bundle-tracing version of
``Examp_ParaboleMirror_Derivative_Comparison.py``.  It compares two ways of
tracing the same shifted parabolic mirror under the same standard condition:
analytical sag derivatives enabled.

The comparison is:

- scalar ``system.Trace()`` called one ray at a time;
- experimental internal ``trace_bundle()`` called once for the whole ray set.

The important idea is that the physical model is not changed.  Both paths use
the same analytical derivative surface behavior; only the ray processing layout
changes.
"""

import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[2]))

import KrakenOS as Kos
from KrakenOS.BundleTrace import trace_bundle


def build_parabolic_mirror_system():
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

    return Kos.system([p_obj, mirror, image], Kos.Setup(), build=0)


def make_parabolic_mirror_rays(tam=15, radius=150.0):
    origins = []
    directions = []

    for i in range(-tam, tam + 1):
        for j in range(-tam, tam + 1):
            x0 = (i / tam) * radius
            y0 = (j / tam) * radius
            if np.sqrt((x0 * x0) + (y0 * y0)) < radius:
                origins.append([x0, y0, 0.0])
                directions.append([0.0, 0.0, 1.0])

    return np.asarray(origins, dtype=float), np.asarray(directions, dtype=float)


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


def spot_coordinates(result):
    active = result["active"]
    hits = result["final_hits"][active]
    directions = result["final_directions"][active]

    x = hits[:, 0]
    y = hits[:, 1]
    z = hits[:, 2]
    l = directions[:, 0]
    m = directions[:, 1]
    n = directions[:, 2]

    spot_x = ((l / n) * z) + x
    spot_y = ((m / n) * z) + y
    return spot_x, spot_y


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
        "rms_fm": np.sqrt(np.mean(radius * radius)) * 1.0e12,
        "max_radius_fm": np.max(radius) * 1.0e12,
    }


def run_case(origins, directions, wavelength):
    scalar_system = build_parabolic_mirror_system()
    bundle_system = build_parabolic_mirror_system()

    scalar = scalar_trace(scalar_system, origins, directions, wavelength)
    bundle = bundle_trace(bundle_system, origins, directions, wavelength)

    spot_x, spot_y = spot_coordinates(bundle)
    metrics = spot_metrics(spot_x, spot_y)

    active = scalar["active"]
    max_hit_error = np.max(
        np.abs(bundle["final_hits"][active] - scalar["final_hits"][active])
    )
    max_direction_error = np.max(
        np.abs(bundle["final_directions"][active] - scalar["final_directions"][active])
    )

    return {
        "label": "Analytical derivative standard condition",
        "rays": len(origins),
        "scalar": scalar,
        "bundle": bundle,
        "spot_x": spot_x,
        "spot_y": spot_y,
        "metrics": metrics,
        "same_active": np.array_equal(bundle["active"], scalar["active"]),
        "max_hit_error": max_hit_error,
        "max_direction_error": max_direction_error,
    }


def print_result(result):
    centroid = result["metrics"]["centroid"]
    scalar_time = result["scalar"]["elapsed"]
    bundle_time = result["bundle"]["elapsed"]
    speedup = scalar_time / bundle_time if bundle_time > 0.0 else float("inf")

    print(f"\n{result['label']}:")
    print(f"  rays:                  {result['rays']}")
    print(f"  scalar Trace time:     {scalar_time:.6f} s")
    print(f"  bundle Trace time:     {bundle_time:.6f} s")
    print(f"  speedup:               {speedup:.3f}x")
    print(f"  same active mask:      {result['same_active']}")
    print(f"  max final hit error:   {result['max_hit_error']:.3e} mm")
    print(f"  max direction error:   {result['max_direction_error']:.3e}")
    print(f"  RMS spot:              {result['metrics']['rms']:.12e} mm")
    print(f"                         {result['metrics']['rms_fm']:.6e} fm")
    print(f"  max radius:            {result['metrics']['max_radius']:.12e} mm")
    print(f"                         {result['metrics']['max_radius_fm']:.6e} fm")
    print(f"  centroid:              ({centroid[0]:.12e}, {centroid[1]:.12e}) mm")


def plot_spot(ax, result):
    cen_x, cen_y = result["metrics"]["centroid"]
    residual_x_fm = (result["spot_x"] - cen_x) * 1.0e12
    residual_y_fm = (result["spot_y"] - cen_y) * 1.0e12

    ax.plot(residual_x_fm, residual_y_fm, "x", markersize=4)
    ax.set_title(
        f"Bundle residual spot\nRMS = {result['metrics']['rms']:.3e} mm"
    )
    ax.set_xlabel("residual x [fm]")
    ax.set_ylabel("residual y [fm]")
    ax.axis("equal")
    ax.grid(True, alpha=0.25)


def main():
    wavelength = 0.4
    origins, directions = make_parabolic_mirror_rays(tam=15, radius=150.0)

    result = run_case(origins, directions, wavelength)

    print("\nParabolic mirror scalar vs bundle comparison")
    print("The bundle helper is experimental and internal.")
    print("Both paths use analytical sag derivatives.")
    print_result(result)
    print(
        "\nNote: the residual is at femtometer scale; visible bands are "
        "floating-point numerical floor, not physical structure."
    )

    fig, ax = plt.subplots(1, 1, figsize=(6, 5), constrained_layout=True)
    plot_spot(ax, result)
    fig.suptitle("Shifted parabolic mirror bundle residual spot")
    plt.show()


if __name__ == "__main__":
    main()
