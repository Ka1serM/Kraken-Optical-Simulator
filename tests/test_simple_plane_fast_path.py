import numpy as np


def build_flat_window_system(build=0):
    import KrakenOS as Kos

    obj = Kos.surf()
    obj.Glass = "AIR"
    obj.Thickness = 10
    obj.Diameter = 30

    window_front = Kos.surf()
    window_front.Glass = "BK7"
    window_front.Thickness = 5
    window_front.Diameter = 30

    window_back = Kos.surf()
    window_back.Glass = "AIR"
    window_back.Thickness = 20
    window_back.Diameter = 30

    image = Kos.surf()
    image.Glass = "AIR"
    image.Thickness = 0
    image.Diameter = 30

    return Kos.system([obj, window_front, window_back, image], Kos.Setup(), build=build)


def build_simple_lens_system(build=0):
    import KrakenOS as Kos

    obj = Kos.surf()
    obj.Glass = "AIR"
    obj.Thickness = 10
    obj.Diameter = 30

    lens_front = Kos.surf()
    lens_front.Rc = 80
    lens_front.Glass = "BK7"
    lens_front.Thickness = 5
    lens_front.Diameter = 30

    lens_back = Kos.surf()
    lens_back.Rc = -80
    lens_back.Glass = "AIR"
    lens_back.Thickness = 20
    lens_back.Diameter = 30

    image = Kos.surf()
    image.Glass = "AIR"
    image.Thickness = 0
    image.Diameter = 30

    return Kos.system([obj, lens_front, lens_back, image], Kos.Setup(), build=build)


def trace_sample(system):
    system.Trace([2.0, -1.5, 0.0], [0.0, 0.0, 1.0], 0.55)
    return {
        "val": system.val,
        "XYZ": np.asarray(system.XYZ, dtype=float),
        "OST_XYZ": np.asarray(system.OST_XYZ, dtype=float),
        "S_LMN": np.asarray(system.S_LMN, dtype=float),
        "R_LMN": np.asarray(system.R_LMN, dtype=float),
        "SURFACE": list(system.SURFACE),
        "TOP": float(system.TOP),
    }


def assert_trace_results_match(left, right):
    assert left["val"] == right["val"]
    assert left["SURFACE"] == right["SURFACE"]
    assert np.allclose(left["XYZ"], right["XYZ"], rtol=1e-10, atol=1e-10)
    assert np.allclose(left["OST_XYZ"], right["OST_XYZ"], rtol=1e-10, atol=1e-10)
    assert np.allclose(left["S_LMN"], right["S_LMN"], rtol=1e-10, atol=1e-10)
    assert np.allclose(left["R_LMN"], right["R_LMN"], rtol=1e-10, atol=1e-10)
    assert np.isclose(left["TOP"], right["TOP"], rtol=1e-10, atol=1e-10)


def test_simple_plane_trace_skips_newton_and_finite_difference_normal(monkeypatch):
    from KrakenOS.HitOnSurf import Hit_Solver

    def fail_if_called(*args, **kwargs):
        raise AssertionError("simple plane fast path should avoid numerical surface solving")

    monkeypatch.setattr(Hit_Solver, "_Hit_Solver__DerLineCurve", fail_if_called)
    monkeypatch.setattr(Hit_Solver, "SurfDer", fail_if_called)

    system = build_flat_window_system(build=0)
    result = trace_sample(system)

    assert result["val"] == 1
    assert result["SURFACE"] == [1, 2, 3]


def test_simple_plane_fast_path_matches_general_solver():
    fast_system = build_simple_lens_system(build=0)
    general_system = build_simple_lens_system(build=0)

    general_system.HS.IsSimplePlane = lambda j: False

    fast_result = trace_sample(fast_system)
    general_result = trace_sample(general_system)

    assert_trace_results_match(fast_result, general_result)
