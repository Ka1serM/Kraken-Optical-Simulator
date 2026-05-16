# KrakenOS Examples

This folder contains small, runnable KrakenOS examples.  They start with simple
ray-tracing cases and gradually move into pupils, gratings, non-sequential
tracing, STL geometry, telescope models, and wavefront analysis.

The examples are intentionally written as scripts rather than as polished API
recipes.  That makes them useful for learning by editing: change one radius,
wavelength, aperture, tilt, or grating order and run the file again.

For a generated manual with topic summaries and selected 2D/3D figures, see
`../../docs/examples_manual.md`.

## How to use these examples

Run an example from this directory, or from a project directory where KrakenOS is
available on the Python path.  Most scripts add the parent repository to
`sys.path`, so they are easiest to run from a clone of the KrakenOS repository.

```bash
python Examples/Examp_Ray.py
```

A few advanced examples need local data files such as STL geometry, sampled
surface profiles, saved rays, or spectral-line tables.  Those files are included
in this folder when they are required by the original scripts.

To regenerate the visual manual assets from the repository root:

```bash
python tools/generate_example_images.py --all
```

## Reading order

For a first pass, use this order:

1. `Examp_Ray.py` - a minimal ray-tracing example.
2. `Examp_Sphere.py` and `Examp_Flat_Mirror_45Deg.py` - basic surfaces and mirrors.
3. `Examp_Doublet_Lens.py` - a full sequential lens example with best-focus logic.
4. `Examp_Doublet_Lens_Pupil.py` - pupil calculation and ray sampling.
5. `Examp_RMS_BestFocus.py` - RMS spot radius and best-focus adjustment.
6. `Examp_PSF_MTF_From_Zernike.py` - PSF and MTF from Zernike coefficients.
7. `Examp_Coating_Energy_Basics.py` - basic coating table and energy terms.
8. `Examp_Lens_Catalog_Basics.py` - a short lens catalog conversion example.
9. `Examp_Reverse_Trace.py` - reverse tracing from image space.
10. `Examp_SurfBlock_Basics.py` - reusable catalog lens assemblies.
11. `Examp_Metal_Mirror_Energy.py` - metal mirror energy terms.
12. `Examp_Diffraction_Grating_Transmission.py` and `Examp_CzernyTurner.py` - dispersive systems.
13. `Examp_Prism_STL.py` and `Examp_Solid_Object_STL.py` - non-sequential STL geometry.
14. `Examp_Tel_2M.py` and the other `Examp_Tel_2M_*` files - telescope-level examples.

## Naming note

The original file names were kept so existing references do not break.  Some of
those names still reflect historical development names.  The module docstring at
the top of each file should be treated as the current description.
