#!/usr/bin/env python3
"""Generate a Markdown manual from KrakenOS example scripts.

The generator reads `KrakenOS/Examples/EXAMPLES_INDEX.md`, extracts the module
docstring from each listed example, and writes `docs/examples_manual.md`.

It intentionally does not execute examples. Many KrakenOS examples open 3D
viewers, use large datasets, or depend on an interactive plotting backend. Image
capture can be added later example by example under `docs/assets/examples/`.
"""

from __future__ import annotations

import ast
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = REPO_ROOT / "KrakenOS" / "Examples"
INDEX_PATH = EXAMPLES_DIR / "EXAMPLES_INDEX.md"
OUTPUT_PATH = REPO_ROOT / "docs" / "examples_manual.md"
ASSET_DIR = REPO_ROOT / "docs" / "assets" / "examples"

IMAGE_CAPTIONS = {
    "Examp_Ray_2d.png": (
        "2D layout of a single ray traced through a cemented doublet. The green "
        "line shows the ray path, while the black profiles show the optical "
        "surfaces and the image plane."
    ),
    "Examp_Doublet_Lens_Pupil.png": (
        "Pupil sampling result copied from the example output. It gives a quick "
        "visual check of the sampled pupil coordinates used for the ray bundle."
    ),
    "Examp_Doublet_Lens_Pupil_2d.png": (
        "2D ray fan generated from the pupil sampler. The figure shows how the "
        "bundle fills the entrance pupil and converges toward the image plane."
    ),
    "Examp_Doublet_Lens_Pupil_3d.png": (
        "Static 3D rendering of the same pupil bundle. This view is useful for "
        "checking that the traced rays and lens geometry are spatially coherent."
    ),
    "Examp_PSF_MTF_From_Zernike_2d.png": (
        "Point-spread function and MTF profiles computed from a small set of "
        "Zernike coefficients. The image connects wavefront terms with image "
        "quality metrics."
    ),
    "Examp_Coating_Energy_Basics_2d.png": (
        "Coating lookup example showing reflected and transmitted energy terms "
        "for two incidence-angle samples. It illustrates how RP, RS, TP, and TS "
        "are interpreted."
    ),
    "Examp_Lens_Catalog_Basics_2d.png": (
        "2D layout generated from a Zemax-style THORLABS catalog entry. The "
        "figure confirms that catalog surfaces can be converted into KrakenOS "
        "surfaces and traced like ordinary systems."
    ),
    "Examp_Dispersion_By_AbbeNumber_2d.png": (
        "Chromatic 2D ray trace through the doublet at three wavelengths. The "
        "separation of the colored bundles illustrates how material dispersion "
        "appears in a traced system."
    ),
    "Examp_RMS_BestFocus_2d.png": (
        "Best-focus diagnostic plot. The left panel shows RMS radius as the "
        "image plane is shifted, and the right panel compares nominal and "
        "best-focus spot coordinates."
    ),
    "Examp_Reverse_Trace_2d.png": (
        "Forward and reverse ray paths through the same doublet. This image "
        "helps verify that `RvTrace` walks the optical path back from image "
        "space toward object space."
    ),
    "Examp_Perfect_lens_2d.png": (
        "2D layout of an ideal thin-lens system. The simplified surfaces make "
        "it easier to see thin-lens behavior before using real refractive "
        "curvatures and glass data."
    ),
    "Examp_Perfect_lens_plot.png": (
        "Image-plane hit coordinates from the ideal-lens example. This plot "
        "separates the spot result from the optical layout."
    ),
    "Examp_Perfect_lens_Telescope_2d.png": (
        "Ideal telescope layout generated from objective and eyepiece thin "
        "lenses. The traced field fans show the simplified telescope geometry."
    ),
    "Examp_Refraction_Prism_2d.png": (
        "Prism-only refraction trace at multiple wavelengths. The tilted flat "
        "faces bend the ray bundle and make the chromatic angular separation "
        "visible."
    ),
    "Examp_Flat_Mirror_45Deg_2d.png": (
        "Folded optical path after a 45 degree mirror. The layout is useful for "
        "checking mirror orientation, reflection direction, and coordinate "
        "sign conventions."
    ),
    "Examp_Glass_Catalog_Order_2d.png": (
        "Catalog-priority chart for a duplicated glass name. The first matching "
        "catalog in the ordered list is the one KrakenOS will use by default."
    ),
    "Examp_Metal_Mirror_Energy_2d.png": (
        "Energy comparison for aluminum and gold mirror data. The bars summarize "
        "average reflection and total transmission terms stored after tracing."
    ),
    "Examp_SurfBlock_Basics_2d.png": (
        "Relay assembled from two reusable catalog lens blocks. The figure shows "
        "how `SurfBlock` and `alignment` expand named components into ordinary "
        "surfaces for tracing."
    ),
}


