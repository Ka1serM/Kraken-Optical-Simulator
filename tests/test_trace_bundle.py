import numpy as np

from KrakenOS.BundleTrace import trace_bundle


def build_simple_lens_system():
    import KrakenOS as Kos

    obj = Kos.surf()
    obj.Glass = "AIR"
    obj.Thickness = 10.0
    obj.Diameter = 30.0

    lens_front = Kos.surf()
    lens_front.Rc = 80.0
    lens_front.Glass = "BK7"
    lens_front.Thickness = 5.0
    lens_front.Diameter = 30.0

    lens_back = Kos.surf()
    lens_back.Rc = -80.0
    lens_back.Glass = "AIR"
    lens_back.Thickness = 20.0
    lens_back.Diameter = 30.0

    image = Kos.surf()
    image.Glass = "AIR"
    image.Thickness = 0.0
    image.Diameter = 30.0

    return Kos.system([obj, lens_front, lens_back, image], Kos.Setup(), build=0)


def build_tilted_decentered_lens_system():
    import KrakenOS as Kos

    obj = Kos.surf()
    obj.Glass = "AIR"
    obj.Thickness = 12.0
    obj.Diameter = 30.0

    lens_front = Kos.surf()
    lens_front.Rc = 90.0
    lens_front.Glass = "BK7"
    lens_front.Thickness = 5.0
    lens_front.Diameter = 30.0
    lens_front.TiltX = 2.0
    lens_front.TiltY = -1.0
    lens_front.DespX = 0.4
    lens_front.DespY = -0.2

    lens_back = Kos.surf()
    lens_back.Rc = -85.0
    lens_back.Glass = "AIR"
    lens_back.Thickness = 18.0
    lens_back.Diameter = 30.0
    lens_back.TiltX = -1.5
    lens_back.TiltY = 0.8
    lens_back.DespX = -0.2
    lens_back.DespY = 0.3

    image = Kos.surf()
    image.Glass = "AIR"
    image.Thickness = 0.0
    image.Diameter = 30.0

    return Kos.system([obj, lens_front, lens_back, image], Kos.Setup(), build=0)


def build_asphere_zernike_lens_system():
    import KrakenOS as Kos

    obj = Kos.surf()
    obj.Glass = "AIR"
    obj.Thickness = 10.0
    obj.Diameter = 30.0

    shaped = Kos.surf()
    shaped.Rc = 100.0
    shaped.Glass = "BK7"
    shaped.Thickness = 5.0
    shaped.Diameter = 30.0
    shaped.AspherData = np.zeros(200)
    shaped.AspherData[0] = 2e-8
    shaped.AspherData[2] = -1e-14
    shaped.ZNK = np.zeros(36)
    shaped.ZNK[2] = 0.003
    shaped.ZNK[5] = -0.001

    lens_back = Kos.surf()
    lens_back.Rc = -90.0
    lens_back.Glass = "AIR"
    lens_back.Thickness = 20.0
    lens_back.Diameter = 30.0

    image = Kos.surf()
    image.Glass = "AIR"
    image.Thickness = 0.0
    image.Diameter = 30.0

    return Kos.system([obj, shaped, lens_back, image], Kos.Setup(), build=0)


def build_zernike_axis_fallback_system():
    import KrakenOS as Kos

    obj = Kos.surf()
    obj.Glass = "AIR"
    obj.Thickness = 10.0
    obj.Diameter = 30.0

    shaped = Kos.surf()
    shaped.Glass = "BK7"
    shaped.Thickness = 5.0
    shaped.Diameter = 30.0
    shaped.ZNK = np.zeros(36)
    shaped.ZNK[2] = 0.003

    lens_back = Kos.surf()
    lens_back.Rc = -90.0
    lens_back.Glass = "AIR"
    lens_back.Thickness = 20.0
    lens_back.Diameter = 30.0

    image = Kos.surf()
    image.Glass = "AIR"
    image.Thickness = 0.0
    image.Diameter = 30.0

    return Kos.system([obj, shaped, lens_back, image], Kos.Setup(), build=0)


