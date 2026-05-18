"""Experimental vectorized sequential ray-bundle tracing helpers.

This module is intentionally internal for now.  It is not imported from
``KrakenOS.__init__`` and should not be treated as public API yet.  The goal is
to gather the bundle-tracing prototype in one place while preserving the
existing scalar ``system.Trace()`` workflow.

Current scope:

- sequential ``build=0`` systems;
- ordinary analytical surfaces with analytical derivatives;
- circular aperture checks;
- refractive/mirror Snell physics following the current scalar implementation.

Still limited in this first experimental module:

- STL and non-sequential tracing;
- UDA/mask geometry beyond the simple circular aperture contract;
- fully vectorized numerical derivative fallback for bundle normals;
- complete coating/energy bookkeeping for reconstructed raykeeper records.
"""

import numpy as np


def transform_points_bundle(matrix, points):
    """Apply a KrakenOS homogeneous transform matrix to many points."""

    matrix = np.asarray(matrix, dtype=float)
    points = np.asarray(points, dtype=float)
    homogeneous = np.column_stack(
        [points[:, 0], points[:, 1], points[:, 2], np.ones(points.shape[0])]
    )
    return homogeneous @ matrix.T


def transform_directions_bundle(matrix, directions):
    """Apply a KrakenOS homogeneous transform matrix to many directions."""

    matrix = np.asarray(matrix, dtype=float)
    directions = np.asarray(directions, dtype=float)
    homogeneous = np.column_stack(
        [
            directions[:, 0],
            directions[:, 1],
            directions[:, 2],
            np.zeros(directions.shape[0]),
        ]
    )
    return homogeneous @ matrix.T


def _scalar_solve_hit(surface, px1, py1, pz1, l, m, n):
    """Use the established scalar solver for one ray as a fallback."""

    from .HitOnSurf import Hit_Solver

    solver = Hit_Solver([surface])
    return solver.SolveHit(px1, py1, pz1, l, m, n, 0)


def _scalar_surface_normal(surface, x, y, z):
    """Use the established scalar normal solver for one point as a fallback."""

    from .HitOnSurf import Hit_Solver

    solver = Hit_Solver([surface])
    solver.vj = 0
    return solver.SurfDer(x, y, z)


def solve_hit_bundle(surface, px1, py1, pz1, l, m, n, case=0, tolerance=1e-9):
    """Solve ray-surface intersections for a bundle using vectorized Newton.

    Rays whose active surface cannot provide an analytical derivative are
    solved by the established scalar ``Hit_Solver.SolveHit`` path.  That keeps
    the common analytical subset vectorized while preserving compatibility for
    isolated singular rays such as a Zernike axis point or axicon apex.
    """

    px1 = np.asarray(px1, dtype=float)
    py1 = np.asarray(py1, dtype=float)
    pz1 = np.asarray(pz1, dtype=float)
    l = np.asarray(l, dtype=float)
    m = np.asarray(m, dtype=float)
    n = np.asarray(n, dtype=float)

    ln = l / n
    mn = m / n
    z = np.array(pz1, dtype=float, copy=True)
    unresolved = np.ones_like(z, dtype=bool)

    for _ in range(30):
        if not np.any(unresolved):
            break

        x = ((z - pz1) * ln) + px1
        y = ((z - pz1) * mn) + py1

        sag = surface.sigma_z(x[unresolved], y[unresolved], case)
        derivative = surface.sigma_derivative(x[unresolved], y[unresolved], case)
        if derivative is None:
            active_indices = np.flatnonzero(unresolved)
            analytical_indices = []
            dzdx_values = []
            dzdy_values = []

            for index in active_indices:
                scalar_derivative = surface.sigma_derivative(float(x[index]), float(y[index]), case)
                if scalar_derivative is None:
                    z[index] = _scalar_solve_hit(
                        surface,
                        float(px1[index]),
                        float(py1[index]),
                        float(pz1[index]),
                        float(l[index]),
                        float(m[index]),
                        float(n[index]),
                    )[2]
                    unresolved[index] = False
                else:
                    analytical_indices.append(index)
                    dzdx_values.append(scalar_derivative[0])
                    dzdy_values.append(scalar_derivative[1])

            if not analytical_indices:
                continue

            step_indices = np.asarray(analytical_indices, dtype=int)
            sag = surface.sigma_z(x[step_indices], y[step_indices], case)
            dzdx = np.asarray(dzdx_values, dtype=float)
            dzdy = np.asarray(dzdy_values, dtype=float)
        else:
            step_indices = np.flatnonzero(unresolved)
            dzdx, dzdy = derivative

        function_value = sag - z[step_indices]
        function_derivative = (dzdx * ln[step_indices]) + (dzdy * mn[step_indices]) - 1.0
        next_z = z[step_indices] - (function_value / function_derivative)

        converged = np.abs(next_z - z[step_indices]) <= tolerance
        z[step_indices] = next_z
        unresolved[step_indices[converged]] = False

    x = ((z - pz1) * ln) + px1
    y = ((z - pz1) * mn) + py1
    return x, y, z


