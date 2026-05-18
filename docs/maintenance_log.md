# KrakenOS Maintenance Log

This document is a handoff log for ongoing KrakenOS maintenance. Update it after
each working iteration so another assistant or maintainer can continue without
losing context.

## How To Use This Log

For each iteration, record:

- the goal;
- the files changed;
- the behavior protected or changed;
- the verification commands;
- the commit message suggested to the maintainer;
- any follow-up risks or next steps.

Keep entries factual and concise. Do not use this file as user-facing manual
documentation; use it as project continuity notes.

## Current Refactor Direction

KrakenOS keeps the public API stable:

```python
import KrakenOS as Kos

s = Kos.surf()
config = Kos.Setup()
system = Kos.system([s], config)
rays = Kos.raykeeper(system)
```

The internal goal is to reduce unnecessary PyVista coupling while preserving:

- sequential tracing behavior;
- non-sequential tracing behavior;
- STL solids;
- UDA polygons;
- masks and side-face interactions;
- existing examples and documentation.

PyVista remains justified as the current backend for 3D visualization, STL/mesh
geometry, masks, side faces, and ray-mesh intersection. The refactor should
remove or encapsulate PyVista only where it is acting as an unnecessary
container, conversion step, or eager dependency.

## Iteration Log

### 2026-05-17 - Remove PyVista Dependency From RayKeeper

Goal:

- Keep `raykeeper` focused on numerical ray records.

Files changed:

- `KrakenOS/RayKeeper.py`

Changes:

- Removed the direct `pyvista` import.
- Replaced unused `valid_CCC` and `invalid_CCC` PyVista `MultiBlock`
  placeholders with plain lists.
- Preserved those attributes for compatibility.

Verification:

```powershell
python -m py_compile KrakenOS\RayKeeper.py
python tests\test_smoke.py
```

Suggested commit:

```text
Remove PyVista dependency from raykeeper
```

```text
- Keep raykeeper focused on numerical ray data
- Replace unused PyVista MultiBlock placeholders with plain lists
- Preserve valid_CCC and invalid_CCC attributes for compatibility
- Verify smoke test still passes
```

### 2026-05-17 - Add Lightweight MeshBlock Container

Goal:

- Replace simple PyVista `MultiBlock` containers where only list behavior and
  `.n_blocks` compatibility are needed.

Files changed:

- `KrakenOS/MeshBlock.py`
- `KrakenOS/Prerequisites3D.py`
- `KrakenOS/SurfClass.py`
- `KrakenOS/__init__.py`
- `KrakenOS/Display.py`

Changes:

- Added `MeshBlock`, a list-like container with `.n_blocks` and deep-copy
  support.
- Used `MeshBlock` for internal geometry block collections and dummy masks.
- Updated 3D display to draw nested mesh block containers by iterating through
  their contents.

Verification:

```powershell
python -m py_compile KrakenOS\MeshBlock.py KrakenOS\Prerequisites3D.py KrakenOS\SurfClass.py KrakenOS\__init__.py
python tests\test_smoke.py
```

Additional manual checks:

- `build=0` and `build=1` basic tracing.
- Masked tracing with a user-provided PyVista mask.
- Simple `NsTrace`.
- `Examp_Doublet_Lens_NonSec.py` display path with `Plotter.show` disabled.

Suggested commits:

```text
Add lightweight MeshBlock container
```

```text
- Add MeshBlock as a small list-like replacement for simple MultiBlock containers
- Use MeshBlock for internal geometry block collections and dummy masks
- Preserve n_blocks compatibility for display and system code
- Verify smoke test, build=0/build=1 tracing, mask tracing, and NsTrace
```

```text
Support MeshBlock containers in 3D display
```

```text
- Add a display helper that plots nested mesh block containers
- Keep PyVista rendering compatible with MeshBlock-backed DDD masks
- Fix non-sequential doublet display after replacing internal MultiBlock containers
- Verify smoke test and Examp_Doublet_Lens_NonSec display path
```

### 2026-05-17 - Plot 2D Rays Directly From Ray Data

Goal:

- Remove unnecessary PyVista conversion from 2D ray plotting.

Files changed:

- `KrakenOS/Display.py`

Changes:

- `Plot2DRays()` now draws directly from `RAYS.CC` numerical arrays.
- Removed `pv.MultiBlock()` and `pv.lines_from_points()` from this 2D ray path.

Verification:

```powershell
python -m py_compile KrakenOS\Display.py
python tests\test_smoke.py
```

Additional manual check:

- `Kos.display2d(...)` in non-interactive Matplotlib mode.

Suggested commit:

```text
Plot 2D rays directly from ray data
```

```text
- Remove unnecessary PyVista line conversion from Plot2DRays
- Draw 2D rays directly from RAYS.CC numeric arrays
- Preserve existing wavelength coloring and arrow behavior
- Verify smoke test and display2d path
```

### 2026-05-17 - Avoid Dummy PyVista Masks In Face3D

Goal:

- Stop creating a fake PyVista mask when a surface has no mask.

Files changed:

- `KrakenOS/Prerequisites3D.py`

