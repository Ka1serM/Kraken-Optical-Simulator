# Core Concepts

KrakenOS is built around explicit optical surfaces and explicit ray traces.
Instead of hiding the system behind a large editor, the user builds a list of
surface objects and passes that list to `Kos.system`.

## The Minimal Mental Model

An optical model usually follows this pattern:

1. Import KrakenOS.
2. Create `surf` objects.
3. Set geometry, material, and aperture attributes on each surface.
4. Put surfaces in order from object space toward image space.
5. Create a `Setup`.
6. Create a `system`.
7. Trace rays with `Trace`, `NsTrace`, or `RvTrace`.
8. Store traced rays with `raykeeper` when more than one ray is needed.
9. Inspect ray data, plot the layout, or run analysis tools.

```python
import KrakenOS as Kos

config = Kos.Setup()
system = Kos.system(surface_list, config)
```

## Main Objects

`surf` stores the definition of one optical interface. A surface may be a
refracting interface, a mirror, an aperture stop, a grating, a thin lens, a
coordinate transform, a user-defined shape, or an STL object.

`system` stores the full ordered model. It performs ray tracing and keeps the
data from the most recent trace in attributes such as `XYZ`, `LMN`, `GLASS`,
`SURFACE`, `OP`, and energy terms.

`raykeeper` stores many traced rays. This avoids losing previous traces when the
same `system` object is reused for the next ray.

`Setup` stores runtime configuration such as glass catalogs and metal data.

`PupilCalc` generates ray origins and direction cosines from stop, aperture,
and field definitions.

## Coordinate and Unit Conventions

The examples use millimeters for distances and micrometers for wavelength
unless a script states otherwise. A ray is defined by:

- `pS`: origin point `[x, y, z]`
- `dC`: direction cosines `[L, M, N]`
- `wV`: wavelength in micrometers

The common direction for sequential examples is from object space toward image
space along positive `z`, but KrakenOS also supports reverse tracing and
non-sequential workflows.

