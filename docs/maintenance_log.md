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
