# KrakenOS Capabilities

KrakenOS is a Python library for exact optical ray tracing and optical-system
analysis. The package has grown from a compact ray-tracing engine into a broader
toolbox for optical design, visualization, catalog handling, wavefront analysis,
and practical system examples.

This document is an overview of the main capabilities currently represented in
the codebase and examples. For a task-oriented list of scripts, see the
[KrakenOS Example Guide](examples.md). For a generated visual manual, see the
[KrakenOS Examples Manual](examples_manual.md). For future example priorities,
see the [Example Coverage Roadmap](example_coverage.md). For a short note on
PSF/MTF helper usage, see [PSF and MTF Notes](psf_mtf_notes.md).

## Core Ray Tracing

KrakenOS supports sequential and non-sequential ray tracing through optical
systems defined as ordered lists of `surf` objects.

Main features:

- sequential ray tracing with `system.Trace`
- non-sequential ray tracing with `system.NsTrace`
- reverse tracing with `system.RvTrace`
- fast tracing paths for repeated calculations
- access to intersection coordinates, direction cosines, optical paths,
  refractive indices, surface normals, diffraction orders, and energy terms
- storage and extraction of traced rays with `raykeeper`

Relevant examples:

- `Examp_Ray.py`
- `Examp_Doublet_Lens.py`
- `Examp_Doublet_Lens_NonSec.py`
- `Examp_Doublet_Lens_CommandsSystem.py`

## Optical Surfaces

The `surf` class can represent many optical interface types using geometric,
material, transformation, and surface-function attributes.

Supported surface concepts include:

- spherical and conic surfaces
- cylindrical surfaces
- axicons
- aspheric surfaces
- Zernike-defined surfaces
- user-defined mathematical surfaces
- shifted surface functions
- error-map surfaces
- masks, obstructions, and user-defined apertures
- thin-lens behavior
- diffraction gratings
- STL solid objects with optical properties
- coatings and metallic coatings

Relevant examples:

- `Examp_Axicon.py`
- `Examp_Axicon_And_Cylinder.py`
- `Examp_Doublet_Lens_Cylinder.py`
- `Examp_Doublet_Lens_Zernike.py`
- `Examp_ExtraShape_Micro_Lens_Array.py`
- `Examp_ExtraShape_Radial_Sine.py`
- `Examp_ExtraShape_UserFacets.py`
- `Examp_ExtraShape_XY_Cosines.py`
- `Examp_ParaboleMirror_Shift.py`
- `Examp_ParaboleMirror_Shift_UDA.py`

## Materials, Glass Catalogs, and Lens Catalogs

KrakenOS includes glass catalog loading and wavelength-dependent refractive
index calculations. The default catalog order is deterministic, with
`SCHOTT.AGF` loaded first by default.

Supported catalog-related features include:

- AGF glass catalog loading
- material lookup by glass name
- wavelength-dependent dispersion calculations
- metallic material data from CSV files
- Zemax-style lens catalog parsing through `LensCat.py`
- conversion from catalog/lens data to KrakenOS surfaces

Relevant examples:

- `Examp_Dispersion_By_AbbeNumber.py`
- `Examp_Glass_Catalog_Order.py`
- `Examp_Spruce-tone_Github_User(Loading_Zemax_and_Catalogs).py`
- `Examp_Spruce-tone_Github_User (Manually enter the refractive index, dispersion and alpha).py`

## Pupils, Fields, and Ray Generation

KrakenOS provides tools to generate ray patterns and connect them to field and
pupil definitions.

Supported concepts include:

- entrance pupil diameter definitions
- stop-based ray generation
- fan and grid sampling patterns
- field-angle ray generation
- ray bundles for spot diagrams and RMS calculations
- custom source distributions

Relevant examples:

- `Examp_Doublet_Lens_Pupil.py`
- `Examp_Doublet_Lens_Pupil_Seidel.py`
- `Examp_Source_Distribution_Function.py`
- `Examp_Tel_2M_Pupila.py`
- `Examp_Tel_2M_Spyder_Spot_Diagram.py`
- `Examp_Tel_2M_Spyder_Spot_RMS.py`

## Aberrations, Wavefronts, PSF, and MTF

KrakenOS includes tools for geometrical and wavefront-based optical analysis.

Supported analyses include:

