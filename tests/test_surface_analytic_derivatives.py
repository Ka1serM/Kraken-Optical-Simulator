import numpy as np


def finite_difference_derivative(surface, x, y, step=1e-6):
    dzdx = (
        surface.sigma_z(x + step, y, 0) - surface.sigma_z(x - step, y, 0)
    ) / (2.0 * step)
    dzdy = (
        surface.sigma_z(x, y + step, 0) - surface.sigma_z(x, y - step, 0)
    ) / (2.0 * step)
    return dzdx, dzdy


def assert_derivative_matches_finite_difference(surface, x=1.7, y=2.3):
    analytical = surface.sigma_derivative(x, y, 0)
    assert analytical is not None
    finite = finite_difference_derivative(surface, x, y)
    assert np.allclose(analytical[0], finite[0], rtol=1e-4, atol=1e-6)
    assert np.allclose(analytical[1], finite[1], rtol=1e-4, atol=1e-6)


def test_conic_aspheric_zernike_derivatives_match_finite_difference():
    import KrakenOS as Kos

    conic = Kos.surf()
    conic.Rc = 80.0
    conic.k = -0.2
    conic.Cylinder_Rxy_Ratio = 0.85
    conic.build_surface_function()
    assert_derivative_matches_finite_difference(conic)

    asphere = Kos.surf()
    asphere.AspherData = np.zeros(200)
    asphere.AspherData[0] = 1e-5
    asphere.AspherData[1] = -1e-8
    asphere.build_surface_function()
    assert_derivative_matches_finite_difference(asphere)

    zernike = Kos.surf()
    zernike.Diameter = 30.0
    zernike.ZNK = np.zeros(36)
    zernike.ZNK[1] = 0.010
    zernike.ZNK[4] = -0.004
    zernike.ZNK[8] = 0.002
    zernike.build_surface_function()
    assert_derivative_matches_finite_difference(zernike)


def test_summed_surface_derivative_matches_summed_sag_finite_difference():
    import KrakenOS as Kos

    surface = Kos.surf()
    surface.Rc = 120.0
    surface.k = -0.4
    surface.AspherData = np.zeros(200)
    surface.AspherData[0] = 3e-6
    surface.AspherData[2] = -2e-11
    surface.ZNK = np.zeros(36)
    surface.ZNK[2] = 0.007
    surface.ZNK[5] = -0.003
    surface.Diameter = 30.0
    surface.build_surface_function()

    assert_derivative_matches_finite_difference(surface, x=2.4, y=-1.9)


def test_analytic_derivatives_accept_vector_inputs():
    import KrakenOS as Kos

    x = np.array([1.0, 5.0, 10.0, 20.0])
    y = np.array([2.0, -3.0, 12.0, -7.0])

    parabola = Kos.surf()
    parabola.Rc = -2000.0
    parabola.k = -1.0
    parabola.Diameter = 300.0
    parabola.build_surface_function()

    asphere = Kos.surf()
    asphere.Rc = 100.0
    asphere.AspherData = np.zeros(200)
    asphere.AspherData[0] = 1e-8
    asphere.AspherData[1] = -1e-12
    asphere.Diameter = 100.0
    asphere.build_surface_function()

    zernike = Kos.surf()
    zernike.Diameter = 100.0
    zernike.ZNK = np.zeros(36)
    zernike.ZNK[3] = 0.01
    zernike.ZNK[4] = -0.02
    zernike.build_surface_function()

    axicon = Kos.surf()
    axicon.Axicon = 2.0
    axicon.Diameter = 100.0
    axicon.build_surface_function()

    for surface in [parabola, asphere, zernike, axicon]:
        dzdx, dzdy = surface.sigma_derivative(x, y, 0)
        assert np.shape(dzdx) == np.shape(x)
        assert np.shape(dzdy) == np.shape(y)
        assert np.all(np.isfinite(dzdx))
        assert np.all(np.isfinite(dzdy))


