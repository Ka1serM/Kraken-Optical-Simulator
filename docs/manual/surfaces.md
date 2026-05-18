# Surfaces

**Manual Navigation:** [Overview](README.md) | [Installation](installation.md) | [Core Concepts](core_concepts.md) | [First System](first_optical_system.md) | [Surfaces](surfaces.md) | [Materials](materials_and_catalogs.md) | [Ray Tracing](ray_tracing_and_ray_data.md) | [Visualization](visualization.md) | [Pupils](pupils_and_fields.md) | [Analysis](optical_analysis.md) | [Advanced](advanced_workflows.md) | [API](api_quick_reference.md)

Previous: [First Optical System](first_optical_system.md) | Next: [Materials and Catalogs](materials_and_catalogs.md)

---

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

![Tilted doublet example](assets/legacy_tilted_doublet_3d.jpg)

Tilts, decenters, repeated elements, and coordinate transforms are easier to
understand visually than from attribute tables alone. Use plots early while
building off-axis systems.

![Axicon and cylinder example](assets/legacy_axicon_cylinder_3d_a.jpg)

Special surface terms such as axicons and cylindrical power can be combined to
create behavior that is not represented by a simple spherical radius.

![User-defined micro-lens array](assets/legacy_microlens_array.jpg)

User-defined surface shapes allow KrakenOS to represent structured optical
surfaces, such as micro-lens arrays or other sampled/analytical profiles.

## Analytical and Numerical Surface Derivatives

KrakenOS uses surface derivatives to compute local surface normals and to solve
ray-surface intersections. Current KrakenOS can mix two derivative strategies:

- analytical derivatives when the active surface terms support them;
- numerical finite-difference derivatives as a compatibility fallback.

This is transparent to normal tracing code. Users still call:

```python
system.Trace(origin, direction, wavelength)
```

Analytical derivatives are currently available for ordinary planes,
conic/spherical/parabolic surfaces, polynomial aspheres, Zernike sag terms, and
axicons away from the singular apex. When these terms are combined on the same
`surf`, KrakenOS sums their sag values and also sums their derivative
contributions. This matches the existing surface model:

```text
Ztotal = Zconic + Zasphere + Zzernike + Zaxicon + ...
dZtotal/dx = dZconic/dx + dZasphere/dx + dZzernike/dx + dZaxicon/dx + ...
dZtotal/dy = dZconic/dy + dZasphere/dy + dZzernike/dy + dZaxicon/dy + ...
```

If any active surface component cannot provide an analytical derivative,
KrakenOS keeps the previous numerical derivative behavior for that surface. This
preserves compatibility with existing user-defined `ExtraData` surfaces,
sampled `Error_map` surfaces, and singular points where an analytical derivative
is not well defined.

For user-defined `ExtraData`, the classic form remains valid:

```python
surface.ExtraData = [sag_function, coefficients]
```

An optional derivative function can be provided when available:

```python
surface.ExtraData = [sag_function, coefficients, derivative_function]
```

The derivative function receives the same `(x, y, coefficients)` inputs and must
return `(dzdx, dzdy)`. If it is omitted, KrakenOS uses the numerical fallback.

Recommended examples:

- [`Examp_ExtraShape_With_Derivative.py`](../../KrakenOS/Examples/Examp_ExtraShape_With_Derivative.py)
- [`Examp_ParaboleMirror_Derivative_Comparison.py`](../../KrakenOS/Examples/Examp_ParaboleMirror_Derivative_Comparison.py)

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
- [`Examp_ExtraShape_With_Derivative.py`](../../KrakenOS/Examples/Examp_ExtraShape_With_Derivative.py)
- [`Examp_ParaboleMirror_Derivative_Comparison.py`](../../KrakenOS/Examples/Examp_ParaboleMirror_Derivative_Comparison.py)
