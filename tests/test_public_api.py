"""Public API contract for the traditional ``import KrakenOS as Kos`` style."""


PUBLIC_API_NAMES = [
    "BestFocus",
    "NsTraceLoop",
    "Phase",
    "Phase2",
    "PupilCalc",
    "RMS",
    "R_RMS_delta",
    "Seidel",
    "Setup",
    "SourceRnd",
    "SurfBlock",
    "TraceLoop",
    "WavefrontData2Image",
    "ZernikeDataImage2Plot",
    "Zernike_Fitting",
    "alignment",
    "calculate_mtf",
    "cat2surf",
    "display2d",
    "display2d_colab",
    "display2d_interactive",
    "display3d",
    "display3d_OB",
    "display3d_colab",
    "display3d_interactive",
    "display3d_old",
    "n_wave_dispersion",
    "plot_mtf",
    "psf",
    "raykeeper",
    "surf",
    "surflist2dict",
    "system",
    "zmf2dict",
    "zmx_read",
]


def test_public_api_names_used_by_examples_are_available():
    import KrakenOS as Kos

    missing = [name for name in PUBLIC_API_NAMES if not hasattr(Kos, name)]
    assert missing == []


def test_core_api_objects_can_be_created():
    import KrakenOS as Kos

    surface = Kos.surf()
    setup = Kos.Setup()
    system = Kos.system([surface], setup, build=0)
    rays = Kos.raykeeper(system)

    assert surface is not None
    assert setup is not None
    assert system is not None
    assert rays is not None
