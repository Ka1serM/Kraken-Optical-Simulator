"""Experimental sequential ray-bundle tracing example.

This example compares the established scalar ``system.Trace()`` workflow with
the internal experimental ``trace_bundle()`` helper.  The bundle helper is not a
public KrakenOS API yet; it is a development tool for testing whether many
sequential rays can be processed together without changing optical results.

The systems are intentionally simple and use ``build=0``.  The example does not
use display or PyVista visualization.
"""

import sys
from pathlib import Path
from time import perf_counter

import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[2]))

import KrakenOS as Kos
from KrakenOS.BundleTrace import trace_bundle


def build_simple_lens_system():
    obj = Kos.surf()
    obj.Glass = "AIR"
    obj.Thickness = 10.0
    obj.Diameter = 40.0

    lens_front = Kos.surf()
    lens_front.Rc = 80.0
    lens_front.Glass = "BK7"
    lens_front.Thickness = 5.0
    lens_front.Diameter = 40.0

    lens_back = Kos.surf()
    lens_back.Rc = -80.0
    lens_back.Glass = "AIR"
    lens_back.Thickness = 20.0
    lens_back.Diameter = 40.0

    image = Kos.surf()
    image.Glass = "AIR"
    image.Thickness = 0.0
    image.Diameter = 40.0

    return Kos.system([obj, lens_front, lens_back, image], Kos.Setup(), build=0)


def build_zernike_axis_system():
    obj = Kos.surf()
    obj.Glass = "AIR"
    obj.Thickness = 10.0
    obj.Diameter = 40.0

    shaped = Kos.surf()
    shaped.Glass = "BK7"
    shaped.Thickness = 5.0
    shaped.Diameter = 40.0
    shaped.ZNK = np.zeros(36)
    shaped.ZNK[2] = 0.003

    lens_back = Kos.surf()
    lens_back.Rc = -90.0
    lens_back.Glass = "AIR"
    lens_back.Thickness = 20.0
    lens_back.Diameter = 40.0

    image = Kos.surf()
    image.Glass = "AIR"
    image.Thickness = 0.0
    image.Diameter = 40.0

    return Kos.system([obj, shaped, lens_back, image], Kos.Setup(), build=0)


def build_axicon_apex_system():
    obj = Kos.surf()
    obj.Glass = "AIR"
    obj.Thickness = 10.0
    obj.Diameter = 40.0

    axicon = Kos.surf()
    axicon.Glass = "BK7"
    axicon.Thickness = 5.0
    axicon.Diameter = 40.0
    axicon.Axicon = 1.5

    lens_back = Kos.surf()
    lens_back.Rc = -90.0
    lens_back.Glass = "AIR"
    lens_back.Thickness = 20.0
    lens_back.Diameter = 40.0

    image = Kos.surf()
    image.Glass = "AIR"
    image.Thickness = 0.0
    image.Diameter = 40.0

    return Kos.system([obj, axicon, lens_back, image], Kos.Setup(), build=0)


def build_user_surface_without_derivative_system():
    def user_surface(x, y, data):
        return data[0] * x * y

    obj = Kos.surf()
    obj.Glass = "AIR"
    obj.Thickness = 10.0
    obj.Diameter = 40.0

    shaped = Kos.surf()
    shaped.Glass = "BK7"
    shaped.Thickness = 5.0
    shaped.Diameter = 40.0
    shaped.ExtraData = [user_surface, [0.002]]

    lens_back = Kos.surf()
    lens_back.Rc = -90.0
    lens_back.Glass = "AIR"
    lens_back.Thickness = 20.0
    lens_back.Diameter = 40.0

    image = Kos.surf()
    image.Glass = "AIR"
    image.Thickness = 0.0
    image.Diameter = 40.0

    return Kos.system([obj, shaped, lens_back, image], Kos.Setup(), build=0)


def make_grid_rays(samples_per_axis):
    axis = np.linspace(-8.0, 8.0, samples_per_axis)
    x, y = np.meshgrid(axis, axis)
    origins = np.column_stack([x.ravel(), y.ravel(), np.zeros(x.size)])
    directions = np.tile(np.array([0.0, 0.0, 1.0]), (origins.shape[0], 1))
    return origins, directions


def make_fallback_rays():
    origins = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [-1.0, 0.5, 0.0],
            [2.0, -1.0, 0.0],
        ],
        dtype=float,
    )
    directions = np.tile(np.array([0.0, 0.0, 1.0]), (origins.shape[0], 1))
    return origins, directions


def scalar_trace(system, origins, directions, wavelength):
    active = []
    final_hits = []
    final_directions = []

    for origin, direction in zip(origins, directions):
        system.Trace(origin, direction, wavelength)
        valid = system.val == 1
        active.append(valid)
        final_hits.append(np.asarray(system.XYZ[-1], dtype=float))
        if valid:
            final_directions.append(np.asarray(system.R_LMN[-1], dtype=float))
        else:
            final_directions.append(np.zeros(3))

    return {
        "active": np.asarray(active, dtype=bool),
        "final_hits": np.asarray(final_hits, dtype=float),
        "final_directions": np.asarray(final_directions, dtype=float),
    }


def compare_results(label, system, origins, directions, wavelength=0.55, repetitions=1):
    scalar_start = perf_counter()
    scalar = None
    for _ in range(repetitions):
        scalar = scalar_trace(system, origins, directions, wavelength)
    scalar_time = perf_counter() - scalar_start

    bundle_start = perf_counter()
    bundle = None
    for _ in range(repetitions):
        bundle = trace_bundle(system, origins, directions, wavelength)
    bundle_time = perf_counter() - bundle_start

    active = scalar["active"]
    if np.any(active):
        hit_error = np.max(
            np.abs(bundle["final_hits"][active] - scalar["final_hits"][active])
        )
        direction_error = np.max(
            np.abs(
                bundle["final_directions"][active]
                - scalar["final_directions"][active]
            )
        )
    else:
        hit_error = 0.0
        direction_error = 0.0

    same_active = np.array_equal(bundle["active"], scalar["active"])
    speedup = scalar_time / bundle_time if bundle_time > 0.0 else float("inf")

    print()
    print(label)
    print("-" * len(label))
    print(f"Rays: {len(origins)}")
    print(f"Repetitions: {repetitions}")
    print(f"Active rays: {np.count_nonzero(active)}")
    print(f"Scalar Trace time: {scalar_time:.6f} s")
    print(f"Bundle Trace time: {bundle_time:.6f} s")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Same active mask: {same_active}")
    print(f"Max final hit error: {hit_error:.3e} mm")
    print(f"Max final direction error: {direction_error:.3e}")


def main():
    print("Experimental trace_bundle comparison")
    print("This helper is internal and may change before becoming public.")

    origins, directions = make_grid_rays(samples_per_axis=25)
    compare_results(
        "Simple spherical lens, vectorized path",
        build_simple_lens_system(),
        origins,
        directions,
        repetitions=25,
    )

    fallback_origins, fallback_directions = make_fallback_rays()
    compare_results(
        "Zernike surface with central-ray fallback",
        build_zernike_axis_system(),
        fallback_origins,
        fallback_directions,
    )
    compare_results(
        "Axicon surface with apex fallback",
        build_axicon_apex_system(),
        fallback_origins,
        fallback_directions,
    )
    compare_results(
        "User ExtraData surface without analytical derivative",
        build_user_surface_without_derivative_system(),
        fallback_origins,
        fallback_directions,
    )


if __name__ == "__main__":
    main()
