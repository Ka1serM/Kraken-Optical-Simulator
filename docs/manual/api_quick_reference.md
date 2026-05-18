# API Quick Reference

**Manual Navigation:** [Overview](README.md) | [Installation](installation.md) | [Core Concepts](core_concepts.md) | [First System](first_optical_system.md) | [Surfaces](surfaces.md) | [Materials](materials_and_catalogs.md) | [Ray Tracing](ray_tracing_and_ray_data.md) | [Visualization](visualization.md) | [Pupils](pupils_and_fields.md) | [Analysis](optical_analysis.md) | [Advanced](advanced_workflows.md) | [API](api_quick_reference.md)

Previous: [Advanced Workflows](advanced_workflows.md)

---

This page is a compact orientation guide, not a complete API reference.

## `Kos.surf`

Use `surf` to define one optical interface or object.

Common attributes:

| Attribute | Meaning |
| --- | --- |
| `Name` | Human-readable label. |
| `Rc` | Radius of curvature. |
| `Thickness` | Distance to next surface. |
| `Glass` | Material after the surface. |
| `Diameter` | Outer aperture diameter. |
| `InDiameter` | Inner aperture diameter. |
| `k` | Conic constant. |
| `DespX`, `DespY`, `DespZ` | Decenter terms. |
| `TiltX`, `TiltY`, `TiltZ` | Tilt terms. |
| `AxisMove` | Coordinate-axis behavior after a transform. |
| `Thin_Lens` | Ideal thin-lens focal behavior. |
| `Diff_Ord`, `Grating_D`, `Grating_Angle` | Grating behavior. |
| `ZNK` | Zernike surface terms. |
| `AspherData` | Polynomial aspheric sag terms. |
| `ExtraData` | User-defined sag function, optionally with analytical derivative. |
| `Solid_3d_stl` | STL geometry path. |
| `Coating`, `CoatingMet` | Dielectric or metallic coating data. |

Surface derivative behavior:

- KrakenOS uses analytical sag derivatives when every active surface term can
  provide one.
- Analytical derivatives are available for planes, conic/spherical/parabolic
  surfaces, polynomial aspheres, Zernike sag terms, and axicons away from the
  singular apex.
- If a surface includes a component without derivative support, KrakenOS uses
  the historical finite-difference derivative fallback.
- Existing user-defined surfaces remain valid with `ExtraData = [f, coef]`.
- Users can opt into analytical derivatives with
  `ExtraData = [f, coef, df]`, where `df(x, y, coef)` returns `(dzdx, dzdy)`.

## `Kos.system`

Use `system` to assemble surfaces and trace rays.

Common methods:

| Method | Purpose |
| --- | --- |
| `Trace(pS, dC, wV)` | Sequential ray trace. |
| `NsTrace(pS, dC, wV)` | Non-sequential ray trace. |
| `RvTrace(pS, dC, wV, StopSurf)` | Reverse trace. |
| `Parax(w)` | Paraxial calculation. |
| `SetData()` | Rebuild internal surface data after edits. |
| `SetSolid()` | Rebuild solid representation after edits. |

Common trace outputs:

| Attribute | Purpose |
| --- | --- |
| `val` | Validity of the most recent trace. |
| `SURFACE` | Surface sequence. |
| `NAME` | Surface names touched by the ray. |
| `GLASS` | Materials along the ray path. |
| `XYZ` | Global ray coordinates. |
| `OST_XYZ` | Local surface coordinates. |
| `LMN` | Incident direction cosines. |
| `R_LMN` | Resulting direction cosines. |
| `N0`, `N1` | Refractive indices before and after interfaces. |
| `OP`, `TOP`, `TOP_S` | Optical path information. |
| `RP`, `RS`, `TP`, `TS`, `TT` | Energy terms. |

## `Kos.raykeeper`

Use `raykeeper(system)` to store multiple ray traces from the same system.

Common methods:

| Method | Purpose |
| --- | --- |
| `push()` | Store the current ray from the system. |
| `pick(surface)` | Extract coordinates and direction cosines. |
| `clean()` | Clear stored rays. |
| `valid()` | Work with valid ray subsets. |

## `Kos.Setup`

Use `Setup` to configure catalog and material data.

Important concepts:

- default glass catalog loading
- deterministic catalog priority
- optional metal data loading
- configuration passed into `Kos.system`

## `Kos.PupilCalc`

Use `PupilCalc` to generate ray arrays from stop, aperture, and field settings.

Common attributes:

| Attribute | Purpose |
| --- | --- |
| `Samp` | Sampling density. |
| `Ptype` | Pattern type, such as fan or hexapolar. |
| `FieldType` | Field interpretation, such as angle. |
| `FieldX`, `FieldY` | Field coordinates. |

Common method:

| Method | Purpose |
| --- | --- |
| `Pattern2Field()` | Return ray origins and direction cosines. |
