#!/usr/bin/env python3
"""Pull the publication record from INSPIRE-HEP and write it out twice:

  assets/ref.bib          BibTeX for jekyll-scholar (the website Publications page)
  _data/publications.yml  structured list for the CV PDF build

The INSPIRE author identifier lives in _data/profile.yml (`inspire_bai`), so this
script needs no arguments. Run it by hand, or let the weekly GitHub Action do it.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
import urllib.parse
import urllib.request

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
API = "https://inspirehep.net/api/literature"

# Papers with at most this many authors are flagged `selected` -- they are the ones
# where you are a visible author rather than one line of a collaboration list.
# They get a `selected = {true}` BibTeX field (the site can feature them) and land
# in the `selected` bucket of publications.yml, which is what the CV PDF prints.
SELECTED_MAX_AUTHORS = 150

# In the `selected` list, print at most this many names before falling back to
# "et al." -- your own name is always kept in the printed head.
SELECTED_MAX_LISTED = 12

# Your surname, used to bold your name and to keep it inside a truncated list.
SURNAME = "Manthey"

FIELDS = (
    "titles,authors,collaborations,publication_info,arxiv_eprints,dois,"
    "document_type,earliest_date,texkeys,report_numbers"
)


def fetch(bai: str) -> list[dict]:
    """Return every INSPIRE literature record for this author, newest first."""
    records, page = [], 1
    while True:
        qs = urllib.parse.urlencode(
            {
                "q": f"a {bai}",
                "sort": "mostrecent",
                "size": 250,
                "page": page,
                "fields": FIELDS,
            }
        )
        with urllib.request.urlopen(f"{API}?{qs}", timeout=60) as fh:
            payload = json.load(fh)
        hits = payload["hits"]["hits"]
        records.extend(hits)
        if len(records) >= payload["hits"]["total"] or not hits:
            break
        page += 1
    return records


def initials(full_name: str) -> str:
    """'Manthey Corchado, Sergio' -> 'S. Manthey Corchado'."""
    if "," not in full_name:
        return full_name
    last, first = (part.strip() for part in full_name.split(",", 1))
    given = " ".join(f"{word[0]}." for word in first.split() if word)
    return f"{given} {last}".strip()


def tex_escape(text: str) -> str:
    """Escape the characters that actually show up in INSPIRE titles."""
    for char in ("&", "%", "#", "_"):
        text = text.replace(char, "\\" + char)
    return text


def clean_title(text: str) -> str:
    """Strip the MathML INSPIRE sometimes embeds in titles.

    Keeping only the leaf text turns
    ``<math><msup><mi>\u03c0</mi><mo>+</mo></msup></math>`` into ``\u03c0+``, which is
    what you want in both a BibTeX file and a LaTeX CV.
    """
    if "<" not in text:
        return text
    text = re.sub(r"<mo>\s*</mo>", " ", text)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", text).strip()


def parse(record: dict) -> dict:
    """Flatten one INSPIRE record into the shape both outputs consume."""
    meta = record["metadata"]
    authors = meta.get("authors", [])
    collaborations = [c["value"] for c in meta.get("collaborations", [])]
    info = (meta.get("publication_info") or [{}])[0]

    journal = info.get("journal_title")
    doi = (meta.get("dois") or [{}])[0].get("value")
    eprint = (meta.get("arxiv_eprints") or [{}])[0].get("value")
    date = meta.get("earliest_date", "")

    selected = len(authors) <= SELECTED_MAX_AUTHORS
    names = [initials(a["full_name"]) for a in authors]
    et_al = False

    if not selected:
        # A paper you appear on as one of ~1400 collaborators: credit the
        # collaboration, or the lead author, rather than printing the roster.
        if collaborations:
            author_list = [f"{collaborations[0]} Collaboration"]
        else:
            author_list, et_al = names[:1], True
    elif len(names) > SELECTED_MAX_LISTED:
        author_list, et_al = names[:SELECTED_MAX_LISTED], True
        if not any(SURNAME in n for n in author_list):
            # Truncating must never hide you from your own CV.
            mine = [n for n in names if SURNAME in n]
            author_list = names[: SELECTED_MAX_LISTED - len(mine)] + mine
    else:
        author_list = names

    doc_type = (meta.get("document_type") or ["article"])[0]
    if not journal:
        bibtype = "unpublished"
    elif doc_type == "conference paper":
        bibtype = "inproceedings"
    else:
        bibtype = "article"

    key = (meta.get("texkeys") or [f"inspire{record['id']}"])[0]

    return {
        "key": re.sub(r"[^A-Za-z0-9:_-]", "", key),
        "recid": record["id"],
        "bibtype": bibtype,
        "title": clean_title(meta["titles"][0]["title"]),
        "authors": author_list,
        "et_al": et_al,
        "n_authors": len(authors),
        "collaboration": collaborations[0] if collaborations else None,
        "journal": journal,
        "volume": info.get("journal_volume"),
        "number": info.get("journal_issue"),
        "pages": info.get("page_start"),
        "year": info.get("year") or (date[:4] if date else None),
        "date": date,
        "doi": doi,
        "arxiv": eprint,
        "selected": selected,
    }


def to_bibtex(pub: dict) -> str:
    """Render one entry for jekyll-scholar."""
    fields: list[tuple[str, str]] = [
        ("title", "{" + tex_escape(pub["title"]) + "}"),
        ("author", tex_escape(" and ".join(pub["authors"]))
                   + (" and others" if pub["et_al"] else "")),
    ]
    if pub["collaboration"]:
        fields.append(("collaboration", pub["collaboration"]))
    for name, key in (
        ("journal", "journal"),
        ("volume", "volume"),
        ("number", "number"),
        ("pages", "pages"),
        ("year", "year"),
        ("doi", "doi"),
    ):
        if pub[key]:
            fields.append((name, str(pub[key])))
    if pub["arxiv"]:
        fields.append(("arxiv", pub["arxiv"]))
        fields.append(("note", f"arXiv:{pub['arxiv']}"))
    fields.append(("url", f"https://inspirehep.net/literature/{pub['recid']}"))
    if pub["selected"]:
        fields.append(("selected", "true"))

    body = ",\n".join(f"  {k} = {{{v}}}" if not v.startswith("{") else f"  {k} = {v}"
                      for k, v in fields)
    return f"@{pub['bibtype']}{{{pub['key']},\n{body},\n}}\n"


def main() -> int:
    profile = yaml.safe_load((ROOT / "_data" / "profile.yml").read_text())
    bai = profile.get("inspire_bai")
    if not bai:
        print("error: set `inspire_bai` in _data/profile.yml", file=sys.stderr)
        return 1

    print(f"querying INSPIRE for author {bai} ...")
    pubs = [parse(r) for r in fetch(bai)]
    pubs.sort(key=lambda p: p["date"] or "", reverse=True)

    bib = ROOT / "assets" / "ref.bib"
    bib.write_text(
        "% Generated by tools/fetch_inspire.py -- do not edit by hand.\n"
        f"% Source: https://inspirehep.net/authors?q={bai}\n\n"
        + "\n".join(to_bibtex(p) for p in pubs)
    )

    selected = [p for p in pubs if p["selected"]]
    collaboration = [p for p in pubs if not p["selected"]]
    out = ROOT / "_data" / "publications.yml"
    out.write_text(
        "# Generated by tools/fetch_inspire.py -- do not edit by hand.\n"
        + yaml.safe_dump(
            {"selected": selected, "collaboration": collaboration},
            sort_keys=False,
            allow_unicode=True,
            width=100,
        )
    )

    print(f"  {len(pubs)} records -> {bib.relative_to(ROOT)}")
    print(f"  {len(selected)} selected / {len(collaboration)} collaboration "
          f"-> {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
