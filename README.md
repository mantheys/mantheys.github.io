# mantheys.github.io

Personal academic site and CV, both generated from one set of data files.

```
_data/*.yml  +  INSPIRE-HEP
     |
     +-- tools/fetch_inspire.py --> assets/ref.bib + _data/publications.yml
     |
     +-- tools/build_cv.py ------> cv/cv.tex --xelatex--> assets/cv.pdf
     |
     +-- Jekyll -----------------> the website
```

Nothing is written twice: the website and the PDF read the same YAML, and the
publication list on both comes from INSPIRE-HEP rather than being maintained by hand.

## Editing your CV

Edit the YAML in `_data/`, never `cv/cv.tex` (it is generated and gitignored):

| File | Drives |
| --- | --- |
| `profile.yml` | name, contact details, ORCID, INSPIRE author id |
| `education.yml` | Academic Education section + About page |
| `experience.yml` | Responsibilities and Positions + About page |
| `skills.yml` | Technical skills and languages + About page |
| `talks.yml` | Conferences and Schools sections + Talks page |
| `research.yml` | Research Activities section + Research page |
| `publications.yml` | **generated** — do not edit |

A small Markdown subset works inside the YAML strings and survives into LaTeX:
`**bold**` and `[label](url)`.

Then rebuild:

```sh
pip install -r tools/requirements.txt
python3 tools/build_cv.py          # -> assets/cv.pdf
python3 tools/build_cv.py --no-pdf # render cv/cv.tex only, for debugging
```

Requires `xelatex` with `fontspec`, `unicode-math`, `tcolorbox`, `sourcesanspro`,
`fontawesome` and `academicons`.

## Publications

```sh
python3 tools/fetch_inspire.py
```

Queries INSPIRE for the `inspire_bai` in `_data/profile.yml` and writes both
`assets/ref.bib` (the website Publications page, via jekyll-scholar) and
`_data/publications.yml` (the CV PDF).

Papers are split into two buckets by author count:

* **selected** — at most `SELECTED_MAX_AUTHORS` (150) authors, i.e. papers where you
  are a visible author. These get `selected = {true}` in the BibTeX, which is what
  the homepage "Selected publications" block queries. Author lists longer than
  `SELECTED_MAX_LISTED` (12) are truncated with *et al.*, always keeping your own name.
* **collaboration** — the ~1400-author DUNE papers, credited to the collaboration.

Tune the two constants at the top of `tools/fetch_inspire.py` to move the line.

`.github/workflows/refresh-publications.yml` re-runs this every Monday and commits
only if the record changed.

## Deploying

`.github/workflows/deploy.yml` runs on push to `main`: it builds the CV PDF, then the
Jekyll site, then deploys to GitHub Pages. One-time setup: **Settings → Pages →
Source → GitHub Actions**.

## Local preview

```sh
bundle install
bundle exec jekyll serve
```

Needs Ruby >= 3.2 (the Gemfile.lock is bundler 2.7). Ruby 3.0 cannot resolve it.

## Credits

Site template: [sbryngelson/academic-website-template](https://github.com/sbryngelson/academic-website-template) (MIT).
CV class: [posquit0/Awesome-CV](https://github.com/posquit0/Awesome-CV) (CC BY-SA 4.0).
