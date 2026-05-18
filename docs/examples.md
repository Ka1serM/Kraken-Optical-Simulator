# KrakenOS Example Guide

Use this guide to find a starting example depending on what you want to do.
For the main learning path, see the
[KrakenOS Manual](manual/README.md). For the generated visual appendix, see
[KrakenOS Generated Examples Appendix](examples_manual.md). That appendix includes generated
2D and 3D images for selected examples. To refresh those images and rebuild the
manual, run `python tools/generate_example_images.py --all` from the repository
root.

| I want to... | Start with this example |
| --- | --- |
| Trace a single ray | [`Examp_Ray.py`](../KrakenOS/Examples/Examp_Ray.py) |
| Trace backward from image space | [`Examp_Reverse_Trace.py`](../KrakenOS/Examples/Examp_Reverse_Trace.py) |
| Build a simple doublet lens | [`Examp_Doublet_Lens.py`](../KrakenOS/Examples/Examp_Doublet_Lens.py) |
| Plot a lens in 2D or 3D | [`Examp_Doublet_Lens_3Dcolor.py`](../KrakenOS/Examples/Examp_Doublet_Lens_3Dcolor.py) |
| Save and reload a traced system | [`Examp_Pickle_Doublet_Lens_3Dcolor.py`](../KrakenOS/Examples/Examp_Pickle_Doublet_Lens_3Dcolor.py) |
| Use a pupil definition | [`Examp_Doublet_Lens_Pupil.py`](../KrakenOS/Examples/Examp_Doublet_Lens_Pupil.py) |
| Calculate Seidel aberrations | [`Examp_Doublet_Lens_Pupil_Seidel.py`](../KrakenOS/Examples/Examp_Doublet_Lens_Pupil_Seidel.py) |
| Calculate RMS spot radius and best focus | [`Examp_RMS_BestFocus.py`](../KrakenOS/Examples/Examp_RMS_BestFocus.py) |
| Use Zernike surfaces | [`Examp_Doublet_Lens_Zernike.py`](../KrakenOS/Examples/Examp_Doublet_Lens_Zernike.py) |
| Calculate PSF and MTF from Zernike terms | [`Examp_PSF_MTF_From_Zernike.py`](../KrakenOS/Examples/Examp_PSF_MTF_From_Zernike.py) |
| Work with cylindrical surfaces | [`Examp_Doublet_Lens_Cylinder.py`](../KrakenOS/Examples/Examp_Doublet_Lens_Cylinder.py) |
| Work with tilted surfaces | [`Examp_Doublet_Lens_Tilt.py`](../KrakenOS/Examples/Examp_Doublet_Lens_Tilt.py) |
| Work with tilted non-sequential surfaces | [`Examp_Doublet_Lens_Tilt_non_sec.py`](../KrakenOS/Examples/Examp_Doublet_Lens_Tilt_non_sec.py) |
| Work with axicons | [`Examp_Axicon.py`](../KrakenOS/Examples/Examp_Axicon.py) |
| Combine axicon and cylinder behavior | [`Examp_Axicon_And_Cylinder.py`](../KrakenOS/Examples/Examp_Axicon_And_Cylinder.py) |
| Use a user-defined surface | [`Examp_ExtraShape_XY_Cosines.py`](../KrakenOS/Examples/Examp_ExtraShape_XY_Cosines.py) |
| Use user-defined apertures or masks | [`Examp_ParaboleMirror_Shift_UDA.py`](../KrakenOS/Examples/Examp_ParaboleMirror_Shift_UDA.py) |
| Use faceted user-defined surfaces | [`Examp_ExtraShape_UserFacets.py`](../KrakenOS/Examples/Examp_ExtraShape_UserFacets.py) |
| Trace non-sequential rays | [`Examp_Doublet_Lens_NonSec.py`](../KrakenOS/Examples/Examp_Doublet_Lens_NonSec.py) |
| Add anti-reflection coatings | [`Examp_Doublet_Lens_NonSec-AR_Coating.py`](../KrakenOS/Examples/Examp_Doublet_Lens_NonSec-AR_Coating.py) |
| Inspect coating energy terms | [`Examp_Coating_Energy_Basics.py`](../KrakenOS/Examples/Examp_Coating_Energy_Basics.py) |
| Compare metal mirror energy terms | [`Examp_Metal_Mirror_Energy.py`](../KrakenOS/Examples/Examp_Metal_Mirror_Energy.py) |
| Use diffraction gratings | [`Examp_Diffraction_Grating_Reflection.py`](../KrakenOS/Examples/Examp_Diffraction_Grating_Reflection.py) |
| Use a transmission grating | [`Examp_Diffraction_Grating_Transmission.py`](../KrakenOS/Examples/Examp_Diffraction_Grating_Transmission.py) |
| Study dispersion with Abbe number | [`Examp_Dispersion_By_AbbeNumber.py`](../KrakenOS/Examples/Examp_Dispersion_By_AbbeNumber.py) |
| Inspect glass catalog priority | [`Examp_Glass_Catalog_Order.py`](../KrakenOS/Examples/Examp_Glass_Catalog_Order.py) |
| Load Zemax and catalog data | [`Examp_Spruce-tone_Github_User(Loading_Zemax_and_Catalogs).py`](../KrakenOS/Examples/Examp_Spruce-tone_Github_User%28Loading_Zemax_and_Catalogs%29.py) |
| Start with a lens catalog entry | [`Examp_Lens_Catalog_Basics.py`](../KrakenOS/Examples/Examp_Lens_Catalog_Basics.py) |
| Reuse catalog lenses as blocks | [`Examp_SurfBlock_Basics.py`](../KrakenOS/Examples/Examp_SurfBlock_Basics.py) |
| Enter refractive index data manually | [`Examp_Spruce-tone_Github_User (Manually enter the refractive index, dispersion and alpha).py`](../KrakenOS/Examples/Examp_Spruce-tone_Github_User%20%28Manually%20enter%20the%20refractive%20index%2C%20dispersion%20and%20alpha%29.py) |
| Use STL optical solids | [`Examp_Solid_Object_STL.py`](../KrakenOS/Examples/Examp_Solid_Object_STL.py) |
| Trace through a prism STL | [`Examp_Prism_STL.py`](../KrakenOS/Examples/Examp_Prism_STL.py) |
| Trace through a prism with coating data | [`Examp_Prism_STL-AR_coating.py`](../KrakenOS/Examples/Examp_Prism_STL-AR_coating.py) |
| Generate prism solid geometry | [`Examp_Refraction_Prism_solid_Generation.py`](../KrakenOS/Examples/Examp_Refraction_Prism_solid_Generation.py) |
| Use a source distribution function | [`Examp_Source_Distribution_Function.py`](../KrakenOS/Examples/Examp_Source_Distribution_Function.py) |
| Model atmospheric refraction correction | [`Examp_Tel_2M_Atmospheric_Refraction_Corrector_Static.py`](../KrakenOS/Examples/Examp_Tel_2M_Atmospheric_Refraction_Corrector_Static.py) |
| Model adaptable atmospheric correction | [`Examp_Tel_2M_Atmospheric_Refraction_Corrector_Adaptable.py`](../KrakenOS/Examples/Examp_Tel_2M_Atmospheric_Refraction_Corrector_Adaptable.py) |
| Fit wavefronts | [`Examp_Tel_2M_Wavefront_Fitting.py`](../KrakenOS/Examples/Examp_Tel_2M_Wavefront_Fitting.py) |
| Optimize with wavefront fitting | [`Examp_Tel_2M_Wavefront_Fitting_optimization.py`](../KrakenOS/Examples/Examp_Tel_2M_Wavefront_Fitting_optimization.py) |
| Optimize a doublet | [`Examp_Doublet_Optimization.py`](../KrakenOS/Examples/Examp_Doublet_Optimization.py) |
| Optimize telescope variables | [`Examp_Tel_2M_Optimization_Variables.py`](../KrakenOS/Examples/Examp_Tel_2M_Optimization_Variables.py) |
| Build a Czerny-Turner monochromator | [`Examp_CzernyTurner.py`](../KrakenOS/Examples/Examp_CzernyTurner.py) |
| Work with an echelle example | [`Examp_Tel_2M_Echelle.py`](../KrakenOS/Examples/Examp_Tel_2M_Echelle.py) |
| Work with an image slicer STL | [`Examp_Tel_2M-STL_ImageSlicer.py`](../KrakenOS/Examples/Examp_Tel_2M-STL_ImageSlicer.py) |
| Run a 2 m telescope example | [`Examp_Tel_2M.py`](../KrakenOS/Examples/Examp_Tel_2M.py) |