Changes:

- Treat missing `Mask_Shape` as an empty `MeshBlock`.
- Keep `SurfClass.RestoreVTK()` available as a legacy method, but no longer use
  it automatically in `Face3D()`.

Verification:

```powershell
python -m py_compile KrakenOS\Prerequisites3D.py
python tests\test_smoke.py
```

Additional manual checks:

- Unmasked system tracing.
- Masked system tracing.
- `Examp_Doublet_Lens_NonSec.py` display path with `Plotter.show` disabled.

Suggested commit:

```text
Avoid dummy PyVista masks in Face3D
```

```text
- Treat missing Mask_Shape as an empty MeshBlock
- Stop creating a dummy PyVista mask for unmasked surfaces
- Keep RestoreVTK available for legacy compatibility
- Verify smoke test, masked/unmasked tracing, and non-sequential display path
```

### 2026-05-17 - Build UDA Meshes Lazily

Goal:

- Separate UDA polygon hit testing from PyVista mesh construction.

Files changed:

- `KrakenOS/UDA.py`

Changes:

- Stored polygon coordinates and `matplotlib.path` in the constructor.
- Deferred PyVista mesh construction until `UDA_Surf` is accessed.
- Preserved assignment compatibility through a `UDA_Surf` property setter.

Verification:

```powershell
python -m py_compile KrakenOS\UDA.py KrakenOS\Prerequisites3D.py
python tests\test_smoke.py
```

Additional manual checks:

- `UDA.Hit()` does not construct `_UDA_Surf`.
- `UDA_Surf` constructs the mesh lazily.
- System with UDA surface traces.
- `Examp_ExtraShape_XY_Cosines_UDA.py`.
- `Examp_ParaboleMirror_Shift_UDA.py`.

Suggested commit:

```text
Build UDA meshes lazily
```

```text
- Keep UDA polygon hit testing independent from mesh generation
- Build the PyVista UDA surface only when UDA_Surf is requested
- Preserve UDA_Surf assignment compatibility
- Verify smoke test and UDA examples
```

### 2026-05-17 - Make Build Zero Skip Dummy Side Meshes

Goal:

- Make `build=0` a lighter sequential setup without losing side-face behavior
  when full geometry is later needed.

Files changed:

- `KrakenOS/Prerequisites3D.py`

Changes:

- `Prerequisites3DSolidsDummy()` no longer builds dummy side meshes.
- Full geometry rebuild remains automatic for `NsTrace()`, `display2d()`, and
  `display3d()`.

Verification:

```powershell
python -m py_compile KrakenOS\Prerequisites3D.py KrakenOS\KrakenSys.py KrakenOS\Display.py
python tests\test_smoke.py
```

Additional manual checks:

- `build=0` sequential tracing.
- `display2d()` from `build=0` triggers full geometry rebuild.
- `display3d()` from `build=0` triggers full geometry rebuild.
- `NsTrace()` from `build=0` triggers full geometry rebuild.

Suggested commit:

```text
Make build zero skip dummy side meshes
```

```text
- Avoid building PyVista side meshes in Prerequisites3DSolidsDummy
- Keep build=0 focused on lightweight sequential tracing setup
- Preserve automatic solid rebuilds for display2d, display3d, and NsTrace
- Verify smoke test and build=0 tracing/display paths
```

### 2026-05-17 - Add Build Mode Regression Test

Goal:

- Protect side-face rebuild behavior from `build=0`.

Files changed:

- `tests/test_build_modes.py`
- `tests/test_build_modes_report.txt`

Changes:

- Added a script-style regression test showing that `build=0` starts without
  side meshes and `NsTrace()` rebuilds full solid geometry and side faces.

Verification:

```powershell
python -m py_compile tests\test_build_modes.py
python tests\test_build_modes.py
python tests\test_smoke.py
```

Suggested commit:

```text
Add build mode regression test
```

```text
- Verify build=0 starts without side meshes
- Verify NsTrace rebuilds full solid geometry and side faces
- Record a build mode test report for quick local inspection
- Keep smoke test passing
```

### 2026-05-17 - Document KrakenOS Architecture And PyVista Roles

Goal:

- Record the current architecture and conservative PyVista refactor direction.

Files changed:

- `docs/architecture.md`
- `docs/README.md`

Changes:

- Added Mermaid diagrams for current flow, build modes, and layering.
- Documented PyVista responsibilities and completed decoupling steps.
- Linked architecture notes from the documentation index.

Verification:

```powershell
python tests\test_smoke.py
python tests\test_build_modes.py
python -m py_compile tests\test_smoke.py tests\test_build_modes.py
```

Additional checks:

- Local Markdown link check.
- Balanced fenced code block check.

Suggested commit:

```text
Document KrakenOS architecture and PyVista roles
```

```text
- Add architecture notes with Mermaid diagrams
- Document build=0/build=1 behavior and PyVista responsibilities
- Record completed decoupling steps and future refactor candidates
- Link architecture notes from the documentation index
- Verify smoke and build mode tests
```

### 2026-05-17 - Load PyVista Lazily In SurfClass

Goal:

