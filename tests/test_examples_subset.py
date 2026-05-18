import runpy
from pathlib import Path


REPORT = Path(__file__).with_name("test_examples_subset_report.txt")
EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "KrakenOS" / "Examples"

EXAMPLES = [
    "Examp_Doublet_Lens_Cylinder.py",
    "Examp_Doublet_Lens_NonSec.py",
    "Examp_Doublet_Lens_Tilt_non_sec.py",
    "Examp_ExtraShape_With_Derivative.py",
    "Examp_ExtraShape_XY_Cosines_UDA.py",
    "Examp_ParaboleMirror_Derivative_Comparison.py",
    "Examp_Tel_2M_Spyder_Spot_Diagram.py",
    "Examp_Prism_STL.py",
]


def write_report(lines):
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_example(path):
    runpy.run_path(str(path), run_name="__main__")


def main():
    lines = []

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import pyvista as pv

    original_plt_show = plt.show
    original_pv_show = pv.Plotter.show
    plt.show = lambda *args, **kwargs: None
    pv.Plotter.show = lambda self, *args, **kwargs: None

    try:
        for example in EXAMPLES:
            path = EXAMPLES_DIR / example
            assert path.exists(), f"Missing example: {path}"

            run_example(path)
            lines.append(f"PASS {example}")

        lines.append("RESULT PASS")
        write_report(lines)
        return 0

    except Exception as exc:
        lines.append(f"RESULT FAIL: {type(exc).__name__}: {exc}")
        write_report(lines)
        raise

    finally:
        plt.show = original_plt_show
        pv.Plotter.show = original_pv_show


def test_representative_examples_run():
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