def local_normals_bundle(surface, x, y, z):
    """Return local normals for many surface hit points.

    Analytical derivatives are used where available. Points whose derivative is
    singular or unsupported use the established scalar finite-difference normal
    path, preserving compatibility while keeping the common analytical subset
    vectorized.
    """

    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    z = np.asarray(z, dtype=float)

    derivative = surface.sigma_derivative(x, y, 0)
    if derivative is None:
        normals = np.empty((x.shape[0], 3), dtype=float)
        analytical_indices = []
        dzdx_values = []
        dzdy_values = []

        for index in range(x.shape[0]):
            scalar_derivative = surface.sigma_derivative(float(x[index]), float(y[index]), 0)
            if scalar_derivative is None:
                normals[index] = _scalar_surface_normal(
                    surface,
                    float(x[index]),
                    float(y[index]),
                    float(z[index]),
                )
            else:
                analytical_indices.append(index)
                dzdx_values.append(scalar_derivative[0])
                dzdy_values.append(scalar_derivative[1])

        if analytical_indices:
            step_indices = np.asarray(analytical_indices, dtype=int)
            dzdx = np.asarray(dzdx_values, dtype=float)
            dzdy = np.asarray(dzdy_values, dtype=float)
            analytical_normals = np.column_stack([dzdx, dzdy, -np.ones_like(dzdx)])
            normals[step_indices] = analytical_normals / np.linalg.norm(
                analytical_normals,
                axis=1,
            )[:, None]
        return normals

    dzdx, dzdy = derivative
    normals = np.column_stack([dzdx, dzdy, -np.ones_like(z)])
    return normals / np.linalg.norm(normals, axis=1)[:, None]


def aperture_active_mask(surface, x, y):
    """Return the simple circular aperture active mask for a ray bundle."""

    scale, center_y, center_x = surface.SubAperture
    radial_distance = np.sqrt(((x - center_x) ** 2.0) + ((y - center_y) ** 2.0))
    diameter_at_point = 2.0 * radial_distance
    return (
        (diameter_at_point <= surface.Diameter * scale)
        & (diameter_at_point >= surface.InDiameter * scale)
    )


def inter_normal_bundle(system, starts, stops, surface_index):
    """Experimental bundle equivalent of the simple sequential InterNormal path."""

    surface = system.SDT[surface_index]
    start_local = transform_points_bundle(system.Pr3D.TRANS_1A[surface_index], starts)[:, :3]
    stop_local = transform_points_bundle(system.Pr3D.TRANS_1A[surface_index], stops)[:, :3]
    segment = stop_local - start_local
    local_direction = segment / np.linalg.norm(segment, axis=1)[:, None]

    px0 = start_local[:, 0]
    py0 = start_local[:, 1]
    pz0 = start_local[:, 2]
    l = local_direction[:, 0]
    m = local_direction[:, 1]
    n = local_direction[:, 2]

    px1 = ((l / n) * (-pz0)) + px0
    py1 = ((m / n) * (-pz0)) + py0
    pz1 = np.zeros_like(px1)

    hit_x, hit_y, hit_z = solve_hit_bundle(surface, px1, py1, pz1, l, m, n)
    active = aperture_active_mask(surface, hit_x, hit_y)
    local_hits = np.column_stack([hit_x, hit_y, hit_z])
    global_hits = transform_points_bundle(system.Pr3D.TRANS_2A[surface_index], local_hits)[:, :3]

    local_normals = local_normals_bundle(surface, hit_x, hit_y, hit_z)
    normal_reference_z = 10000000.0
    normal_p1_x = (
        ((normal_reference_z - hit_z) * (local_normals[:, 0] / local_normals[:, 2]))
        + hit_x
    )
    normal_p1_y = (
        ((normal_reference_z - hit_z) * (local_normals[:, 1] / local_normals[:, 2]))
        + hit_y
    )
    normal_p1 = np.column_stack(
        [normal_p1_x, normal_p1_y, np.full_like(hit_z, normal_reference_z)]
    )
    global_p1 = transform_points_bundle(system.Pr3D.TRANS_2A[surface_index], normal_p1)[:, :3]
    global_p2 = transform_points_bundle(system.Pr3D.TRANS_2A[surface_index], local_hits)[:, :3]
    global_normals = -(global_p1 - global_p2)
    global_normals = global_normals / np.linalg.norm(global_normals, axis=1)[:, None]

    return active, global_hits, global_normals, local_hits, local_direction


