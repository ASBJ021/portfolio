#!/usr/bin/env python3
"""Convert the resume PDF into a normalized plain-text file."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple
import xml.etree.ElementTree as ET

try:  # Prefer pypdf/PyPDF2 when installed
    from pypdf import PdfReader as _PdfReader  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    try:
        from PyPDF2 import PdfReader as _PdfReader  # type: ignore
    except ModuleNotFoundError:  # pragma: no cover - optional dependency
        _PdfReader = None  # type: ignore


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="Extract text from the resume PDF into parsed_resume.txt"
    )
    parser.add_argument(
        "-i",
        "--input",
        default=root / "assets/resume/CV__Akashkumar_Jain.pdf",
        type=Path,
        help="Path to the resume PDF (default: assets/resume/CV__Akashkumar_Jain.pdf)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=root / "parsed_resume.txt",
        type=Path,
        help="Destination text file (default: parsed_resume.txt in repo root)",
    )
    parser.add_argument(
        "--gs",
        default="gs",
        help="Ghostscript executable to use (default: %(default)s)",
    )
    parser.add_argument(
        "--line-tol",
        type=float,
        default=2.0,
        help="Y-axis tolerance (in PDF units) when grouping characters into lines.",
    )
    parser.add_argument(
        "--space-factor",
        type=float,
        default=0.2,
        help="Multiplier applied to the mean glyph width to decide when to insert spaces.",
    )
    return parser.parse_args()


def run_ghostscript(
    gs_bin: str, pdf_path: Path, structured_out: Path
) -> None:
    cmd = [
        gs_bin,
        "-dBATCH",
        "-dNOPAUSE",
        "-sDEVICE=txtwrite",
        "-dTextFormat=0",
        f"-sOutputFile={structured_out}",
        str(pdf_path),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except FileNotFoundError as exc:
        raise SystemExit(
            f"Ghostscript executable '{gs_bin}' was not found on PATH."
        ) from exc
    except subprocess.CalledProcessError as exc:
        msg = exc.stderr or exc.stdout or str(exc)
        raise SystemExit(f"Ghostscript failed:\n{msg}") from exc


def _wrap_xml(raw: str) -> str:
    return "<document>\n" + raw + "\n</document>"


def extract_with_pdfreader(pdf_path: Path) -> Optional[str]:
    """Use PyPDF2/pypdf if available for higher-fidelity text extraction."""
    if _PdfReader is None:
        return None
    reader = _PdfReader(str(pdf_path))
    lines: List[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text:
            lines.extend(text.splitlines())
        lines.append("")  # preserve page gaps
    return normalize_lines(lines)


def load_chars(xml_path: Path) -> List[Tuple[int, float, float, float, str]]:
    """Return a list of tuples (page, y0, x0, x1, character)."""
    raw = xml_path.read_text(encoding="utf-8", errors="ignore")
    wrapped = _wrap_xml(raw)
    root = ET.fromstring(wrapped)
    chars: List[Tuple[int, float, float, float, str]] = []
    for page_idx, page in enumerate(root.findall("page")):
        for span in page.findall("span"):
            for ch in span.findall("char"):
                glyph = ch.attrib.get("c", "")
                if not glyph:
                    continue
                bbox = ch.attrib.get("bbox")
                if not bbox:
                    continue
                try:
                    x0, y0, x1, y1 = (float(v) for v in bbox.split())
                except ValueError:
                    continue
                chars.append((page_idx, y0, x0, x1, glyph))
    return chars


def group_lines(
    chars: Sequence[Tuple[int, float, float, float, str]], line_tol: float
) -> List[List[Tuple[float, float, float, str]]]:
    """Group characters into lines based on Y proximity."""
    if not chars:
        return []
    chars_sorted = sorted(chars, key=lambda item: (item[0], item[1], item[2]))
    lines: List[List[Tuple[float, float, float, str]]] = []
    current_line: List[Tuple[float, float, float, str]] = []
    current_page, current_y = chars_sorted[0][0], chars_sorted[0][1]
    for page_idx, y0, x0, x1, glyph in chars_sorted:
        if (
            page_idx != current_page
            or abs(y0 - current_y) > line_tol
        ):
            if current_line:
                lines.append(current_line)
            current_line = []
            current_page = page_idx
            current_y = y0
        current_line.append((x0, x1, y0, glyph))
    if current_line:
        lines.append(current_line)
    # Sort lines from top to bottom
    lines.sort(key=lambda line: line[0][2] if line else float("inf"))
    return lines


def collapse_line(
    line_chars: Sequence[Tuple[float, float, float, str]],
    space_factor: float,
) -> str:
    """Turn a line's characters into readable text with inferred spaces."""
    if not line_chars:
        return ""
    ordered = sorted(line_chars, key=lambda item: item[0])
    pieces: List[str] = []
    prev_x1: Optional[float] = None
    prev_width: Optional[float] = None
    widths = [x1 - x0 for x0, x1, *_ in ordered if x1 > x0]
    avg_width = sum(widths) / len(widths) if widths else 4.0
    min_gap = max(1.5, avg_width * space_factor)
    for x0, x1, _, glyph in ordered:
        if prev_x1 is not None:
            gap = x0 - prev_x1
            width_guard = prev_width * 0.45 if prev_width else 0.0
            if gap > max(min_gap, width_guard):
                pieces.append(" ")
        pieces.append(glyph)
        prev_x1 = x1
        prev_width = x1 - x0 if x1 > x0 else prev_width
    return "".join(pieces).rstrip()


def normalize_lines(lines: Iterable[str]) -> str:
    cleaned: List[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if cleaned and cleaned[-1]:
                cleaned.append("")
            continue
        cleaned.append(stripped)
    text = "\n".join(cleaned).rstrip()
    return text + ("\n" if text else "")


def main() -> None:
    args = parse_args()
    pdf_path = args.input.expanduser().resolve()
    out_path = args.output.expanduser().resolve()
    if not pdf_path.exists():
        raise SystemExit(f"Input PDF not found: {pdf_path}")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    text = extract_with_pdfreader(pdf_path)
    if text is None:
        with tempfile.TemporaryDirectory() as tmpdir:
            structured = Path(tmpdir) / "resume.xml"
            run_ghostscript(args.gs, pdf_path, structured)
            chars = load_chars(structured)

        if not chars:
            raise SystemExit("No text was extracted from the PDF.")

        lines = group_lines(chars, line_tol=args.line_tol)
        rendered = [collapse_line(line, args.space_factor) for line in lines]
        text = normalize_lines(rendered)

    with tempfile.TemporaryDirectory() as tmpdir:
        structured = Path(tmpdir) / "resume.xml"
        run_ghostscript(args.gs, pdf_path, structured)
        chars = load_chars(structured)

    out_path.write_text(text, encoding="utf-8")
    print(f"Wrote {out_path} ({len(text)} characters).")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nAborted.")
