# Pupils and Fields

`PupilCalc` generates ray origins and direction cosines from a stop surface,
aperture definition, sampling pattern, and field definition.

## Basic Pattern

```python
pupil = Kos.PupilCalc(system, Surf=1, W=0.55, AperType="EPD", AperVal=20.0)
pupil.Samp = 5
pupil.Ptype = "hexapolar"
pupil.FieldType = "angle"
pupil.FieldX = 0.0
pupil.FieldY = 0.0

x, y, z, l, m, n = pupil.Pattern2Field()
```

The returned arrays can be traced in a loop or with `Kos.TraceLoop`:

```python
rays = Kos.raykeeper(system)
Kos.TraceLoop(x, y, z, l, m, n, 0.55, rays, clean=1)
```

## Common Aperture and Pattern Ideas

Typical pupil workflows define:

- the stop surface index
- wavelength
- aperture type, such as entrance pupil diameter
- aperture value
- field type and field coordinates
- sampling pattern

Common patterns include fans, rectangular grids, and hexapolar sampling. Use
small sample counts while learning, then increase sampling for analysis.

## Atmospheric Refraction

KrakenOS includes atmospheric tools through the `AstroAtmosphere` package and
telescope examples. These workflows are advanced because they combine wavelength
selection, field definition, observatory parameters, and telescope geometry.

Recommended examples:

- [`Examp_Doublet_Lens_Pupil.py`](../../KrakenOS/Examples/Examp_Doublet_Lens_Pupil.py)
- [`Examp_Tel_2M_Pupila.py`](../../KrakenOS/Examples/Examp_Tel_2M_Pupila.py)
- [`Examp_Tel_2M_Atmospheric_Refraction_Corrector_Static.py`](../../KrakenOS/Examples/Examp_Tel_2M_Atmospheric_Refraction_Corrector_Static.py)
- [`Examp_Tel_2M_Atmospheric_Refraction_Corrector_Adaptable.py`](../../KrakenOS/Examples/Examp_Tel_2M_Atmospheric_Refraction_Corrector_Adaptable.py)

