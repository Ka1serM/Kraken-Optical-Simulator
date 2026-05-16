# PSF and MTF Notes

KrakenOS includes PSF and MTF helpers in `PSFCalc.py`. The shortest starting
point is `KrakenOS/Examples/Examp_PSF_MTF_From_Zernike.py`.

## Inputs

The compact PSF/MTF helpers use:

- `COEF`: Zernike coefficients in waves.
- `Focal`: focal length in millimeters.
- `Diameter`: pupil diameter in millimeters.
- `Wave`: wavelength in micrometers.
- `pixels`: sampled image size for `Kos.psf`.
- `PupilSample`: pupil sampling scale.

## Practical Notes

- `Kos.psf(...)` can be used without plotting by passing `plot=0`.
- `Kos.calculate_mtf(...)` returns a normalized 2D MTF array.
- A zero-spatial-frequency MTF sample should be near 1 after normalization.
- A small nonzero Zernike coefficient vector is useful for tutorial examples
  because it avoids the degenerate all-zero wavefront case.
- The current `calculate_mtf` helper internally uses its default PSF sampling.
  Treat it as a quick analysis helper rather than a fully parameterized plotting
  pipeline.

## Suggested Example Order

1. Start with `Examp_PSF_MTF_From_Zernike.py`.
2. Move to `Examp_Tel_2M_Wavefront_Fitting.py` for PSF from traced wavefronts.
3. Use `Examp_Tel_2M_Wavefront_Fitting_optimization.py` when optimization and
   wavefront analysis need to be connected.
