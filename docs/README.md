# KrakenOS Documentation

This folder has one intended entry point: the modern
[KrakenOS Manual](manual/README.md). The other documents support that
manual instead of replacing it.

## Recommended Reading Path

1. [KrakenOS Manual](manual/README.md)

   Start here if you are learning KrakenOS. It explains the current workflow:
   installation, core concepts, surfaces, materials, ray tracing, visualization,
   pupils, analysis, and advanced examples.

2. [Example Guide](examples.md)

   Use this when you already know what you want to do and need a runnable
   script to start from.

3. [Generated Examples Appendix](examples_manual.md)

   Use this as the visual appendix. It is generated from example docstrings and
   includes reproducible 2D and 3D figures for selected examples.

4. [Capabilities Overview](capabilities.md)

   Use this as a feature map of the current codebase.

5. [Example Coverage Roadmap](example_coverage.md)

   Use this to decide which examples and documentation areas should be improved
   next.

6. [Architecture Notes](architecture.md)

   Use this as a maintenance guide for the current internal flow, build modes,
   PyVista responsibilities, and conservative refactor direction.

7. [PSF and MTF Notes](psf_mtf_notes.md)

   Use this for focused notes on the compact PSF/MTF helpers.

8. [Maintenance Log](maintenance_log.md)

   Use this as an internal handoff log: change control, verification commands,
   and suggested commit messages for each maintenance iteration.

## Documentation Roles

| Document | Role |
| --- | --- |
| `manual/README.md` | Primary learning manual. |
| `examples.md` | Task-to-example lookup table. |
| `examples_manual.md` | Generated visual appendix from examples. |
| `capabilities.md` | Capability map by subsystem. |
| `example_coverage.md` | Maintenance and growth roadmap. |
| `architecture.md` | Internal architecture and refactor notes. |
| `psf_mtf_notes.md` | Focused technical note. |
| `maintenance_log.md` | Internal iteration log and handoff notes. |

To regenerate the example figures and generated examples manual:

```bash
python tools/generate_example_images.py --all
```
