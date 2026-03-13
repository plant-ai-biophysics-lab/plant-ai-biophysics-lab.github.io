# Scripts

## Fetch publications (OpenAlex + Google Scholar)

Compares publications from **OpenAlex** and optionally **Google Scholar** with your existing `_data/publications.yml` and reports any that might be missing.

### Setup

```bash
cd /path/to/plant-ai-biophysics-lab.github.io
pip install -r scripts/requirements.txt
```

### Usage

**OpenAlex only** (no API key; uses [OpenAlex](https://openalex.org) public API):

```bash
python scripts/fetch_publications.py
```

**OpenAlex + Google Scholar** (Scholar is scraped via [scholarly](https://github.com/scholarly-python-package/scholarly); you may hit rate limits or CAPTCHAs):

```bash
python scripts/fetch_publications.py --scholar
```

**Report only** (no file writes):

```bash
python scripts/fetch_publications.py --report
python scripts/fetch_publications.py --scholar --report
```

### Config: `_data/publications_config.yml`

- **OpenAlex** (used by default): `authors[].openalex_id` or `orcid`.
- **Google Scholar** (optional): add one of these per author:
  - `google_scholar_author_id`: from the profile URL  
    `https://scholar.google.com/citations?user=**XXXX**&hl=en`
  - `name_for_scholar`: search string (e.g. `"Mason Earles UC Davis"`) if you don’t have the ID.

The script prints:

- How many works were fetched from each source.
- OpenAlex works not yet in `publications.yml`.
- (With `--scholar`) Papers that appear in Google Scholar but not in OpenAlex, for you to add manually if needed.

Add any missing entries by editing `_data/publications.yml` (you can copy the format from existing entries and add optional `podcast_url`, `github`, etc.).
