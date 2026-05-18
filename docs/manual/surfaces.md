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

## Numerical Surface Derivatives

KrakenOS uses surface derivatives to compute local surface normals and to solve
ray-surface intersections. The public KrakenOS trace path uses numerical
finite-difference derivatives for ordinary sequential tracing and for
user-defined or sampled surfaces.

This is transparent to normal tracing code. Users still call:

```python
system.Trace(origin, direction, wavelength)
```

Surface sag terms are still additive. For example, when conic, aspheric,
Zernike, axicon, `ExtraData`, or error-map terms are combined on one `surf`,
KrakenOS evaluates the total surface as:

```text
Ztotal = Zconic + Zasphere + Zzernike + Zaxicon + ...
```

The derivative used by the solver is sampled numerically from that same total
surface. This keeps the public behavior consistent for built-in terms,
user-defined `ExtraData` profiles, sampled `Error_map` profiles, masks, and
other mixed surfaces.

For user-defined `ExtraData`, use the classic form:

```python
surface.ExtraData = [sag_function, coefficients]
```

Higher-performance analytical derivative experiments are developed separately
in KrakenCore and are not part of the public KrakenOS API.

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