- Avoid global PyVista import from `SurfClass.py`.

Files changed:

- `KrakenOS/SurfClass.py`

Changes:

- Moved `import pyvista as pv` into `RestoreVTK()`.
- Preserved legacy `RestoreVTK()` behavior.

Verification:

```powershell
python -m py_compile KrakenOS\SurfClass.py
python tests\test_smoke.py
python tests\test_build_modes.py
```

Additional manual checks:

- `s = Kos.surf()`
- `s.EraseVTK()`
- `s.RestoreVTK()`
- Basic tracing from a `build=0` system.

Suggested commit:

```text
Load PyVista lazily in SurfClass
```

```text
- Remove the global PyVista import from SurfClass
- Import PyVista only when RestoreVTK is called
- Preserve legacy RestoreVTK behavior with MeshBlock masks
- Verify smoke test, build mode test, and basic tracing
```

### 2026-05-17 - Centralize 3D Ray Polyline Conversion

Goal:

- Encapsulate the conversion from numerical ray points to PyVista polylines.

Files changed:

- `KrakenOS/Display.py`

Changes:

- Added `_ray_points_to_polyline(points)`.
- Replaced repeated direct `pv.lines_from_points()` calls.
- Replaced ray `pv.MultiBlock()` containers with simple lists in 3D display
  paths.

Verification:

```powershell
python tests\test_smoke.py
python tests\test_build_modes.py
```

Additional manual checks with `Plotter.show` disabled:

- `Kos.display3d(...)`
- `Kos.display3d_old(...)`
- `Kos.display3d_OB().plot()`

Suggested commit:

```text
Centralize 3D ray polyline conversion
```

```text
- Add an internal helper for converting ray points to PyVista polylines
- Replace 3D ray MultiBlock containers with simple lists
- Keep 3D display behavior unchanged
- Verify display3d, display3d_old, display3d_OB, smoke test, and build mode test
```

### 2026-05-17 - Add Representative Examples Regression Test

Goal:

- Create a faster examples regression subset covering important workflows.

Files changed:

- `tests/test_examples_subset.py`
- `tests/test_examples_subset_report.txt`

Changes:

- Added a non-interactive examples subset test.
- Disabled Matplotlib and PyVista windows during the test.
- Covered sequential, non-sequential, UDA, mask, and STL workflows.

Verification:

```powershell
python -m py_compile tests\test_examples_subset.py
python tests\test_examples_subset.py
python tests\test_smoke.py
python tests\test_build_modes.py
```

Suggested commit:

```text
Add representative examples regression test
```

```text
- Add a non-interactive examples subset test
- Cover sequential, non-sequential, UDA, mask, and STL workflows
- Record an examples subset report for quick inspection
- Verify smoke and build mode tests
```

### 2026-05-17 - Add Internal Geometry Backend Adapter

Goal:

- Centralize simple PyVista mesh creation/loading calls before any future backend
  replacement.

Files changed:

- `KrakenOS/GeometryBackend.py`
- `KrakenOS/Prerequisites3D.py`
- `docs/architecture.md`
- `tests/test_examples_subset.py`
- `tests/test_examples_subset_report.txt`

Changes:

- Added `GeometryBackend.py` with `make_disc`, `make_polydata`,
  `read_mesh`, and `is_polydata`.
- Routed `Prerequisites3D.py` mesh creation and loading through the adapter.
- Updated architecture notes.
- Stabilized the examples subset report by removing variable timing output.

Verification:

```powershell
python -m py_compile KrakenOS\GeometryBackend.py KrakenOS\Prerequisites3D.py tests\test_examples_subset.py
python tests\test_smoke.py
python tests\test_build_modes.py
python tests\test_examples_subset.py
```

Suggested commit:

```text
Add internal geometry backend adapter
```

```text
- Add GeometryBackend as a small PyVista adapter
- Route Prerequisites3D mesh creation and loading through the backend
- Document the backend in the architecture notes
- Stabilize the examples subset report output
- Verify smoke, build mode, and examples subset tests
```

### 2026-05-17 - Clean Display Backups And Stabilize Prerequisites3D

Goal:

- Clean duplicate display backup files from the package root.
- Apply a minimal stabilization pass to `Prerequisites3D.py`.

Files changed:

- `KrakenOS/Display (1).py`
- `KrakenOS/Display (2).py`
- `KrakenOS/DisplayResplado.py`
- `KrakenOS/Prerequisites3D.py`

Changes:

- Removed untracked duplicate/backup display files from the package root.
- Removed duplicate `Flat2SigmaSurface(disc, j)` processing.
- Assigned returned meshes from `compute_normals(..., inplace=False)`.
- Ensured `lens` and `masked` are initialized for every surface in
  `Prerequisites3DSolids()`, including `Const[1] != 0`.

Verification:

```powershell
python -m py_compile KrakenOS\Prerequisites3D.py
python tests\test_smoke.py
python tests\test_build_modes.py
python tests\test_examples_subset.py
```

Additional manual check:

- Built and traced a system with `Const[1] = 1`.

Suggested commit:

