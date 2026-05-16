# Surfaces

Every optical element in KrakenOS is represented by one or more `surf` objects.
A `surf` can describe a refracting surface, mirror, aperture, ideal thin lens,
grating, coordinate transform, user-defined profile, or STL solid.

## Common Surface Attributes

| Attribute | Purpose |
| --- | --- |
| `Name` | Optional label used in plots and diagnostics. |
| `Rc` | Radius of curvature. Use `0.0` for a plane. |
| `Thickness` | Distance to the next surface. |
| `Glass` | Material after the surface, such as `"AIR"`, `"BK7"`, `"MIRROR"`, or a numeric index. |
| `Diameter` | Outer aperture diameter. |
| `InDiameter` | Inner aperture diameter for central obscurations. |
| `k` | Conic constant. |
| `DespX`, `DespY`, `DespZ` | Surface displacement. |
| `TiltX`, `TiltY`, `TiltZ` | Surface rotation. |
| `AxisMove` | Controls how the coordinate axis moves after transformations. |
| `Drawing` | Whether the surface is drawn in visualization. |
| `Color` | RGB color for 3D visualization. |

## Special Surface Behavior

Several attributes activate specialized behavior:

- `Thin_Lens`: ideal thin-lens power.
- `Cylinder_Rxy_Ratio`: cylindrical or toric behavior.
- `Axicon`: axicon angle term.
- `Diff_Ord`, `Grating_D`, `Grating_Angle`: diffraction grating behavior.
- `ZNK`: Zernike surface coefficients.
- `AspherData`: aspheric coefficients.
- `ExtraData`: user-defined surface functions.
- `Mask`, `Mask_Shape`: apertures, masks, and obstructions.
- `Error_map`: sampled surface error maps.
- `Solid_3d_stl`: STL geometry used as an optical solid.
- `Coating`, `CoatingMet`: dielectric or metallic coating behavior.

## Reserved Materials

Common special values for `Glass` include:

- `"AIR"`: air propagation.
- `"MIRROR"`: reflective surface.
- `"NULL"`: coordinate or placeholder surface without optical power.
- `"ABSORB"`: absorbing surface.

Glass names must match loaded catalog names. A numeric value can be used for a
constant refractive index, but that bypasses wavelength-dependent dispersion.

Recommended examples:

- [`Examp_Doublet_Lens.py`](../../KrakenOS/Examples/Examp_Doublet_Lens.py)
- [`Examp_Perfect_lens.py`](../../KrakenOS/Examples/Examp_Perfect_lens.py)
- [`Examp_Doublet_Lens_Cylinder.py`](../../KrakenOS/Examples/Examp_Doublet_Lens_Cylinder.py)
- [`Examp_Axicon.py`](../../KrakenOS/Examples/Examp_Axicon.py)
- [`Examp_ExtraShape_XY_Cosines.py`](../../KrakenOS/Examples/Examp_ExtraShape_XY_Cosines.py)