@dataclass
class Example:
    file_name: str
    level: str
    topic: str
    description: str
    required_files: str
    docstring: str

    @property
    def code_link(self) -> str:
        return f"../KrakenOS/Examples/{quote_link_path(self.file_name)}"

    @property
    def anchor(self) -> str:
        base = self.file_name.lower().replace(".py", "")
        base = re.sub(r"[^a-z0-9]+", "-", base).strip("-")
        return base

    @property
    def image_file_name(self) -> str:
        return self.file_name.replace(".py", ".png")

    @property
    def image_path(self) -> Path:
        return ASSET_DIR / self.image_file_name

    def image_candidates(self) -> list[Path]:
        stem = self.file_name.replace(".py", "")
        names = [
            f"{stem}.png",
            f"{stem}_2d.png",
            f"{stem}_3d.png",
            f"{stem}_plot.png",
        ]
        return [ASSET_DIR / name for name in names if (ASSET_DIR / name).exists()]


def quote_link_path(path: str) -> str:
    return (
        path.replace(" ", "%20")
        .replace("(", "%28")
        .replace(")", "%29")
        .replace(",", "%2C")
        .replace("#", "%23")
    )


def parse_index() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in INDEX_PATH.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `Examp_"):
            continue
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) != 5:
            continue
        file_name = parts[0].strip("`")
        rows.append(
            {
                "file_name": file_name,
                "level": parts[1],
                "topic": parts[2],
                "description": parts[3],
                "required_files": parts[4],
            }
        )
    return rows