```text
Clean display backups and stabilize Prerequisites3D
```

```text
- Remove duplicate Display backup files from the package root
- Avoid duplicate Flat2SigmaSurface processing in Face3D
- Preserve computed normals returned by PyVista
- Ensure lens and mask geometry are always initialized in Prerequisites3DSolids
- Verify smoke, build mode, examples subset, and Const[1] geometry paths
```

Follow-up:

- `KrakenOS/Display.py` and `KrakenOS/Examples/Examp_Interactive_Display.py`
  were already modified/untracked locally during this iteration context. Review
  them separately before including in any commit.

### 2026-05-17 - Centralize PyVista Normal Computation

Goal:

- Keep `Prerequisites3D.py` behavior unchanged while making PyVista normal
  computation easier to review and maintain.

Files changed:

- `KrakenOS/GeometryBackend.py`
- `KrakenOS/Prerequisites3D.py`
- `docs/maintenance_log.md`

Changes:

- Added a shared `NORMAL_OPTIONS` dictionary to `GeometryBackend.py`.
- Added `compute_normals(mesh)` as the internal backend wrapper for PyVista
  normal generation.
- Replaced three repeated `mesh.compute_normals(...)` calls in
  `Prerequisites3D.py` with `compute_normals(mesh)`.
- Preserved the same PyVista options, including `inplace=False`, so the mesh
  returned by PyVista is still used explicitly.

Verification:

```powershell
python -m py_compile KrakenOS\GeometryBackend.py KrakenOS\Prerequisites3D.py
python tests\test_smoke.py
python tests\test_build_modes.py
python tests\test_examples_subset.py
```

Notes:

- The examples subset still reports existing numerical runtime warnings in
  `Physics.py` and `PhysicsClass.py`; these warnings did not fail the test.

Suggested commit:

```text
Centralize PyVista normal computation
```

```text
- Add a shared compute_normals helper in GeometryBackend
- Route Prerequisites3D normal generation through the backend adapter
- Preserve existing PyVista normal options and returned-mesh behavior
- Verify smoke, build mode, and examples subset tests
```

### 2026-05-17 - Make Tests Pytest Discoverable

Goal:

- Allow maintainers and CI systems to run the existing checks with
  `python -m pytest tests`.
- Preserve the previous script-style test execution.

Files changed:

- `pyproject.toml`
- `tests/test_smoke.py`
- `tests/test_build_modes.py`
- `tests/test_examples_subset.py`
- `docs/maintenance_log.md`

Changes:

- Added one `test_*` function to each existing test script.
- Kept each script's `main()` entry point, so direct execution still works.
- Added a `dev` optional dependency group with `pytest`.

Verification:

```powershell
python -m py_compile tests\test_smoke.py tests\test_build_modes.py tests\test_examples_subset.py
python tests\test_smoke.py
python tests\test_build_modes.py
python tests\test_examples_subset.py
python -m pip install -e ".[dev]"
python -m pytest tests
```

Result:

- `pytest` collected 3 tests and all passed.
- The run reports many existing warnings, mostly `np.matrix`
  pending-deprecation warnings plus known numerical runtime warnings.

Suggested commit:

```text
Make tests discoverable by pytest
```

```text
- Add pytest-compatible test functions to existing test scripts
- Keep direct script execution working for the same checks
- Add pytest as an optional development dependency
- Update the maintenance log with verification notes
- Verify scripts and pytest test discovery
```

### 2026-05-17 - Add Public API Contract Test

Goal:

- Protect the traditional `import KrakenOS as Kos` public API before future
  changes to package-level imports.

Files changed:

- `tests/test_public_api.py`
- `docs/maintenance_log.md`

Changes:

- Added a public API contract test for names used by current examples and
  documentation, including `surf`, `Setup`, `system`, `raykeeper`, display
  helpers, pupil tools, PSF/MTF helpers, wavefront helpers, and Zemax/lens
  catalog helpers.
- Added a construction smoke check for `surf`, `Setup`, `system(..., build=0)`,
  and `raykeeper`.

Verification:

```powershell
python -m py_compile tests\test_public_api.py
python -m pytest tests
```

Result:

- `pytest` collected 5 tests and all passed.
- Existing warnings remain noisy, especially `np.matrix`
  pending-deprecation warnings.

Notes:

- `Display2D`, `Display3D`, and `system_Lite` appear in searched text but are
  not currently exposed as `Kos.Display2D`, `Kos.Display3D`, or
  `Kos.system_Lite`. They were not added to the public API contract in this
  iteration.

Suggested commit:

```text
Add public API contract test
```

```text
- Add a pytest contract for public KrakenOS names used by examples
- Verify core objects can still be created through import KrakenOS as Kos
- Record current non-exposed references for future review
- Update the maintenance log with verification notes
- Verify the full pytest suite
```

### 2026-05-17 - Restore Display Aliases And Remove Obsolete Lite Reference

Goal:

- Resolve public API inconsistencies found while preparing future
  package-level import cleanup.

Files changed:

- `KrakenOS/Display.py`
- `KrakenOS/Examples/Examp_ParaboleMirror_Shift.py`
- `tests/test_public_api.py`
- `docs/maintenance_log.md`