def build_axicon_apex_fallback_system():
    import KrakenOS as Kos

    obj = Kos.surf()
    obj.Glass = "AIR"
    obj.Thickness = 10.0
    obj.Diameter = 30.0

    axicon = Kos.surf()
    axicon.Glass = "BK7"
    axicon.Thickness = 5.0
    axicon.Diameter = 30.0
    axicon.Axicon = 1.5

    lens_back = Kos.surf()
    lens_back.Rc = -90.0
    lens_back.Glass = "AIR"
    lens_back.Thickness = 20.0
    lens_back.Diameter = 30.0

    image = Kos.surf()
    image.Glass = "AIR"
    image.Thickness = 0.0
    image.Diameter = 30.0

    return Kos.system([obj, axicon, lens_back, image], Kos.Setup(), build=0)


def build_extra_data_without_derivative_fallback_system():
    import KrakenOS as Kos

    def user_surface(x, y, data):
        return data[0] * x * y

    obj = Kos.surf()
    obj.Glass = "AIR"
    obj.Thickness = 10.0
    obj.Diameter = 30.0

    shaped = Kos.surf()
    shaped.Glass = "BK7"
    shaped.Thickness = 5.0
    shaped.Diameter = 30.0
    shaped.ExtraData = [user_surface, [0.002]]

    lens_back = Kos.surf()
    lens_back.Rc = -90.0
    lens_back.Glass = "AIR"
    lens_back.Thickness = 20.0
    lens_back.Diameter = 30.0

    image = Kos.surf()
    image.Glass = "AIR"
    image.Thickness = 0.0
    image.Diameter = 30.0

    return Kos.system([obj, shaped, lens_back, image], Kos.Setup(), build=0)


def build_small_aperture_lens_system():
    import KrakenOS as Kos

    obj = Kos.surf()
    obj.Glass = "AIR"
    obj.Thickness = 10.0
    obj.Diameter = 30.0

    lens_front = Kos.surf()
    lens_front.Rc = 80.0
    lens_front.Glass = "BK7"
    lens_front.Thickness = 5.0
    lens_front.Diameter = 4.0

    lens_back = Kos.surf()
    lens_back.Rc = -80.0
    lens_back.Glass = "AIR"
    lens_back.Thickness = 20.0
    lens_back.Diameter = 4.0

    image = Kos.surf()
    image.Glass = "AIR"
    image.Thickness = 0.0
    image.Diameter = 30.0

    return Kos.system([obj, lens_front, lens_back, image], Kos.Setup(), build=0)


def build_flat_mirror_system():
    import KrakenOS as Kos

    obj = Kos.surf()
    obj.Glass = "AIR"
    obj.Thickness = 10.0
    obj.Diameter = 30.0

    mirror = Kos.surf()
    mirror.Glass = "MIRROR"
    mirror.Thickness = -10.0
    mirror.Diameter = 30.0

    image = Kos.surf()
    image.Glass = "AIR"
    image.Thickness = 0.0
    image.Diameter = 30.0

    return Kos.system([obj, mirror, image], Kos.Setup(), build=0)


def scalar_trace_results(system, origins, directions, wavelength):
    hits = []
    output_directions = []
    active = []
    for origin, direction in zip(origins, directions):
        system.Trace(origin, direction, wavelength)
        valid = system.val == 1
        active.append(valid)
        hits.append(np.asarray(system.XYZ[-1], dtype=float))
        if valid:
            output_directions.append(np.asarray(system.R_LMN[-1], dtype=float))
        else:
            output_directions.append(np.zeros(3))
    return {
        "active": np.asarray(active, dtype=bool),
        "final_hits": np.asarray(hits, dtype=float),
        "final_directions": np.asarray(output_directions, dtype=float),
    }


def make_default_rays():
    origins = np.array(
        [
            [-4.0, -3.0, 0.0],
            [-2.0, 1.0, 0.0],
            [0.0, 0.0, 0.0],
            [1.5, -2.5, 0.0],
            [4.0, 3.0, 0.0],
        ],
        dtype=float,
    )
    l = np.array([0.0, 0.005, -0.005, 0.01, -0.01])
    m = np.array([0.0, -0.004, 0.006, -0.005, 0.005])
    n = np.sqrt(1.0 - (l * l) - (m * m))
    directions = np.column_stack([l, m, n])
    return origins, directions


