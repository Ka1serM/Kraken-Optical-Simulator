# First Optical System

This chapter builds the smallest useful KrakenOS workflow: create surfaces,
assemble a system, trace one ray, and save it in a ray container.

## Build the Surfaces

```python
import KrakenOS as Kos

object_plane = Kos.surf()
object_plane.Thickness = 10.0
object_plane.Glass = "AIR"
object_plane.Diameter = 30.0

first_surface = Kos.surf()
first_surface.Rc = 92.847
first_surface.Thickness = 6.0
first_surface.Glass = "BK7"
first_surface.Diameter = 30.0

second_surface = Kos.surf()
second_surface.Rc = -30.716
second_surface.Thickness = 3.0
second_surface.Glass = "F2"
second_surface.Diameter = 30.0

last_surface = Kos.surf()
last_surface.Rc = -78.197
last_surface.Thickness = 97.376
last_surface.Glass = "AIR"
last_surface.Diameter = 30.0

image_plane = Kos.surf()
image_plane.Thickness = 0.0
image_plane.Glass = "AIR"
image_plane.Diameter = 12.0
image_plane.Name = "Image plane"
```

`Thickness` is the distance from the current surface to the next surface.
`Glass` is the material after the surface. `Rc` is the radius of curvature.

## Create the System

```python
surfaces = [
    object_plane,
    first_surface,
    second_surface,
    last_surface,
    image_plane,
]

config = Kos.Setup()
doublet = Kos.system(surfaces, config)
```

## Trace One Ray

```python
wavelength = 0.55
source = [0.0, 4.0, 0.0]
direction = [0.0, 0.0, 1.0]

doublet.Trace(source, direction, wavelength)
print(doublet.XYZ[-1])
```

After `Trace`, the `system` object contains data from the most recent ray.
Useful first checks are:

- `doublet.val`: whether the trace is valid
- `doublet.XYZ`: global ray coordinates along the path
- `doublet.LMN`: ray direction cosines
- `doublet.GLASS`: materials encountered along the path
- `doublet.SURFACE`: surface numbers touched by the ray

## Save the Ray

```python
rays = Kos.raykeeper(doublet)
rays.push()
```

Use `raykeeper` whenever you trace more than one ray. Each call to
`system.Trace` replaces the current trace stored in the `system`, and
`rays.push()` stores a copy of that trace.

Recommended example: [`Examp_Ray.py`](../../KrakenOS/Examples/Examp_Ray.py).