Changes:

- Added backward-compatible `Display2D = display2d` and
  `Display3D = display3d` aliases.
- Added `Display2D` and `Display3D` to the public API contract test.
- Replaced the obsolete commented `Kos.system_Lite(...)` example with the
  current lightweight construction form: `Kos.system(..., build=0)`.

Verification:

```powershell
python -m py_compile KrakenOS\Display.py KrakenOS\Examples\Examp_ParaboleMirror_Shift.py tests\test_public_api.py
python -m pytest tests
```

Additional check:

```python
import KrakenOS as Kos
assert Kos.Display2D is Kos.display2d
assert Kos.Display3D is Kos.display3d
```

Result:

- `pytest` collected 5 tests and all passed.
- Existing warning noise remains unchanged.

Suggested commit:

```text
Restore legacy display aliases
```

```text
- Add Display2D and Display3D aliases for backward compatibility
- Include the legacy display aliases in the public API contract
- Replace an obsolete system_Lite comment with system(..., build=0)
- Update the maintenance log with verification notes
- Verify the full pytest suite
```

### 2026-05-17 - Add RayKeeper Result Ingestion Path

Goal:

- Prepare `raykeeper` for parallel tracing workflows where workers return
  extracted ray results instead of full `system` or `raykeeper` objects.

Files changed:

- `KrakenOS/RayKeeper.py`
- `tests/test_raykeeper_results.py`
- `tests/test_public_api.py`
- `docs/maintenance_log.md`

Changes:

- Added `extract_ray_result(system)` to capture the current traced ray state
  without returning the full mutable system.
- Added `raykeeper.push_result(result)` to store one extracted result.
- Added `raykeeper.extend_results(results)` to ingest multiple extracted
  results.
- Kept the classic `system.Trace(...); rays.push()` workflow working by making
  `push()` call `push_result(extract_ray_result(self.SYSTEM))`.
- Added tests proving `push_result(extract_ray_result(system))` matches
  `push()` for valid and invalid rays.
- Added `extract_ray_result` to the public API contract.

Verification:

```powershell
python -m py_compile KrakenOS\RayKeeper.py tests\test_raykeeper_results.py tests\test_public_api.py
python -m pytest tests\test_raykeeper_results.py tests\test_invalid_trace_results.py tests\test_public_api.py -q
python -m pytest tests\test_trace_performance_components.py -s
python -m pytest tests
```

Result:

- Targeted raykeeper/result tests passed.
- Full test suite collected 13 tests and all passed.
- The performance component test showed `raykeeper.push()` still has measurable
  overhead compared with minimal extraction; this is now explicit and can be
  optimized later.

Suggested commit:

```text
Add RayKeeper result ingestion path
```

```text
- Add extract_ray_result for decoupling traced ray data from system objects
- Add push_result and extend_results to raykeeper
- Keep the classic push workflow as a compatibility wrapper
- Verify push_result matches push for valid and invalid rays
- Update the public API contract and maintenance log
```

### 2026-05-17 - Connect Parallel Trace Prototype To RayKeeper Results

Goal:

- Prove the intended parallel workflow end to end:
  worker-local tracing, extracted ray results, parent-process raykeeper
  reconstruction.

Files changed:

- `tests/test_parallel_trace.py`
- `docs/maintenance_log.md`

Changes:

- Updated the parallel trace prototype so each worker calls
  `Kos.extract_ray_result(system)` after `Trace()`.
- Kept workers independent: each process owns its own `system(build=0)`.
- Added parent-process reconstruction through
  `raykeeper.extend_results(results)`.
- Compared the reconstructed raykeeper against a classic sequential
  `system.Trace(...); rays.push()` raykeeper.
- Preserved timing output for `parallel_total` and `parallel_warm_trace`.

Verification:

```powershell
python -m py_compile tests\test_parallel_trace.py
python -m pytest tests\test_parallel_trace.py -s
python -m pytest tests
```

Result:

- `tests/test_parallel_trace.py` passed.
- Full test suite collected 13 tests and all passed.
- Warm parallel timings still show useful speedup for moderate worker counts,
  while total time remains dominated by Windows process startup/import overhead.

Suggested commit:

```text
Connect parallel trace prototype to RayKeeper results
```

```text
- Use extract_ray_result inside parallel trace workers
- Rebuild raykeeper in the parent process with extend_results
- Compare reconstructed raykeeper data with the classic push workflow
- Preserve warm parallel timing diagnostics
- Verify the full pytest suite
```

### 2026-05-17 - Split Parallel Trace Benchmark From Pytest

Goal:

- Keep automated tests fast while preserving a reusable benchmark for parallel
  sequential tracing experiments.

Files changed:

- `tests/test_parallel_trace.py`
- `tools/benchmark_parallel_trace.py`
- `docs/maintenance_log.md`

Changes:

- Reduced the pytest parallel trace coverage to a small deterministic case.
- Kept the correctness contract in pytest:
  sequential results, parallel worker results, and reconstructed raykeeper data
  must match.