def assert_bundle_matches_scalar(system, origins, directions, wavelength=0.55):
    bundle = trace_bundle(system, origins, directions, wavelength)
    scalar = scalar_trace_results(system, origins, directions, wavelength)
    active = scalar["active"]

    assert np.array_equal(bundle["active"], scalar["active"])
    assert np.allclose(
        bundle["final_hits"][active], scalar["final_hits"][active], rtol=1e-8, atol=1e-8
    )
    assert np.allclose(
        bundle["final_directions"][active],
        scalar["final_directions"][active],
        rtol=1e-8,
        atol=1e-8,
    )
    return bundle, scalar


def test_trace_bundle_matches_scalar_trace_for_simple_lens():
    system = build_simple_lens_system()
    origins, directions = make_default_rays()
    wavelength = 0.55

    bundle, _scalar = assert_bundle_matches_scalar(system, origins, directions, wavelength)

    assert np.all(bundle["active"])


def test_trace_bundle_matches_scalar_for_tilted_decentered_lens():
    system = build_tilted_decentered_lens_system()
    origins, directions = make_default_rays()

    bundle, _scalar = assert_bundle_matches_scalar(system, origins, directions)

    assert np.all(bundle["active"])


def test_trace_bundle_matches_scalar_for_asphere_zernike_lens_off_axis():
    system = build_asphere_zernike_lens_system()
    origins = np.array(
        [
            [-4.0, -3.0, 0.0],
            [-2.0, 1.0, 0.0],
            [0.8, 0.6, 0.0],
            [1.5, -2.5, 0.0],
            [4.0, 3.0, 0.0],
        ],
        dtype=float,
    )
    _default_origins, directions = make_default_rays()

    bundle, _scalar = assert_bundle_matches_scalar(system, origins, directions)

    assert np.all(bundle["active"])


def test_trace_bundle_matches_scalar_with_zernike_axis_fallback():
    system = build_zernike_axis_fallback_system()
    origins = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [-1.0, 0.5, 0.0],
        ],
        dtype=float,
    )
    directions = np.tile(np.array([0.0, 0.0, 1.0]), (len(origins), 1))

    bundle, _scalar = assert_bundle_matches_scalar(system, origins, directions)

    assert np.all(bundle["active"])


def test_trace_bundle_matches_scalar_with_axicon_apex_fallback():
    system = build_axicon_apex_fallback_system()
    origins = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [-1.0, 0.5, 0.0],
        ],
        dtype=float,
    )
    directions = np.tile(np.array([0.0, 0.0, 1.0]), (len(origins), 1))

    bundle, _scalar = assert_bundle_matches_scalar(system, origins, directions)

    assert np.all(bundle["active"])


def test_trace_bundle_matches_scalar_with_extra_data_fallback():
    system = build_extra_data_without_derivative_fallback_system()
    origins = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [-1.0, 0.5, 0.0],
        ],
        dtype=float,
    )
    directions = np.tile(np.array([0.0, 0.0, 1.0]), (len(origins), 1))

    bundle, _scalar = assert_bundle_matches_scalar(system, origins, directions)

    assert np.all(bundle["active"])


def test_trace_bundle_matches_scalar_active_mask_for_aperture_misses():
    system = build_small_aperture_lens_system()
    origins = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.5, 0.0, 0.0],
            [2.0, 0.0, 0.0],
            [3.0, 0.0, 0.0],
            [-3.0, 0.0, 0.0],
        ],
        dtype=float,
    )
    directions = np.tile(np.array([0.0, 0.0, 1.0]), (len(origins), 1))

    bundle, scalar = assert_bundle_matches_scalar(system, origins, directions)

    assert bundle["active"].tolist() == [True, True, True, False, False]
    assert np.array_equal(bundle["active"], scalar["active"])


def test_trace_bundle_matches_scalar_for_flat_mirror():
    system = build_flat_mirror_system()
    origins, directions = make_default_rays()

    bundle, _scalar = assert_bundle_matches_scalar(system, origins, directions)

    assert np.all(bundle["active"])