def read_docstring(file_name: str) -> str:
    source_path = EXAMPLES_DIR / file_name
    try:
        tree = ast.parse(source_path.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        tree = ast.parse(source_path.read_text(encoding="latin-1"))
    return ast.get_docstring(tree) or ""


def load_examples() -> list[Example]:
    examples = []
    for row in parse_index():
        examples.append(
            Example(
                file_name=row["file_name"],
                level=row["level"],
                topic=row["topic"],
                description=row["description"],
                required_files=row["required_files"],
                docstring=read_docstring(row["file_name"]),
            )
        )
    return examples


def first_paragraph(docstring: str, fallback: str) -> str:
    if not docstring:
        return fallback
    paragraphs = [part.strip() for part in docstring.split("\n\n") if part.strip()]
    if len(paragraphs) == 1:
        return paragraphs[0]
    title = paragraphs[0]
    body = paragraphs[1]
    if title.lower().startswith("example:"):
        return body
    return f"{title}\n\n{body}"


def extract_section(docstring: str, heading: str) -> list[str]:
    lines = docstring.splitlines()
    capture = False
    result: list[str] = []
    known_headings = {
        "what this example teaches:",
        "key ideas:",
        "expected output:",
        "didactic note:",
        "units:",
        "required packaged files:",
    }

    for line in lines:
        normalized = line.strip().lower()
        if normalized == heading.lower():
            capture = True
            continue
        if capture and normalized in known_headings:
            break
        if capture:
            result.append(line.rstrip())

    return [line for line in result if line.strip()]


def render_bullets(lines: list[str]) -> list[str]:
    if not lines:
        return []
    rendered = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- "):
            rendered.append(stripped)
        elif rendered:
            rendered[-1] = f"{rendered[-1]} {stripped}"
        else:
            rendered.append(f"- {stripped}")
    return rendered


def image_kind(image_name: str) -> str:
    if image_name.endswith("_3d.png"):
        return "3D"
    if image_name.endswith("_plot.png"):
        return "Plot"
    if image_name.endswith("_2d.png"):
        return "2D"
    return "Image"


def render_illustrated_examples(examples: list[Example]) -> list[str]:
    illustrated = [example for example in examples if example.image_candidates()]
    if not illustrated:
        return []

    lines = [
        "## Illustrated Examples",
        "",
        "These examples currently include generated or curated figures. Use this",
        "table as the fastest visual entry point into the manual.",
        "",
        "| Example | Topic | Figures | Visual focus |",
        "| --- | --- | --- | --- |",
    ]

    for example in sorted(illustrated, key=lambda item: (item.topic, item.file_name)):
        images = example.image_candidates()
        figure_links = []
        captions = []
        for image in images:
            image_name = image.name
            image_link = f"assets/examples/{quote_link_path(image_name)}"
            figure_links.append(f"[{image_kind(image_name)}]({image_link})")
            caption = IMAGE_CAPTIONS.get(image_name)
            if caption:
                captions.append(caption)
        focus = captions[0] if captions else example.description
        lines.append(
            f"| [`{example.file_name}`](#{example.anchor}) | {example.topic} | "
            f"{', '.join(figure_links)} | {focus} |"
        )

    lines.append("")
    return lines


def render_manual(examples: list[Example]) -> str:
    by_topic: dict[str, list[Example]] = defaultdict(list)
    for example in examples:
        by_topic[example.topic].append(example)

    lines: list[str] = [
        "# KrakenOS Generated Examples Manual",
        "",
        "This is the generated visual appendix for the main",
        "[KrakenOS User Manual](user_manual/README.md). It is generated from the",
        "example scripts in `KrakenOS/Examples`. Each section links back to the",
        "runnable Python file and summarizes the didactic notes written in the",
        "example docstrings.",
        "",
        "Generated with:",
        "",
        "```bash",
        "python tools/generate_examples_manual.py",
        "```",
        "",
        "Images are loaded from `docs/assets/examples/` when available. They can",
        "be created with `python tools/generate_example_images.py --all` or added",
        "manually with names such as `Examp_Ray_2d.png` and `Examp_Ray_3d.png`.",
        "",
    ]

    lines.extend(render_illustrated_examples(examples))
    lines.extend(["## Quick Index", ""])

    for topic in sorted(by_topic):
        lines.append(f"- [{topic}](#{quote_anchor(topic)})")
    lines.append("")

    for topic in sorted(by_topic):
        lines.extend([f"## {topic}", ""])
        topic_examples = sorted(by_topic[topic], key=lambda item: (item.level, item.file_name))

        lines.extend(["| Example | Level | Summary | Required files |", "| --- | --- | --- | --- |"])
        for example in topic_examples:
            lines.append(
                f"| [`{example.file_name}`](#{example.anchor}) | "
                f"{example.level} | {example.description} | {example.required_files} |"
            )
        lines.append("")

        for example in topic_examples:
            lines.extend(
                [
                    f"### {example.file_name}",
                    "",
                    f"- **Level:** {example.level}",
                    f"- **Topic:** {example.topic}",
                    f"- **Required files:** {example.required_files}",
                    f"- **Source:** [`{example.file_name}`]({example.code_link})",
                    "",
                    first_paragraph(example.docstring, example.description),
                    "",
                ]
            )

            teaches = extract_section(example.docstring, "What this example teaches:")
            if not teaches:
                teaches = extract_section(example.docstring, "Key ideas:")
            expected = extract_section(example.docstring, "Expected output:")
            didactic = extract_section(example.docstring, "Didactic note:")
            units = extract_section(example.docstring, "Units:")

            if teaches:
                lines.extend(["**What You Learn**", ""])
                lines.extend(render_bullets(teaches))
                lines.append("")
            if expected:
                lines.extend(["**Expected Output**", ""])
                lines.extend(render_bullets(expected))
                lines.append("")
            if didactic:
                lines.extend(["**Didactic Notes**", ""])
                lines.extend(render_bullets(didactic))
                lines.append("")
            if units:
                lines.extend(["**Units**", ""])
                lines.extend(render_bullets(units))
                lines.append("")

            lines.extend(
                [
                    "**Run**",
                    "",
                    "```bash",
                    f"python KrakenOS/Examples/{shell_path(example.file_name)}",
                    "```",
                    "",
                ]
            )

            images = example.image_candidates()
            if images:
                lines.extend(
                    [
                        "**Example Images**",
                        "",
                    ]
                )
                for image in images:
                    image_name = image.name
                    image_link = f"assets/examples/{quote_link_path(image_name)}"
                    lines.append(f"![{image_name}]({image_link})")
                    caption = IMAGE_CAPTIONS.get(image_name)
                    if caption:
                        lines.append("")
                        lines.append(f"*{caption}*")
                    lines.append("")
            else:
                lines.extend(
                    [
                        "<!-- Optional image placeholder:",
                        f"Add docs/assets/examples/{example.file_name.replace('.py', '')}_2d.png",
                        f"or docs/assets/examples/{example.file_name.replace('.py', '')}_3d.png",
                        "to show images here.",
                        "-->",
                        "",
                    ]
                )

    return "\n".join(lines).rstrip() + "\n"


def quote_anchor(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def shell_path(path: str) -> str:
    if any(char in path for char in " ()#,"):
        return f'"{path}"'
    return path


def main() -> int:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    manual = render_manual(load_examples())
    OUTPUT_PATH.write_text(manual, encoding="utf-8", newline="\n")
    keep = ASSET_DIR / ".gitkeep"
    if not keep.exists():
        keep.write_text("", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