- Added `tools/benchmark_parallel_trace.py` as a standalone benchmark for larger
  worker/ray-count sweeps.
- The benchmark reports both total multiprocessing time and warm trace time,
  making Windows process startup overhead visible.

Verification:

```powershell
python -m py_compile tests\test_parallel_trace.py tools\benchmark_parallel_trace.py
python tools\benchmark_parallel_trace.py --rays 100 --workers 1 2
python -m pytest tests\test_parallel_trace.py -s
python -m pytest tests
```

Result:

- The standalone benchmark passed its sequential/parallel numerical
  validation.
- The short benchmark showed that total multiprocessing time is dominated by
  worker startup, while warm parallel tracing can already be faster than the
  sequential path.
- Full test suite collected 13 tests and all passed.

Suggested commit:

```text
Split parallel trace benchmark from pytest
```

```text
- Keep pytest parallel trace coverage short and deterministic
- Add standalone warm parallel trace benchmark
- Validate benchmark results against sequential tracing
- Report total and warm multiprocessing timings separately
- Update the maintenance log
```

### 2026-05-17 - Add Parallel Sequential Trace Example

Goal:

- Provide a user-facing example for the parallel-ready sequential tracing
  pattern validated by the tests and benchmark.

Files changed:

- `KrakenOS/Examples/Examp_Parallel_Trace.py`
- `docs/maintenance_log.md`

Changes:

- Added an example that builds a lightweight `system(build=0)` inside each
  worker process.
- Traces deterministic ray batches in parallel with Windows-compatible
  multiprocessing `spawn`.
- Returns only serializable numerical ray results from workers.
- Reconstructs a parent-process `raykeeper` with `extend_results`.
- Prints sequential warm time, parallel total time, parallel warm trace time,
  and numerical validation status.

Verification:

```powershell
python -m py_compile KrakenOS\Examples\Examp_Parallel_Trace.py
python KrakenOS\Examples\Examp_Parallel_Trace.py
```

Result:

- The example ran successfully on Windows.
- For 1000 rays and 4 workers, the example reported a warm trace speedup above
  2x while making the process startup overhead visible.
- Parallel and sequential numerical results matched.
- The reconstructed raykeeper contained all traced rays.

Suggested commit:

```text
Add parallel sequential trace example
```

```text
- Add example for worker-local build=0 sequential tracing
- Return serializable ray results from multiprocessing workers
- Reconstruct raykeeper in the parent process with extend_results
- Print total and warm parallel timing diagnostics
- Update the maintenance log
```

### 2026-05-17 - Add Simple Plane Fast Path

Goal:

- Avoid unnecessary Newton intersection and finite-difference normal
  evaluation for strict analytical z=0 plane surfaces.

Files changed:

- `KrakenOS/HitOnSurf.py`
- `KrakenOS/InterNormalCalc.py`
- `tests/test_simple_plane_fast_path.py`
- `docs/maintenance_log.md`

Changes:

- Added `Hit_Solver.IsSimplePlane(j)` as a conservative internal predicate for
  traditional plane surfaces.
- `SolveHit()` now returns the already-known local plane hit directly for
  simple planes.
- `InterNormalCalc.__SigmaOutOrigSpace()` now computes the plane normal through
  the existing two-point transform convention instead of calling `SurfDer()`.
- Added code comments documenting why the fast path is intentionally narrow and
  why general surfaces stay on the original numerical path.
- Added tests proving:
  - simple plane tracing avoids Newton and finite-difference normals;
  - the fast path matches the original general solver when that path is forced.

Verification:

```powershell
python -m py_compile KrakenOS\HitOnSurf.py KrakenOS\InterNormalCalc.py tests\test_simple_plane_fast_path.py
python -m pytest tests\test_simple_plane_fast_path.py -q
python -m pytest tests
python -m pytest tests\test_trace_performance_components.py -s
```

Result:

- Full test suite collected 15 tests and all passed.
- For the representative doublet trace counter, `SurfaceShape` calls dropped
  from 9034 to 7034 per 1000 rays and `SurfDer` calls dropped from 3000 to
  2000 per 1000 rays.
- End-to-end timing on the doublet changed little because the remaining
  spherical surfaces still dominate the cost; this confirms the next
  performance target should be conic/spherical intersection and normal logic.

Suggested commit:

```text
Add simple plane trace fast path
```

```text
- Detect strict analytical plane surfaces in Hit_Solver
- Skip Newton intersection for simple z=0 planes
- Skip finite-difference normal evaluation for simple planes
- Add regression tests against the general solver path
- Update the maintenance log
```

### 2026-05-17 - Add Mixed Analytical Sag Derivatives

Goal:

- Use analytical sag derivatives when every active surface component can
  provide them, while preserving the existing finite-difference fallback for
  user-defined or sampled surfaces.

Files changed:

- `KrakenOS/MathShapesClass.py`
- `KrakenOS/SurfClass.py`
- `KrakenOS/HitOnSurf.py`
- `tests/test_surface_analytic_derivatives.py`
- `docs/maintenance_log.md`

Changes:

