from pathlib import Path
from importlib import resources


REPORT = Path(__file__).with_name("test_report.txt")


def write_report(lines):
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    lines = []

    try:
        import KrakenOS as Kos

        lines.append("PASS import KrakenOS")
        lines.append(f"INFO KrakenOS file: {Kos.__file__}")

        surface = Kos.surf()
        surface.Glass = "BK7"
        surface.Rc = 100
        surface.Diameter = 30

        assert surface.Glass == "BK7"
        assert surface.Rc == 100
        assert surface.Diameter == 30
        lines.append("PASS create and edit Kos.surf")

        config = Kos.Setup()
        first_catalog = Path(config.GlassCat[0]).name
        lines.append(f"INFO first catalog: {first_catalog}")
        assert first_catalog == "SCHOTT.AGF"
        lines.append("PASS default catalog priority uses SCHOTT.AGF first")

        package_root = Path(Kos.__file__).resolve().parent
        required_files = [
            package_root / "Cat" / "SCHOTT.AGF",
            package_root / "Cat" / "Gold.csv",
            package_root / "Examples" / "R1064_F1800.txt",
            package_root / "LensCat" / "THORLABS.ZMF",
            package_root / "AstroAtmosphere" / "__init__.py",
        ]

        for required_file in required_files:
            assert required_file.exists(), f"Missing required file: {required_file}"
            lines.append(f"PASS found data file: {required_file.relative_to(package_root)}")

        kraken_resources = resources.files("KrakenOS")
        gold_csv = kraken_resources / "Cat" / "Gold.csv"
        fresnel_profile = kraken_resources / "Examples" / "R1064_F1800.txt"
        thorlabs_catalog = kraken_resources / "LensCat" / "THORLABS.ZMF"
        zemax_lens = kraken_resources / "LensCat" / "zmax_84383.zmx"
        prism_stl = kraken_resources / "Examples" / "prism.stl"
        prisma_stl = kraken_resources / "Examples" / "Prisma.stl"
        assert gold_csv.exists(), f"Missing resource: {gold_csv}"
        assert fresnel_profile.exists(), f"Missing resource: {fresnel_profile}"
        assert thorlabs_catalog.exists(), f"Missing resource: {thorlabs_catalog}"
        assert zemax_lens.exists(), f"Missing resource: {zemax_lens}"
        assert prism_stl.exists(), f"Missing resource: {prism_stl}"
        assert prisma_stl.exists(), f"Missing resource: {prisma_stl}"
        lines.append("PASS importlib.resources finds Cat/Gold.csv")
        lines.append("PASS importlib.resources finds Examples/R1064_F1800.txt")
        lines.append("PASS importlib.resources finds LensCat/THORLABS.ZMF")
        lines.append("PASS importlib.resources finds LensCat/zmax_84383.zmx")
        lines.append("PASS importlib.resources finds Examples/prism.stl")
        lines.append("PASS importlib.resources finds Examples/Prisma.stl")

        lines.append("RESULT PASS")
        write_report(lines)
        return 0

    except Exception as exc:
        lines.append(f"RESULT FAIL: {type(exc).__name__}: {exc}")
        write_report(lines)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
