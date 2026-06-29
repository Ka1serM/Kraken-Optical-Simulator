import numpy as np


def build_lens_system(Kos):
    obj = Kos.surf()
    obj.Glass = "AIR"
    obj.Thickness = 10
    obj.Diameter = 30

    lens_front = Kos.surf()
    lens_front.Rc = 80
    lens_front.Glass = "BK7"
    lens_front.Thickness = 5
    lens_front.Diameter = 30
    lens_front.STOP = True

    lens_back = Kos.surf()
    lens_back.Rc = -80
    lens_back.Glass = "AIR"
    lens_back.Thickness = 20
    lens_back.Diameter = 30

    image = Kos.surf()
    image.Glass = "AIR"
    image.Thickness = 0
    image.Diameter = 30

    return Kos.system([obj, lens_front, lens_back, image], Kos.Setup(), build=0)


def test_phase_can_return_reference_sphere_image_position():
    import KrakenOS as Kos

    system = build_lens_system(Kos)
    pupil = Kos.PupilCalc(system, 1, 0.587)
    pupil.Samp = 3
    pupil.FieldType = "angle"
    pupil.FieldX = 2
    pupil.FieldY = 1

    result = Kos.Phase(pupil, return_reference_position=True)

    assert len(result) == 5
    reference_position = result[4]
    assert reference_position.shape == (3,)
    assert np.all(np.isfinite(reference_position))
    np.testing.assert_allclose(reference_position, system.XYZ[-1])


def test_phase_preserves_the_existing_return_shape_by_default():
    import KrakenOS as Kos

    system = build_lens_system(Kos)
    pupil = Kos.PupilCalc(system, 1, 0.587)
    pupil.Samp = 3
    pupil.FieldType = "angle"

    assert len(Kos.Phase(pupil)) == 4