def snell_refraction_bundle(incident, normals, n1, n2):
    """Vectorized form of the current scalar Snell/reflection calculation."""

    nv = np.asarray(normals, dtype=float).copy()
    iv = np.asarray(incident, dtype=float)

    cos = np.sum(nv * iv, axis=1)
    angles = np.rad2deg(np.arccos(np.clip(cos, -1.0, 1.0)))
    flip = angles <= 90.0
    nv[flip] = -nv[flip]
    angles[~flip] = 180.0 - angles[~flip]

    sign = np.ones(iv.shape[0])
    n2_effective = np.full(iv.shape[0], n2, dtype=float)
    if n2 == -1.0:
        n2_effective[:] = -n1
        sign[:] = -1.0

    nn = n1 / n2_effective
    cross = np.cross(nv, iv)
    d22 = np.sum(cross * cross, axis=1)
    tir = ((nn * nn) * d22) > 1.0
    if np.any(tir):
        n2_effective[tir] = -n1
        nn = n1 / n2_effective
        sign[tir] = -1.0

    c1 = np.sum(nv * iv, axis=1)
    c1 = np.where(c1 < 0.0, np.sum((-nv) * iv, axis=1), c1)
    ip = (nn * nn) * (1.0 - (c1 * c1))
    c2 = np.sqrt(1.0 - ip)
    transmitted = (nn[:, None] * iv) + (((nn * c1) - c2)[:, None] * nv)
    return transmitted, np.abs(n2_effective), sign, angles


def trace_bundle(system, origins, directions, wavelength, keep_history=False):
    """Trace a bundle through a simple sequential system.

    This is experimental and intentionally narrower than ``system.Trace``.
    Set ``keep_history=True`` when the result will be converted into
    ``raykeeper`` records for display or analysis.
    """

    system.Wave = wavelength
    system._system__WavePrecalc()

    ray_origins = np.asarray(origins, dtype=float).copy()
    ray_directions = np.asarray(directions, dtype=float).copy()
    active = np.ones(ray_origins.shape[0], dtype=bool)
    propagation_sign = np.ones(ray_origins.shape[0], dtype=float)
    previous_n = system.N_Prec[0]
    final_hits = np.array(ray_origins, copy=True)
    final_directions = np.array(ray_directions, copy=True)

    if keep_history:
        ray_count = ray_origins.shape[0]
        global_hits = np.zeros((ray_count, system.n, 3), dtype=float)
        local_hits = np.zeros((ray_count, system.n, 3), dtype=float)
        incident_directions = np.zeros((ray_count, system.n - 1, 3), dtype=float)
        output_directions = np.zeros((ray_count, system.n - 1, 3), dtype=float)
        local_directions = np.zeros((ray_count, system.n - 1, 3), dtype=float)
        normals = np.zeros((ray_count, system.n - 1, 3), dtype=float)
        global_hits[:, 0, :] = ray_origins

    for surface_index in range(1, system.n):
        stops = ray_origins + (ray_directions * 999999999.9 * propagation_sign[:, None])
        hit_active, hits, normal_vectors, hit_local, direction_local = inter_normal_bundle(
            system, ray_origins, stops, surface_index
        )
        active = active & hit_active

        current_n = system.N_Prec[surface_index]
        next_directions, current_after_physics, sign, _angles = snell_refraction_bundle(
            ray_directions, normal_vectors, previous_n, current_n
        )
        propagation_sign = propagation_sign * sign

        if keep_history:
            history_index = surface_index - 1
            global_hits[:, surface_index, :] = hits
            local_hits[:, surface_index, :] = hit_local
            incident_directions[:, history_index, :] = ray_directions
            output_directions[:, history_index, :] = next_directions
            local_directions[:, history_index, :] = direction_local
            normals[:, history_index, :] = normal_vectors

        ray_origins[active] = hits[active]
        ray_directions[active] = next_directions[active]
        final_hits[active] = hits[active]
        final_directions[active] = next_directions[active]
        previous_n = current_after_physics[0]

    result = {
        "active": active,
        "final_hits": final_hits,
        "final_directions": final_directions,
    }
    if keep_history:
        result.update(
            {
                "wavelength": wavelength,
                "global_hits": global_hits,
                "local_hits": local_hits,
                "incident_directions": incident_directions,
                "output_directions": output_directions,
                "local_directions": local_directions,
                "normals": normals,
            }
        )
    return result


