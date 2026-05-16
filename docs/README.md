# KrakenOS Documentation

This folder has one intended entry point: the modern
[KrakenOS User Manual](user_manual/README.md). The other documents support that
manual instead of replacing it.

## Recommended Reading Path

1. [User Manual](user_manual/README.md)

   Start here if you are learning KrakenOS. It explains the current workflow:
   installation, core concepts, surfaces, materials, ray tracing, visualization,
   pupils, analysis, and advanced examples.

2. [Example Guide](examples.md)

   Use this when you already know what you want to do and need a runnable
   script to start from.

3. [Generated Examples Manual](examples_manual.md)

   Use this as the visual appendix. It is generated from example docstrings and
   includes reproducible 2D and 3D figures for selected examples.

4. [Capabilities Overview](capabilities.md)

   Use this as a feature map of the current codebase.

5. [Example Coverage Roadmap](example_coverage.md)

   Use this to decide which examples and documentation areas should be improved
   next.

6. [PSF and MTF Notes](psf_mtf_notes.md)

   Use this for focused notes on the compact PSF/MTF helpers.

## Documentation Roles

| Document | Role |
| --- | --- |
| `user_manual/README.md` | Primary learning manual. |
| `examples.md` | Task-to-example lookup table. |
| `examples_manual.md` | Generated visual appendix from examples. |
| `capabilities.md` | Capability map by subsystem. |
| `example_coverage.md` | Maintenance and growth roadmap. |
| `psf_mtf_notes.md` | Focused technical note. |

To regenerate the example figures and generated examples manual:

```bash
python tools/generate_example_images.py --all
```

