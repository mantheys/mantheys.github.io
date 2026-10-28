#!/usr/bin/env python3
"""Render _data/*.yml into an Awesome-CV LaTeX document and compile it.

  python3 tools/build_cv.py              # public CV -> assets/cv.pdf
  python3 tools/build_cv.py --private    # adds home address and phone number
  python3 tools/build_cv.py --no-pdf     # stop after writing cv/cv.tex
  python3 tools/build_cv.py --no-publications

The PDF lands at assets/cv.pdf, which is what `links.cv` in _config.yml points at,
so the website always serves the CV built from the same data it renders itself.

That file is published, so by default it carries no home address or phone number;
the header falls back to the institution. Pass --private to merge in
_data/private.yml (gitignored) and write cv-private.pdf instead, for applications.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import shutil
import subprocess
import sys

import jinja2
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
CVDIR = ROOT / "cv"

# Order matters: these become the \cvsection headings, in this sequence.
TALK_SECTIONS = [("Conferences", "conferences"), ("Schools", "schools")]


def _escape(text: str) -> str:
    """Escape LaTeX specials. Backslash first, or we escape our own escapes."""
    out = text.replace("\\", r"\textbackslash{}")
    for char in ("&", "%", "$", "#", "_"):
        out = out.replace(char, "\\" + char)
    return out.replace("~", r"\textasciitilde{}").replace("^", r"\textasciicircum{}")


# INSPIRE titles carry real LaTeX in both common spellings: "$\\pi^+$-Ar" and
# "\\(\\nu\\) cross-section". Escaping $, ^ or the backslash would print the markup
# instead of the symbol, so these spans are passed through untouched.
MATH_RE = re.compile(r"\$[^$]*\$|\\\(.*?\\\)")


def tex(text: object) -> str:
    """Escape LaTeX specials, leaving inline math from INSPIRE intact."""
    if text is None:
        return ""
    s = str(text)
    out, last = [], 0
    for m in MATH_RE.finditer(s):
        out.append(_escape(s[last:m.start()]))
        out.append(m.group(0))
        last = m.end()
    out.append(_escape(s[last:]))
    return "".join(out)


def md(text: object) -> str:
    """Escape, then re-expand the small Markdown subset the YAML uses.

    Supported: **bold** and [label](url). The \\LaTeX logo macro is deliberately
    not substituted -- its kerning collapses in awesome-cv's sans-serif skill rows,
    so the plain word reads better.
    """
    out = tex(text)
    out = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", out)
    out = re.sub(r"\[(.+?)\]\((.+?)\)", r"\\href{\2}{\1}", out)
    return out


def authors(pub: dict) -> str:
    """Author line, with your own name bolded and a trailing italic et al."""
    rendered = []
    for name in pub["authors"]:
        escaped = tex(name)
        if "Manthey" in name:
            escaped = r"\textbf{" + escaped + "}"
        rendered.append(escaped)
    line = "; ".join(rendered)
    return line + (r" \emph{et al.}" if pub.get("et_al") else "")


def venue(pub: dict) -> str:
    """The journal/volume/pages tail after a title, or 'in preparation'."""
    if not pub.get("journal"):
        return r", \emph{preprint}" + (f", {pub['year']}" if pub.get("year") else "")
    bits = [r", \emph{" + tex(pub["journal"]) + "}"]
    if pub.get("volume"):
        bits.append(f" {tex(pub['volume'])}")
    if pub.get("number"):
        bits.append(f"({tex(pub['number'])})")
    if pub.get("pages"):
        bits.append(f", {tex(pub['pages'])}")
    if pub.get("year"):
        bits.append(f", {pub['year']}")
    return "".join(bits) + "."


def publink(pub: dict) -> str:
    """Prefer a DOI, fall back to arXiv, then to the INSPIRE record."""
    if pub.get("doi"):
        return rf"\href{{https://doi.org/{pub['doi']}}}{{doi:{tex(pub['doi'])}}}"
    if pub.get("arxiv"):
        return rf"\href{{https://arxiv.org/abs/{pub['arxiv']}}}{{arXiv:{pub['arxiv']}}}"
    return rf"\href{{https://inspirehep.net/literature/{pub['recid']}}}{{INSPIRE}}"


def load(name: str) -> object:
    path = ROOT / "_data" / f"{name}.yml"
    if not path.exists():
        return None
    return yaml.safe_load(path.read_text())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-pdf", action="store_true", help="write cv/cv.tex only")
    ap.add_argument("--private", action="store_true",
                    help="merge _data/private.yml (address, phone) and write "
                         "cv-private.pdf instead of assets/cv.pdf")
    ap.add_argument("--no-publications", action="store_true",
                    help="omit the INSPIRE publication section")
    args = ap.parse_args()

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(CVDIR / "templates"),
        # LaTeX uses {} and % heavily, so move Jinja out of the way entirely.
        block_start_string="<%", block_end_string="%>",
        variable_start_string="<<", variable_end_string=">>",
        comment_start_string="<#", comment_end_string="#>",
        trim_blocks=True, lstrip_blocks=True, keep_trailing_newline=True,
        undefined=jinja2.StrictUndefined,
    )
    env.filters.update(tex=tex, md=md, authors=authors, venue=venue, publink=publink)

    talks = load("talks") or []
    talk_sections = [
        (heading, [t for t in talks if t.get("section") == key])
        for heading, key in TALK_SECTIONS
    ]
    talk_sections = [(h, g) for h, g in talk_sections if g]

    profile = load("profile")
    if args.private:
        private = load("private")
        if not private:
            print("error: --private needs _data/private.yml "
                  "(copy _data/private.example.yml)", file=sys.stderr)
            return 1
        profile = {**profile, **private}

    pubs = None if args.no_publications else load("publications")
    if pubs is None and not args.no_publications:
        print("note: _data/publications.yml missing -- run tools/fetch_inspire.py first")

    rendered = env.get_template("cv.tex.j2").render(
        profile=profile,
        education=load("education"),
        experience=load("experience"),
        skills=load("skills"),
        research=load("research"),
        talk_sections=talk_sections,
        publications=pubs,
    )

    tex_path = CVDIR / "cv.tex"
    tex_path.write_text(rendered)
    print(f"wrote {tex_path.relative_to(ROOT)}")
    if args.no_pdf:
        return 0

    if shutil.which("xelatex") is None:
        print("error: xelatex not found on PATH", file=sys.stderr)
        return 1

    # Twice, so the footer page numbers settle.
    for run in (1, 2):
        proc = subprocess.run(
            ["xelatex", "-interaction=nonstopmode", "-halt-on-error", "cv.tex"],
            cwd=CVDIR, capture_output=True, text=True,
        )
        if proc.returncode != 0:
            sys.stderr.write(proc.stdout[-4000:])
            print(f"error: xelatex failed on run {run}", file=sys.stderr)
            return 1

    # The private build never lands in assets/ -- that directory is published.
    dest = ROOT / ("cv-private.pdf" if args.private else "assets/cv.pdf")
    shutil.copy(CVDIR / "cv.pdf", dest)
    print(f"wrote {dest.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
