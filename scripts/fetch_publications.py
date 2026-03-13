#!/usr/bin/env python3
"""
Fetch publications from OpenAlex and optionally Google Scholar, then compare
with _data/publications.yml to report potentially missing papers.

Usage:
  pip install -r scripts/requirements.txt
  python scripts/fetch_publications.py [--scholar] [--report]

  --scholar   Also fetch from Google Scholar (requires scholarly; may be rate-limited).
  --report    Only print report; do not write any files.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import requests
import yaml

# Repo root (script lives in scripts/)
REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "_data" / "publications_config.yml"
PUBLICATIONS_PATH = REPO_ROOT / "_data" / "publications.yml"
OPENALEX_BASE = "https://api.openalex.org"


def load_yaml(path: Path) -> list | dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def normalize_title(title: str) -> str:
    """Lowercase, collapse whitespace, remove some punctuation for fuzzy matching."""
    if not title or not isinstance(title, str):
        return ""
    t = title.lower().strip()
    t = re.sub(r"[\s\-–—]+", " ", t)
    t = re.sub(r"[^\w\s]", "", t)
    return " ".join(t.split())


def get_openalex_works(author_id: str, max_years_back: int = 15, per_page: int = 200) -> list[dict]:
    """Fetch all works for an OpenAlex author ID (paginated)."""
    from_year = 2026 - max_years_back
    works: list[dict] = []
    cursor = "*"
    while True:
        params = {
            "filter": f"authorships.author.id:https://openalex.org/{author_id}",
            "per-page": min(200, per_page),
            "cursor": cursor,
            "sort": "publication_date:desc",
        }
        r = requests.get(f"{OPENALEX_BASE}/works", params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        results = data.get("results") or []
        for w in results:
            pub_date = (w.get("publication_date") or "")[:4]
            if pub_date.isdigit() and int(pub_date) < from_year:
                continue
            works.append(w)
        # Stop early if we're past the year window (results sorted by date desc)
        if results:
            last_date = (results[-1].get("publication_date") or "")[:4]
            if last_date.isdigit() and int(last_date) < from_year:
                break
        meta = data.get("meta", {})
        next_cursor = meta.get("next_cursor")
        if not next_cursor:
            break
        cursor = next_cursor
    return works


def openalex_work_to_entry(w: dict) -> dict:
    """Convert OpenAlex work to a minimal entry like publications.yml."""
    title = (w.get("title") or "").strip()
    year = (w.get("publication_date") or "")[:4] or None
    authors = w.get("authorships") or []
    author_names = []
    for a in authors:
        author = a.get("author") or {}
        name = author.get("display_name") or ""
        if name:
            author_names.append(name)
    authors_str = ", ".join(author_names) if author_names else ""
    # Prefer DOI link, then primary_location
    doi = (w.get("doi") or "").strip()
    if doi and not doi.startswith("http"):
        doi = f"https://doi.org/{doi}"
    url = doi
    if not url:
        loc = w.get("primary_location") or {}
        url = (loc.get("landing_page_url") or "").strip() or (loc.get("pdf_url") or "").strip()
    if not url:
        url = w.get("id") or ""  # OpenAlex URL
    return {"title": title, "year": year, "authors": authors_str, "url": url, "doi": doi or None}


def get_existing_titles(publications_path: Path) -> set[str]:
    """Load existing publication titles (normalized) from YAML."""
    if not publications_path.exists():
        return set()
    data = load_yaml(publications_path)
    if not isinstance(data, list):
        return set()
    titles = set()
    for item in data:
        if isinstance(item, dict) and "title" in item:
            titles.add(normalize_title(item["title"]))
    return titles


def fetch_google_scholar_publications(
    scholar_author_id: str | None = None,
    author_name: str | None = None,
    publication_limit: int = 100,
) -> list[dict]:
    """Fetch publications from Google Scholar. Returns list of {title, year, url, authors}."""
    try:
        from scholarly import scholarly
    except ImportError:
        print("Warning: install 'scholarly' for Google Scholar (pip install scholarly).", file=sys.stderr)
        return []

    entries: list[dict] = []
    try:
        if scholar_author_id:
            author = scholarly.search_author_id(scholar_author_id)
        elif author_name:
            author = next(scholarly.search_author(author_name), None)
            if not author:
                return []
        else:
            return []

        author = scholarly.fill(author, sections=["publications"], publication_limit=publication_limit)
        for pub in author.get("publications") or []:
            scholarly.fill(pub)
            bib = pub.get("bib") or {}
            title = (bib.get("title") or "").strip()
            if not title:
                continue
            year = bib.get("pub_year") or bib.get("year")
            if year:
                year = str(year)
            url = (pub.get("pub_url") or pub.get("eprint_url") or "").strip()
            authors = bib.get("author") or ""
            if isinstance(authors, list):
                authors = ", ".join(authors)
            entries.append({"title": title, "year": year, "url": url, "authors": authors})
    except Exception as e:
        print(f"Google Scholar error: {e}", file=sys.stderr)
    return entries


def main() -> None:
    ap = argparse.ArgumentParser(description="Fetch publications from OpenAlex and optionally Google Scholar.")
    ap.add_argument("--scholar", action="store_true", help="Also fetch from Google Scholar")
    ap.add_argument("--report", action="store_true", help="Only print report (no file writes)")
    args = ap.parse_args()

    if not CONFIG_PATH.exists():
        print(f"Config not found: {CONFIG_PATH}", file=sys.stderr)
        sys.exit(1)

    config = load_yaml(CONFIG_PATH)
    authors = config.get("authors") or []
    max_years_back = int(config.get("max_years_back") or 15)
    per_author_limit = int(config.get("per_author_limit") or 200)

    existing = get_existing_titles(PUBLICATIONS_PATH)
    openalex_titles: set[str] = set()
    openalex_entries: list[dict] = []
    scholar_entries: list[dict] = []
    scholar_titles: set[str] = set()

    # OpenAlex
    seen_openalex_ids: set[str] = set()
    for author in authors:
        oa_id = author.get("openalex_id") or (author.get("orcid") and f"https://openalex.org/{author.get('orcid')}")
        if not oa_id:
            continue
        if isinstance(oa_id, str) and oa_id.startswith("https://"):
            oa_id = oa_id.split("/")[-1]
        if oa_id in seen_openalex_ids:
            continue
        seen_openalex_ids.add(oa_id)
        print(f"Fetching OpenAlex author {oa_id} ...", file=sys.stderr)
        works = get_openalex_works(oa_id, max_years_back=max_years_back, per_page=per_author_limit)
        for w in works:
            entry = openalex_work_to_entry(w)
            norm = normalize_title(entry["title"])
            if norm and norm not in openalex_titles:
                openalex_titles.add(norm)
                openalex_entries.append(entry)

    # Google Scholar (optional)
    if args.scholar:
        for author in authors:
            sid = author.get("google_scholar_author_id")
            name = author.get("name_for_scholar")
            if not sid and not name:
                continue
            print(f"Fetching Google Scholar ({sid or name}) ...", file=sys.stderr)
            for entry in fetch_google_scholar_publications(scholar_author_id=sid, author_name=name):
                norm = normalize_title(entry.get("title") or "")
                if norm and norm not in scholar_titles:
                    scholar_titles.add(norm)
                    scholar_entries.append(entry)

    # Report
    in_openalex_not_in_existing = [e for e in openalex_entries if normalize_title(e["title"]) not in existing]
    in_scholar_not_in_existing = [e for e in scholar_entries if normalize_title(e.get("title") or "") not in existing] if scholar_entries else []
    in_scholar_not_in_openalex = []
    if scholar_titles and openalex_titles:
        in_scholar_not_in_openalex = [e for e in scholar_entries if normalize_title(e.get("title") or "") not in openalex_titles]

    print("\n--- OpenAlex ---")
    print(f"Fetched {len(openalex_entries)} works (last {max_years_back} years).")
    print(f"Already in publications.yml: {len(openalex_entries) - len(in_openalex_not_in_existing)}")
    if in_openalex_not_in_existing:
        print(f"OpenAlex works not yet in publications.yml ({len(in_openalex_not_in_existing)}):")
        for e in in_openalex_not_in_existing[:30]:
            print(f"  - {e.get('year')} | {e.get('title')}")
        if len(in_openalex_not_in_existing) > 30:
            print(f"  ... and {len(in_openalex_not_in_existing) - 30} more.")

    if args.scholar and scholar_entries:
        print("\n--- Google Scholar ---")
        print(f"Fetched {len(scholar_entries)} publications.")
        if in_scholar_not_in_openalex:
            print(f"Papers in Google Scholar but not in OpenAlex ({len(in_scholar_not_in_openalex)}):")
            for e in in_scholar_not_in_openalex:
                print(f"  - {e.get('year')} | {e.get('title')}")
        else:
            print("All Scholar papers found in OpenAlex.")

    if not args.report and in_openalex_not_in_existing and PUBLICATIONS_PATH.exists():
        print("\nTo add missing papers, edit _data/publications.yml manually or run a merge script.", file=sys.stderr)


if __name__ == "__main__":
    main()
