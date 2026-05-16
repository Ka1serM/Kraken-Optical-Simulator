# KrakenOS User Manual

This is the primary learning manual for KrakenOS. It is written for users who
want to build optical systems, trace rays, inspect results, and move gradually
from simple sequential examples to advanced 3D, catalog, and instrument-level
workflows.

KrakenOS represents an optical system with two central ideas:

- `surf`: one optical interface, plane, stop, mirror, lens surface, grating,
  solid object, coordinate transform, or analysis plane.
- `system`: an ordered collection of surfaces plus the tracing and analysis
  methods that act on them.

The recommended learning path is:

1. [Installation](installation.md)
2. [Core Concepts](core_concepts.md)
3. [First Optical System](first_optical_system.md)
4. [Surfaces](surfaces.md)
5. [Materials and Catalogs](materials_and_catalogs.md)
6. [Ray Tracing and Ray Data](ray_tracing_and_ray_data.md)
7. [Visualization](visualization.md)
8. [Pupils and Fields](pupils_and_fields.md)
9. [Optical Analysis](optical_analysis.md)
10. [Advanced Workflows](advanced_workflows.md)
11. [API Quick Reference](api_quick_reference.md)

For runnable scripts, use the [Example Guide](../examples.md). For the visual
appendix generated from example docstrings, use the
[Generated Examples Manual](../examples_manual.md). For the full documentation
map, see [KrakenOS Documentation](../README.md).