def test_vector_analytic_derivatives_match_vector_finite_difference():
    import KrakenOS as Kos

    surface = Kos.surf()
    surface.Rc = 120.0
    surface.k = -0.35
    surface.AspherData = np.zeros(200)
    surface.AspherData[0] = 3e-8
    surface.AspherData[2] = -2e-14
    surface.ZNK = np.zeros(36)
    surface.ZNK[2] = 0.007
    surface.ZNK[5] = -0.003
    surface.Diameter = 80.0
    surface.build_surface_function()

    x = np.array([1.0, 5.0, 10.0, 20.0])
    y = np.array([2.0, -3.0, 12.0, -7.0])

    analytical = surface.sigma_derivative(x, y, 0)
    finite = finite_difference_derivative(surface, x, y)

    assert np.allclose(analytical[0], finite[0], rtol=1e-4, atol=1e-6)
    assert np.allclose(analytical[1], finite[1], rtol=1e-4, atol=1e-6)


def test_extra_data_derivative_is_optional_and_backwards_compatible():
    import KrakenOS as Kos

    coef = [0.25]

    def user_surface(x, y, data):
        return data[0] * x * y

    surface_without_derivative = Kos.surf()
    surface_without_derivative.ExtraData = [user_surface, coef]
    surface_without_derivative.build_surface_function()
    assert surface_without_derivative.sigma_derivative(1.2, 2.0, 0) is None

    def user_derivative(x, y, data):
        return data[0] * y, data[0] * x

    surface_with_derivative = Kos.surf()
    surface_with_derivative.ExtraData = [user_surface, coef, user_derivative]
    surface_with_derivative.build_surface_function()

    dzdx, dzdy = surface_with_derivative.sigma_derivative(1.2, 2.0, 0)
    assert np.isclose(dzdx, 0.5)
    assert np.isclose(dzdy, 0.3)


def build_mixed_surface_system(disable_analytic=False):
    import KrakenOS as Kos

    obj = Kos.surf()
    obj.Glass = "AIR"
    obj.Thickness = 10
    obj.Diameter = 30

    mixed = Kos.surf()
    mixed.Rc = 80
    mixed.Glass = "BK7"
    mixed.Thickness = 20
    mixed.Diameter = 30
    mixed.AspherData = np.zeros(200)
    mixed.AspherData[0] = 1e-6
    mixed.ZNK = np.zeros(36)
    mixed.ZNK[2] = 0.003

    image = Kos.surf()
    image.Glass = "AIR"
    image.Thickness = 0
    image.Diameter = 30

    system = Kos.system([obj, mixed, image], Kos.Setup(), build=0)
    if disable_analytic:
        for surface in system.SDT:
            surface.sigma_derivative = lambda x, y, case: None
    return system


def trace_sample(system):
    system.Trace([2.0, -1.5, 0.0], [0.0, 0.0, 1.0], 0.55)
    return {
        "val": system.val,
        "XYZ": np.asarray(system.XYZ, dtype=float),
        "S_LMN": np.asarray(system.S_LMN, dtype=float),
        "R_LMN": np.asarray(system.R_LMN, dtype=float),
        "TOP": float(system.TOP),
    }


def test_trace_with_analytic_derivatives_matches_finite_difference_path():
    analytical = trace_sample(build_mixed_surface_system(disable_analytic=False))
    numerical = trace_sample(build_mixed_surface_system(disable_analytic=True))

    assert analytical["val"] == numerical["val"]
    assert np.allclose(analytical["XYZ"], numerical["XYZ"], rtol=1e-8, atol=1e-8)
    assert np.allclose(analytical["S_LMN"], numerical["S_LMN"], rtol=1e-8, atol=1e-8)
    assert np.allclose(analytical["R_LMN"], numerical["R_LMN"], rtol=1e-8, atol=1e-8)
    assert np.isclose(analytical["TOP"], numerical["TOP"], rtol=1e-8, atol=1e-8)