- paraxial calculations
- Seidel aberration calculations
- Zernike polynomial fitting
- wavefront phase reconstruction
- best-focus estimation
- PSF calculation
- MTF calculation
- PSF maps over field points
- spherical-reference PSF calculations

Relevant examples:

- `Examp_Doublet_Lens-ParaxMatrix.py`
- `Examp_Doublet_Lens_Pupil_Seidel.py`
- `Examp_Doublet_Lens_Zernike.py`
- `Examp_Tel_2M_Wavefront_Fitting.py`
- `Examp_Tel_2M_Wavefront_Fitting_optimization.py`

## Visualization

KrakenOS includes 2D and 3D visualization tools for optical systems and traced
rays.

Supported visualization paths include:

- 2D system layout plots
- 3D system visualization
- colored ray plotting
- surface and solid rendering
- ray extraction for custom plots

Relevant examples:

- `Examp_Doublet_Lens_3Dcolor.py`
- `Examp_Pickle_Doublet_Lens_3Dcolor.py`
- `Examp_Tel_2M.py`

## CAD, STL, and Solid Objects

KrakenOS can assign optical behavior to STL solid objects and use them in ray
tracing.

Supported CAD/STL concepts include:

- STL solid loading
- solid-object ray interactions
- prism and polygon-based optical solids
- image-slicer geometry examples

Relevant examples:

- `Examp_Prism_STL.py`
- `Examp_Prism_STL-AR_coating.py`
- `Examp_Refraction_Prism.py`
- `Examp_Refraction_Prism_solid.py`
- `Examp_Refraction_Prism_solid_Generation.py`
- `Examp_Solid_Object_STL.py`
- `Examp_Solid_Object_STL_ARRAY.py`
- `Examp_Tel_2M-STL_ImageSlicer.py`

## Diffraction, Coatings, and Energy

KrakenOS includes ray interactions beyond simple refraction.

Supported features include:

- diffraction gratings
- reflection and refraction
- Fresnel energy coefficients
- P and S polarization energy terms
- dielectric and metal behavior
- coating lookup and interpolation

Relevant examples:

- `Examp_Diffraction_Grating_Reflection.py`
- `Examp_Diffraction_Grating_Reflection_Single.py`
- `Examp_Diffraction_Grating_Transmission.py`
- `Examp_Doublet_Lens_NonSec-AR_Coating.py`
- `Examp_Doublet_Lens_Tilt_non_sec-AR-Coating.py`
- `Examp_Fresnel.py`
- `Examp_Flat_NonSec_AR-caoating.py`

## Atmospheric and Astronomical Optics

The `AstroAtmosphere` package provides atmospheric refraction and dispersion
models useful for astronomical optical systems.

Supported concepts include:

- refractivity models
- atmospheric refraction
- atmospheric dispersion
- observatory/location parameters
- atmospheric dispersion corrector examples

Relevant examples:

- `Examp_Tel_2M_Atmospheric_Refraction_Corrector_Adaptable.py`
- `Examp_Tel_2M_Atmospheric_Refraction_Corrector_Static.py`

## Optimization and Design Workflows

Several examples demonstrate optimization-oriented workflows using KrakenOS as
the optical engine.

Supported workflows include:

- best-focus search
- merit-function style calculations
- external optimization loops
- variable updates on optical systems
- telescope and doublet design studies

Relevant examples:

- `Examp_Doublet_Optimization.py`
- `Examp_Tel_2M_Optimization_Variables.py`
- `Examp_Tel_2M_Wavefront_Fitting_optimization.py`

## Spectrographs and Instrument Examples

The example set includes several instrument-level optical systems.

Represented examples include:

- Czerny-Turner monochromator
- echelle spectrograph behavior
- semi-Littrow style spectrograph workflows
- telescope examples
- image slicer geometry

Relevant examples:

- `Examp_CzernyTurner.py`
- `Examp_Tel_2M_Echelle.py`
- `Examp_Tel_2M.py`
- `Examp_Tel_2M-STL_ImageSlicer.py`

## Documentation Roadmap

Useful future documentation additions:

- a feature-to-example table
- a concise API overview for `surf`, `system`, `raykeeper`, `Setup`, and
  `PupilCalc`
- a glass catalog management guide
- a packaging and installation guide for contributors
- short tutorials that reproduce selected examples step by step
- more generated figures for STL/solid geometry, diffraction, atmospheric
  optics, optimization, and telescope-level workflows