- Added optional `derivative(x, y)` methods for:
  - conic/spherical surfaces;
  - polynomial aspheres;
  - axicons, except at the singular apex;
  - Zernike surfaces, following KrakenOS's existing `arctan2(x, y)`
    convention.
- Added optional derivative support for `ExtraData`:
  - existing `ExtraData = [surface, coef]` keeps the numerical fallback;
  - new `ExtraData = [surface, coef, derivative]` can return `(dzdx, dzdy)`.
- Added `surf.sigma_derivative(x, y, case)` to sum derivative contributions in
  the same order and with the same component stack used by `sigma_z()`.
- Updated `Hit_Solver.SurfDer()` to use analytical derivatives for surface
  normals when available.
- Updated Newton line solving to use the chain-rule derivative
  `dF/dz = dzdx * L/N + dzdy * M/N - 1` when available.
- Kept the finite-difference path as the automatic fallback whenever any active
  component cannot provide an analytical derivative.
- Added scalar fast paths to avoid creating tiny NumPy arrays during ray-by-ray
  tracing.

Verification:

```powershell
python -m py_compile KrakenOS\MathShapesClass.py KrakenOS\SurfClass.py KrakenOS\HitOnSurf.py tests\test_surface_analytic_derivatives.py
python -m pytest tests\test_surface_analytic_derivatives.py -q
python -m pytest tests
python -m pytest tests\test_trace_performance_components.py -s
python tools\benchmark_parallel_trace.py --rays 1000 --workers 4
```

Result:

- Full test suite collected 19 tests and all passed.
- Analytical derivatives matched finite-difference slopes for conic,
  aspheric, Zernike, and mixed surfaces.
- Existing `ExtraData` without derivative remains compatible and uses the
  numerical fallback.
- A mixed traced surface using analytical derivatives matched the forced
  finite-difference path.
- Representative doublet counters for 1000 rays:
  - `SurfaceShape` calls dropped from 7034 to 4876 after analytical Newton
    derivatives.
  - `SurfDer` calls remained at 2000, but those calls now use analytical
    normals when possible.
- `tests/test_trace_performance_components.py` reported:
  - `trace_only=0.177311s`
  - `trace_plus_minimal_extract=0.184357s`
  - `trace_plus_raykeeper_push=0.207696s`
- Parallel benchmark for 1000 rays and 4 workers reported:
  - `sequential_warm=0.166525s`
  - `parallel_warm_trace=0.106552s`
  - `warm_speedup=1.563x`

Suggested commit:

```text
Add mixed analytical sag derivatives
```

```text
- Add analytical derivatives for conic, aspheric, axicon, and Zernike sag terms
- Sum analytical derivative contributions through surf.sigma_derivative
- Preserve finite-difference fallback for unsupported surface components
- Allow optional user-provided ExtraData derivatives
- Use analytical derivatives for normals and Newton line solving
- Add derivative and trace regression tests
- Update the maintenance log
```

### 2026-05-17 - Add ExtraData Derivative Example

Goal:

- Provide a user-facing example that shows how to add an optional analytical
  derivative to a custom `ExtraData` surface.

Files changed:

- `KrakenOS/Examples/Examp_ExtraShape_With_Derivative.py`
- `KrakenOS/Examples/EXAMPLES_INDEX.md`
- `tests/test_examples_subset.py`
- `docs/maintenance_log.md`

Changes:

- Added a didactic example with a smooth 2D cosine sag function.
- Shows the new optional form:
  `ExtraData = [surface_function, coefficients, derivative_function]`.
- Compares the analytical derivative path against the old numerical fallback:
  `ExtraData = [surface_function, coefficients]`.
- Prints timing and maximum final ray differences.
- Added the example to the examples index.
- Added the example to the representative examples test subset.

Verification:

```powershell
python -m py_compile KrakenOS\Examples\Examp_ExtraShape_With_Derivative.py tests\test_examples_subset.py
python KrakenOS\Examples\Examp_ExtraShape_With_Derivative.py
python -m pytest tests\test_examples_subset.py -q
python -m pytest tests
```

Result:

- The example ran successfully.
- Example output for 441 rays:
  - analytical derivative time: `0.054011s`
  - numerical fallback time: `0.059581s`
  - max final XYZ difference: `1.375182e-09`
  - max final LMN difference: `1.392064e-10`
- Full test suite collected 19 tests and all passed.

Suggested commit:

```text
Add ExtraData derivative example
```

```text
- Add example for user-defined ExtraData analytical derivatives
- Compare analytical and numerical fallback tracing paths
- Add the example to the examples index and representative test subset
- Update the maintenance log
```

### 2026-05-17 - Add Parabolic Mirror Derivative Comparison Example

Goal:

- Provide a visual and numerical image-quality comparison between analytical
  and numerical derivative tracing on a shifted parabolic mirror.

Files changed:

- `KrakenOS/Examples/Examp_ParaboleMirror_Derivative_Comparison.py`
- `KrakenOS/Examples/EXAMPLES_INDEX.md`
- `tests/test_examples_subset.py`
- `docs/maintenance_log.md`

Changes:

