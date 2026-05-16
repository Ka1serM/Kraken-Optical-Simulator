# KrakenOS Example Coverage Roadmap

This roadmap compares the current KrakenOS capabilities with the example set.
It is meant to guide future example work without changing the historical
example filenames.

## Well Covered

These areas already have useful examples and mostly need small maintenance over
time:

| Area | Current coverage |
| --- | --- |
| Basic sequential ray tracing | `Examp_Ray.py`, `Examp_Doublet_Lens.py` |
| Pupil-based ray generation | `Examp_Doublet_Lens_Pupil.py`, `Examp_Tel_2M_Pupila.py` |
| 2D and 3D visualization | `Examp_Doublet_Lens_3Dcolor.py`, `Examp_Tel_2M.py` |
| Tilted and decentered components | `Examp_Doublet_Lens_Tilt.py`, `Examp_Doublet_Lens_Tilt_non_sec.py` |
| Axicons, cylinders, Zernike surfaces, and custom shapes | `Examp_Axicon.py`, `Examp_Doublet_Lens_Cylinder.py`, `Examp_Doublet_Lens_Zernike.py`, `Examp_ExtraShape_*` |
| Diffraction gratings and spectrograph layouts | `Examp_Diffraction_Grating_*`, `Examp_CzernyTurner.py`, `Examp_Tel_2M_Echelle.py` |
| STL and solid-object tracing | `Examp_Prism_STL.py`, `Examp_Solid_Object_STL.py`, `Examp_Tel_2M-STL_ImageSlicer.py` |
| Telescope-level workflows | `Examp_Tel_2M*.py` |
| Atmospheric refraction correction | `Examp_Tel_2M_Atmospheric_Refraction_Corrector_*.py` |

## Partly Covered

These features exist and have examples, but the examples are either advanced,
large, or not ideal as first-contact tutorials:

| Area | Current state | Suggested improvement |
| --- | --- | --- |
| Coating tables and energy behavior | `Examp_Coating_Energy_Basics.py` now shows a small coating-only tutorial with reflected and transmitted energy terms. | Larger non-sequential coating examples remain useful for advanced workflows. |
| Metal coatings and polarization terms | `Examp_Metal_Mirror_Energy.py` compares aluminum and gold mirror energy terms. | Keep `Examp_Sphere.py` as a geometry-oriented metal mirror example. |
| PSF and MTF | `Examp_PSF_MTF_From_Zernike.py` now shows direct PSF and MTF calculation from Zernike coefficients. | Add a deeper note later about PSF/MTF sampling and units. |
| RMS and best-focus tools | `Examp_RMS_BestFocus.py` now shows `Kos.RMS` and RMS minimization in a compact example. | Consider adding a deeper API note if `Kos.BestFocus` is revised in the future. |
| Zemax lens catalog conversion | `Examp_Lens_Catalog_Basics.py` now shows a short packaged ZMF entry conversion. | The larger Spruce-tone example remains useful for advanced catalog workflows. |
| Reverse tracing | `Examp_Reverse_Trace.py` now shows a minimal image-to-object reverse trace. | Add a more advanced off-axis reverse-trace example only if needed. |
| Fast tracing | `FastTrace` exists in the system class, but is not presented as a workflow. | Add a performance-oriented example only after confirming the intended public API. |
| `SurfBlock` reusable assemblies | `Examp_SurfBlock_Basics.py` now shows catalog entries used as reusable blocks. | Larger relay examples can build on this pattern. |

## Recently Added First-Contact Examples

These focused examples were added to make important capabilities easier to learn
without starting from the larger instrument-level scripts:

1. `Examp_RMS_BestFocus.py`

   Purpose: show how to trace a compact ray bundle, extract image-plane rays,
   calculate RMS, move to best focus, and report before/after RMS.

2. `Examp_PSF_MTF_From_Zernike.py`

   Purpose: show how to use a simple Zernike coefficient vector with the PSF
   and MTF helpers, independent of a large telescope model.

3. `Examp_Coating_Energy_Basics.py`

   Purpose: show the coating table format, trace one or a few rays, and inspect
   the resulting reflected/transmitted energy terms.

4. `Examp_Lens_Catalog_Basics.py`

   Purpose: load a packaged Zemax-style catalog file, list a few available lens
   entries, convert one entry to KrakenOS surfaces, and display the result.

5. `Examp_Reverse_Trace.py`

   Purpose: demonstrate `RvTrace` in a tiny system so users understand when
   reverse tracing is useful.

6. `Examp_SurfBlock_Basics.py`

   Purpose: show how catalog-derived lenses can be wrapped as reusable
   `SurfBlock` assemblies and aligned with explicit distances.

7. `Examp_Metal_Mirror_Energy.py`

   Purpose: compare default aluminum and loaded gold mirror energy terms so
   users can inspect `RP`, `RS`, `TP`, `TS`, and `TT`.

8. `docs/psf_mtf_notes.md`

   Purpose: document the practical inputs and current sampling behavior of the
   PSF/MTF helper functions.

## Generated Visual Manual

The generated examples manual now includes reproducible images for selected
first-contact examples. These images are created by
`tools/generate_example_images.py` and inserted by
`tools/generate_examples_manual.py`.

Currently illustrated areas include:

- basic ray tracing
- glass catalog priority
- coating and metal energy terms
- ideal lenses and an ideal telescope
- lens catalog conversion and `SurfBlock` assemblies
- chromatic dispersion
- prism refraction
- folded mirror geometry
- PSF/MTF from Zernike terms
- pupil tracing in 2D and 3D
- reverse tracing
- RMS best-focus analysis

## Documentation Improvements Before Adding Many Examples

- Keep current historical example filenames stable for compatibility.
- Add aliases or new clean filenames only when the old names are confusing
  enough to hurt new users.
- Prefer short examples that teach one idea at a time.
- Put large instrument examples after basic examples in guides.
- Mark deliberately commented blocks with `Optional didactic ...` comments.
- Avoid requiring heavy data files for beginner examples.

## Suggested Next Batch

The next practical batch should investigate or design:

1. Add generated figures for STL/solid-object examples.
2. Add generated figures for diffraction grating examples.
3. Add generated figures for atmospheric refraction and telescope-level examples.
4. Review whether `FastTrace` should have a public beginner example.
5. Add a glass catalog manager API or GUI in a future version.
6. Add deeper off-axis reverse-trace and metal-coating tutorials only if users ask for them.

Then update:

- `docs/examples.md`
- `KrakenOS/Examples/README.md`
- `KrakenOS/Examples/EXAMPLES_INDEX.md`
- `tests/test_smoke.py` if the new examples add resources or important import
  assumptions
