
# Kraken-Optical-Simulator (KrakenOS)         
![GitHub Logo](/images/00.png)


[Joel Herrera V. - UNAM](https://www.astroscu.unam.mx/IA/index.php?option=com_content&view=article&id=790Itemid=86&lang=es)    

Email: joel@astro.unam.mx

#### Collaborators:
Carlos Guerrero P., Morgan Rhaí Najera Roa, Anais Sotelo B., Ilse Plauchu F., José A. Araiza

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5501376.svg)](https://doi.org/10.5281/zenodo.5501376)


## 

It would be appreciated if a reference to the following work, for which this package was originally built, is included whenever this code is used for a publication: (https://www.spiedigitallibrary.org/journals/optical-engineering/volume-61/issue-1/015101/KrakenOS-Python-based-general-exact-ray-tracing-library/10.1117/1.OE.61.1.015101.short)

And the book "Optical Simulation Using Python and KrakenOS":
(https://spie.org/Publications/Book/2672426#_=_)



KrakenOS (Kraken - Optical Simulator) is a python library based in Numpy, Matplotlib, PyVTK and PyVista libraries, it provides a three-dimensional optical systems visualization and ray tracing. This tool has been programmed on the object-oriented paradigm. KrakenOS focuses on performing sequential and non-sequential exact ray tracing, it permits to define all the parameters of the optical elements or even the mathematical function to describe their shape, it also allows adding optical properties to 3D solid elements in STL format and use glass catalogs. The library permits controlling and modifying the position of the surfaces in a three-dimensional space, this allows generating off-axis systems. It also has several tools such as the calculation of wavefront aberrations in terms of Zernike polynomials, Seidel sums, Entrance and exit pupil calculation and paraxial optics.

## Install KrakenOS

For regular use, install KrakenOS with pip:

```bash
python -m pip install KrakenOS
```

This installs KrakenOS and its Python dependencies, including NumPy, SciPy,
Matplotlib, PyVista, VTK, PyVTK, csv342, and pandas.

For development from a cloned repository, run this command from the repository
root, where `pyproject.toml` is located:

```bash
python -m pip install -e .
```

To verify the installation:

```python
import KrakenOS as Kos

print(Kos.__file__)
print(Kos.surf())
```

For a broader map of the library, see
[KrakenOS Capabilities](docs/capabilities.md).

### A little fun before class ... and objects

```python
"""Examp Doublet Lens Pupil"""

# Loading the library
import KrakenOS as Kos
```

```python
# Creating an object of the surf class for the object plane
P_Obj = Kos.surf()
P_Obj.Thickness = 100
P_Obj.Glass = "AIR"
P_Obj.Diameter = 30.0

# Creating a surface for the first face in BK7 Glass
L1a = Kos.surf()
L1a.Rc = 92.847
L1a.Thickness = 6.0
L1a.Glass = "BK7"
L1a.Diameter = 30.0

# Creating a surface for the second face in F2 Glass
L1b = Kos.surf()
L1b.Rc = -30.716
L1b.Thickness = 3.0
L1b.Glass = "F2"
L1b.Diameter = 30

# Creating a surface for the third interface to air
L1c = Kos.surf()
L1c.Rc = -78.197
L1c.Thickness = 97.376 - 40
L1c.Glass = "AIR"
L1c.Diameter = 30

# Creating a surface to exemplify a pupil
pupila = Kos.surf()
pupila.Rc = 30
pupila.Thickness = 40.
pupila.Glass = "AIR"
pupila.Diameter = 5
pupila.Name = "Pupil"
pupila.DespY = 0.
pupila.Nm_Pos=(-10,10)

# Creating a surface for image plane
P_Ima = Kos.surf()
P_Ima.Rc = 0.0
P_Ima.Thickness = 0.0
P_Ima.Glass = "AIR"
P_Ima.Diameter = 20.0
P_Ima.Name = "P_Ima"
P_Ima.Nm_Pos=(-10,10)
```

Creating a list with all the surfaces and loading the default glass catalogs (See user manual)
```python
A = [P_Obj, L1a, L1b, L1c, pupila, P_Ima]
config_1 = Kos.Setup()
```

```python
# Creating the system with previous information
Doublet = Kos.system(A, config_1)
```

Creating a ray container
```python
Rays = Kos.raykeeper(Doublet)
```

Defining parameters to configure pupil on surface 4 (Again.., see user manual)
```python
W = 0.4
sur = 4
AperVal = 10
AperType = "EPD"
Pup = Kos.PupilCalc(Doublet, sur, W, AperType, AperVal)

# Configuring field and ray array type
Pup.Samp = 3
Pup.Ptype = "fan"
Pup.FieldType = "angle"
Pup.FieldY = 2.0
```

Generating and tracing rays 
```python

# ray origin coordinates and direction cosines
x, y, z, L, M, N = Pup.Pattern2Field()

# Tracing the rays with a loop
for i in range(0, len(x)):
    pSource_0 = [x[i], y[i], z[i]]
    dCos = [L[i], M[i], N[i]]
    Doublet.Trace(pSource_0, dCos, W)
    Rays.push()# Saving rays

# Configuring (-field) and ray array type,.. etc
Pup.FieldY = -Pup.FieldY
x, y, z, L, M, N = Pup.Pattern2Field()
for i in range(0, len(x)):
    pSource_0 = [x[i], y[i], z[i]]
    dCos = [L[i], M[i], N[i]]
    Doublet.Trace(pSource_0, dCos, W)
    Rays.push() # Saving rays
```

3D plotting
```python
Kos.display3d(Doublet, Rays,2)
```

![GitHub Logo](/images/01.png)




Or for 2D plotting
```python
Kos.display2d(Doublet, Rays,0,1)
```

![GitHub Logo](/images/03.png)



## surf class Attributes
| class Attribute                       | Short description                                                                                                 |
| -------------------------------------| ----------------------------------------------------------------------------------------------------------------- |
| surf.Name = ""                       | Name of the element.                                                                                              |
| surf.Nm_Pos = (0,0)                 | "Name" position in the 2D diagram.                                                                                |
| surf.Note = "None"                   | Useful for adding user notes to a surface.                                                                        |
| surf.Rc = 0                          | Paraxial radius of curvature in millimeters.                                                                      |
| surf.Cylinder\_Rxy\_Ratio = 1        | Ratio between the axial and sagittal radius of curvature.                                                         |
| surf.Axicon = 0                      | Values other than zero an axicon is generated with the angle defined                                              |
| surf.Thickness = 0.0                 | Distance between this surface and the next surface.                                                               |
| surf.Diameter = 1.0                  | Outside diameter of the surface.                                                                                  |
| surf.InDiameter = 0.0                | Internal diameter of the surface.                                                                                 |
| surf.Glass = "AIR"                   | String for the glass name. If a float is used instead, that float is the refractive index.                        |
| surf.k = 0.0                         | Conicity constant for classical conic surfaces, k = 0 for spherical, k = -1 for parabola, etc. Default value: 0.0 |
|                                                                                                                                                          |
| surf.DespX = 0.0                     | Displacement of the surface in the X, Y and Z axis                                                                |
| surf.DespY = 0.0                     |                                                                                                                   |
| surf.DespZ = 0.0                     |                                                                                                                   |
|                                                                                                                                                          |
| surf.TiltX = 0.0                     | Rotation of the surface in the X, Y and Z axis                                                                    |                                       
| surf.TiltY = 0.0                     |                                                                                                                   |
| surf.TiltZ = 0.0                     |                                                                                                                   |
|                                                                                                                                                          |
| surf.Order = 0                       | Define the order of the transformations.                                                                          |
| surf.AxisMove = 1                    | Defines what will happen to the optical axis after a coordinate transformation.                                   |
| surf.Diff\_Ord = 0.0                 | Diffraction order.                                                                                                |
| surf.Grating\_D = 0.0                | Separation between the lines of the diffraction grating.                                                          |
| surf.Grating\_Angle = 0.0            | Angle of the grating lines in the plane of the surface                                                            |
| surf.ZNK = np.zeros (#)              | Zernike polynomials coefficients                                                                                  |
| surf.ShiftX = 0                      | Offset the surface function on the X or Y axis.                                                                   |
| surf.ShiftY = 0                      |                                                                                                                   |
| surf.Mask = 0                        | (0) Do not apply mask, (1) Use mask as aperture, (2) Use mask as obstruction. Default value: 0                    |
| surf.Mask\_Shape = Object\_3D        | Form of the mask to apply on surface                                                                              |
| surf.AspherData = np.zeros (#)       | Asphericity coefficients.                                                                                         |
| self.ExtraData = \[f, coef\]         | User-defined function for optical surface                                                                         |
| Surf.Error\_map = \[X, Y, Z, SPACE\] | Error map array                                                                                                   |
| surf.Drawing = 1                     | 1 for drawn in the 3D plot, 0 to omit.                                                                            |
| surf.Color = \[0,0,0\]               | Element color for 3D Plot. \[R,G,B\]                                                                              |
| surf.Solid\_3d\_stl = "None"         | Path to the 3D solid STL file.                                                                                    |



## system class attributes and methods

| Attribute or method | Short description |
| --- | --- |
| `system.Trace(pS, dC, wV)` | Sequential ray tracing. `pS` is the ray origin `[x, y, z]`, `dC` is the direction cosine vector `[L, M, N]`, and `wV` is the wavelength in micrometers. |
| `system.NsTrace(pS, dC, wV)` | Non-sequential ray tracing. |
| `system.Parax(w)` | Paraxial optics calculations. |
| `system.disable_inner` | Enables the central aperture. |
| `system.enable_inner` | Disables the central aperture. |
| `system.SURFACE` | Surfaces the ray passed through. |
| `system.NAME` | Surface names the ray passed through. |
| `system.GLASS` | Materials the ray passed through. |
| `system.XYZ` | Ray coordinates from origin to image plane. |
| `system.OST_XYZ` | Ray intersection coordinates in the local surface coordinate system. |
| `system.DISTANCE` | Distances traveled by the ray. |
| `system.OP` | Optical path list. |
| `system.TOP` | Total optical path. |
| `system.TOP_S` | Optical path by sections. |
| `system.ALPHA` | Material absorption coefficients. |
| `system.BULK_TRANS` | Bulk transmission through the system. |
| `system.S_LMN` | Surface normal direction cosines `[L, M, N]`. |
| `system.LMN` | Incident ray direction cosines `[L, M, N]`. |
| `system.R_LMN` | Resulting ray direction cosines `[L, M, N]`. |
| `system.N0` | Refractive indices before each interface. |
| `system.N1` | Refractive indices after each interface. |
| `system.WAV` | Ray wavelength in micrometers. |
| `system.G_LMN` | Direction cosines defining diffraction grating lines on the surface. |
| `system.ORDER` | Ray diffraction order. |
| `system.GRATING_D` | Diffraction grating line spacing in micrometers. |
| `system.RP` | Fresnel reflection coefficient for P polarization. |
| `system.RS` | Fresnel reflection coefficient for S polarization. |
| `system.TP` | Fresnel transmission coefficient for P polarization. |
| `system.TS` | Fresnel transmission coefficient for S polarization. |
| `system.TTBE` | Total energy transmitted or reflected by element. |
| `system.TT` | Total transmitted or reflected energy. |
| `system.targ_surf(int)` | Limits ray tracing to the selected surface. |
| `system.flat_surf(int)` | Changes a surface to flat. |



## User Manual and Examples

The included user manual is [MU-2022-01.pdf](KrakenOS/Docs/MU-2022-01.pdf).

Example scripts are available in `KrakenOS/Examples`:

- `Examp_Axicon.py`
- `Examp_Axicon_And_Cylinder.py`
- `Examp_CzernyTurner.py`
- `Examp_Diffraction_Grating_Reflection.py`
- `Examp_Diffraction_Grating_Reflection_Single.py`
- `Examp_Diffraction_Grating_Transmission.py`
- `Examp_Dispersion_By_AbbeNumber.py`
- `Examp_Doublet_Lens.py`
- `Examp_Doublet_Lens_3Dcolor.py`
- `Examp_Doublet_Lens_CommandsSystem.py`
- `Examp_Doublet_Lens_Cylinder.py`
- `Examp_Doublet_Lens_NonSec.py`
- `Examp_Doublet_Lens_NonSec-AR_Coating.py`
- `Examp_Doublet_Lens_Pupil.py`
- `Examp_Doublet_Lens_Pupil_Seidel.py`
- `Examp_Doublet_Lens_Tilt.py`
- `Examp_Doublet_Lens_Tilt_non_sec.py`
- `Examp_Doublet_Lens_Tilt_non_sec-AR-Coating.py`
- `Examp_Doublet_Lens_Tilt-Nulls.py`
- `Examp_Doublet_Lens_Zernike.py`
- `Examp_Doublet_Lens-ParaxMatrix.py`
- `Examp_Doublet_Optimization.py`
- `Examp_ExtraShape_Micro_Lens_Array.py`
- `Examp_ExtraShape_Radial_Sine.py`
- `Examp_ExtraShape_UserFacets.py`
- `Examp_ExtraShape_XY_Cosines.py`
- `Examp_ExtraShape_XY_Cosines_UDA.py`
- `Examp_Flat_Mirror_45Deg.py`
- `Examp_Flat_NonSec_AR-caoating.py`
- `Examp_Fresnel.py`
- `Examp_Glass_Catalog_Order.py`
- `Examp_ParaboleMirror_Shift.py`
- `Examp_ParaboleMirror_Shift_UDA.py`
- `Examp_Perfect_lens.py`
- `Examp_Perfect_lens_Telescope.py`
- `Examp_Pickle_Doublet_Lens_3Dcolor.py`
- `Examp_Prism_STL.py`
- `Examp_Prism_STL-AR_coating.py`
- `Examp_Ray.py`
- `Examp_Refraction_Prism.py`
- `Examp_Refraction_Prism_OneRay.py`
- `Examp_Refraction_Prism_solid.py`
- `Examp_Refraction_Prism_solid_Generation.py`
- `Examp_RonchiTest.py`
- `Examp_Solid_Object_STL.py`
- `Examp_Solid_Object_STL_ARRAY.py`
- `Examp_Source_Distribution_Function.py`
- `Examp_Sphere.py`
- `Examp_Spruce-tone_Github_User (Manually enter the refractive index, dispersion and alpha).py`
- `Examp_Spruce-tone_Github_User(Loading_Zemax_and_Catalogs).py`
- `Examp_Tel_2M.py`
- `Examp_Tel_2M_Atmospheric_Refraction_Corrector_Adaptable.py`
- `Examp_Tel_2M_Atmospheric_Refraction_Corrector_Static.py`
- `Examp_Tel_2M_Cuña.py`
- `Examp_Tel_2M_Echelle.py`
- `Examp_Tel_2M_Optimization_Variables.py`
- `Examp_Tel_2M_Pupila.py`
- `Examp_Tel_2M_Spyder_Spot_Diagram.py`
- `Examp_Tel_2M_Spyder_Spot_RMS.py`
- `Examp_Tel_2M_Wavefront_Fitting.py`
- `Examp_Tel_2M_Wavefront_Fitting_optimization.py`
- `Examp_Tel_2M-STL_ImageSlicer.py`

Enjoy it!