- Added a parabolic mirror comparison example based on
  `Examp_ParaboleMirror_Shift.py`.
- Traces the same ray bundle twice:
  - once with the analytical derivative path;
  - once with `sigma_derivative` disabled to force the numerical fallback.
- Prints RMS spot radius, maximum spot radius, centroid, and trace time.
- Plots analytical and numerical spot diagrams side by side.
- Added the example to the examples index and representative examples test.

Verification:

```powershell
python -m py_compile KrakenOS\Examples\Examp_ParaboleMirror_Derivative_Comparison.py tests\test_examples_subset.py
python KrakenOS\Examples\Examp_ParaboleMirror_Derivative_Comparison.py
python -m pytest tests\test_examples_subset.py -q
python -m pytest tests
```

Result:

- The example ran successfully.
- Example output for 697 rays:
  - analytical RMS spot: `5.182787959976e-14 mm`
  - numerical fallback RMS spot: `2.577772152048e-13 mm`
  - RMS improvement factor: `4.974x`
  - analytical time: `0.115581s`
  - numerical fallback time: `0.137818s`
- Full test suite collected 19 tests and all passed.

Suggested commit:

```text
Add parabolic mirror derivative comparison example
```

```text
- Add parabolic mirror image-quality comparison example
- Compare analytical and numerical derivative tracing paths
- Plot side-by-side spot diagrams and print RMS metrics
- Add the example to the examples index and representative test subset
- Update the maintenance log
```

### 2026-05-17 - Document Analytical And Numerical Derivatives

Goal:

- Make the new analytical/numerical derivative behavior part of the main user
  documentation, not only an implementation detail.

Files changed:

- `docs/manual/surfaces.md`
- `docs/manual/api_quick_reference.md`
- `docs/examples.md`
- `docs/maintenance_log.md`

Changes:

- Added a dedicated section in the surfaces manual explaining:
  - why KrakenOS uses surface derivatives;
  - when analytical derivatives are used;
  - when numerical finite-difference fallback is preserved;
  - how combined sag terms also combine derivative terms.
- Documented supported analytical derivative terms:
  - planes;
  - conic/spherical/parabolic surfaces;
  - polynomial aspheres;
  - Zernike sag terms;
  - axicons away from the singular apex.
- Documented unsupported/fallback cases:
  - existing `ExtraData = [f, coef]`;
  - sampled `Error_map`;
  - singular points where an analytical derivative is not well defined.
- Added the optional user-defined derivative form:
  `ExtraData = [f, coef, df]`.
- Updated the API quick reference with derivative behavior.
- Added task-oriented entries in the example guide for:
  - `Examp_ExtraShape_With_Derivative.py`;
  - `Examp_ParaboleMirror_Derivative_Comparison.py`.

Verification:

```powershell
Select-String -Path docs\manual\surfaces.md -Pattern "Analytical and Numerical Surface Derivatives" -Context 0,55
Select-String -Path docs\manual\api_quick_reference.md -Pattern "Surface derivative behavior" -Context 0,20
Select-String -Path docs\examples.md -Pattern "derivative" -Context 1,2
```

Result:

- The derivative behavior is now documented in the main surfaces manual, API
  quick reference, and example guide.

Suggested commit:

```text
Document analytical and numerical derivatives
```

```text
- Explain analytical and numerical derivative behavior in the surfaces manual
- Document supported analytical derivative surface terms and fallback cases
- Add ExtraData derivative syntax to the API quick reference
- Link derivative examples from the example guide
- Update the maintenance log
```

### 2026-05-17 - Clarify Parabolic Mirror Numerical Floor

Goal:

- Make the parabolic mirror comparison easier to interpret by showing that the
  remaining spot is a floating-point numerical floor, not a physical aberration.

Files changed:

- `KrakenOS/Examples/Examp_ParaboleMirror_Derivative_Comparison.py`
- `docs/manual/surfaces.md`
- `docs/maintenance_log.md`

Changes:

- Updated the parabolic mirror derivative comparison example to plot residual
  spot coordinates with the centroid removed.
- Changed the plot scale to femtometers so the near-perfect analytical result
  is labeled honestly.
- Printed RMS and maximum radius in both millimeters and femtometers.
- Added an explicit note explaining that visible banding at this scale is a
  floating-point numerical floor.
- Added the same interpretation note to the surfaces manual.

Verification:

```powershell
python -m py_compile KrakenOS\Examples\Examp_ParaboleMirror_Derivative_Comparison.py
$env:MPLBACKEND = "Agg"; python KrakenOS\Examples\Examp_ParaboleMirror_Derivative_Comparison.py
```

Expected result:

- The example should run successfully.
- The analytical case should remain around `5e-14 mm` RMS.
- The plot should show centered residuals in femtometers, making the numerical
  floor explicit.

Suggested commit:

```text
Clarify parabolic mirror numerical floor
```

```text
- Plot parabolic mirror residual spots in femtometers
- Print RMS and maximum spot radius in mm and fm
- Explain that visible banding is a floating-point numerical floor
- Document the interpretation in the surfaces manual
- Update the maintenance log
```