def bundle_to_raykeeper_results(system, bundle_result, wavelength=None):
    """Convert a history-enabled bundle result into raykeeper result records.

    The conversion is intentionally conservative.  It reconstructs the spatial
    ray path and direction data needed by ``raykeeper.pick`` and display tools,
    while filling coating/energy terms with neutral values until the bundled
    tracer grows full coating bookkeeping.
    """

    if "global_hits" not in bundle_result:
        raise ValueError("trace_bundle(..., keep_history=True) is required")

    wave = bundle_result.get("wavelength", wavelength)
    if wave is None:
        wave = system.Wave

    global_hits = bundle_result["global_hits"]
    local_hits = bundle_result["local_hits"]
    incident_directions = bundle_result["incident_directions"]
    output_directions = bundle_result["output_directions"]
    local_directions = bundle_result["local_directions"]
    normals = bundle_result["normals"]
    active = bundle_result["active"]

    surfaces = list(range(1, system.n))
    names = [system.SDT[index].Name for index in surfaces]
    glasses = [system.SDT[index].Glass for index in surfaces]
    n0_values = [system.N_Prec[index - 1] for index in surfaces]
    n1_values = [system.N_Prec[index] for index in surfaces]

    results = []
    for ray_index in range(global_hits.shape[0]):
        starts = global_hits[ray_index, :-1, :]
        stops = global_hits[ray_index, 1:, :]
        distance = np.linalg.norm(stops - starts, axis=1)
        optical_path = distance * np.asarray(n1_values, dtype=float)
        top_s = np.cumsum(optical_path)
        total_path = top_s[-1] if len(top_s) else 0.0

        results.append(
            {
                "nelements": system.n,
                "val": int(active[ray_index]),
                "Wave": wave,
                "ray_SurfHits": np.asarray(global_hits[ray_index]),
                "SURFACE": surfaces,
                "NAME": names,
                "GLASS": glasses,
                "S_XYZ": list(starts),
                "T_XYZ": list(stops),
                "XYZ": list(global_hits[ray_index]),
                "OST_XYZ": list(local_hits[ray_index]),
                "OST_LMN": list(local_directions[ray_index]),
                "S_LMN": list(normals[ray_index]),
                "LMN": list(incident_directions[ray_index]),
                "R_LMN": list(output_directions[ray_index]),
                "N0": n0_values,
                "N1": n1_values,
                "WAV": wave,
                "G_LMN": [np.asarray([0, 1, 0])] * (system.n - 1),
                "ORDER": [0.0] * (system.n - 1),
                "GRATING": [0.0] * (system.n - 1),
                "DISTANCE": list(distance),
                "OP": list(optical_path),
                "TOP_S": list(top_s),
                "TOP": total_path,
                "ALPHA": [0.0] * (system.n + 1),
                "BULK_TRANS": [1.0] * (system.n - 1),
                "RP": [0.0] * (system.n - 1),
                "RS": [0.0] * (system.n - 1),
                "TP": [1.0] * (system.n - 1),
                "TS": [1.0] * (system.n - 1),
                "TTBE": [1.0] * (system.n - 1),
                "TT": 1.0,
            }
        )
    return results
