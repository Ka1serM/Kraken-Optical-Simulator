from pathlib import Path


REPORT = Path(__file__).with_name("test_build_modes_report.txt")


def write_report(lines):
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_lens_system(Kos, build):
    obj = Kos.surf()
    obj.Glass = "AIR"
    obj.Thickness = 10
    obj.Diameter = 30

    lens_front = Kos.surf()
    lens_front.Rc = 80
    lens_front.Glass = "BK7"
    lens_front.Thickness = 5
    lens_front.Diameter = 30

    lens_back = Kos.surf()
    lens_back.Rc = -80
    lens_back.Glass = "AIR"
    lens_back.Thickness = 20
    lens_back.Diameter = 30

    image = Kos.surf()
    image.Glass = "AIR"
    image.Thickness = 0
    image.Diameter = 30

    return Kos.system([obj, lens_front, lens_back, image], Kos.Setup(), build=build)


def main():
    lines = []

    try:
        import KrakenOS as Kos

        system = build_lens_system(Kos, build=0)
        lines.append("PASS create system with build=0")
        lines.append(
            f"INFO before NsTrace: ExistSolid={system.Pr3D.ExistSolid}, "
            f"BBB={system.BBB.n_blocks}, EEE={system.EEE.n_blocks}"
        )

        assert system.Pr3D.ExistSolid == 0
        assert system.BBB.n_blocks == 0
        assert system.EEE.n_blocks == len(system.SDT)
        lines.append("PASS build=0 starts without side meshes")

        system.NsTrace([12, 0, 0], [0, 0, 1], 0.55)
        lines.append(
            f"INFO after NsTrace: ExistSolid={system.Pr3D.ExistSolid}, "
            f"BBB={system.BBB.n_blocks}, EEE={system.EEE.n_blocks}"
        )

        assert system.Pr3D.ExistSolid == 1
        assert system.BBB.n_blocks > 0
        assert system.EEE.n_blocks > len(system.SDT)
        lines.append("PASS NsTrace rebuilds side meshes from build=0")

        lines.append("RESULT PASS")
        write_report(lines)
        return 0

    except Exception as exc:
        lines.append(f"RESULT FAIL: {type(exc).__name__}: {exc}")
        write_report(lines)
        raise


def test_build_zero_rebuilds_nonsequential_meshes():
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
