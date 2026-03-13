#!/usr/bin/env python3
"""
Look up URLs for publications in _data/publications.yml that have empty url fields.
Uses OpenAlex title search (free, no API key). Run and paste suggested URLs into the YAML.

Usage:
  pip install -r scripts/requirements.txt
  python scripts/lookup_paper_urls.py

  --apply   Update publications.yml with found URLs (creates backup first)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import requests
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
PUBLICATIONS_PATH = REPO_ROOT / "_data" / "publications.yml"
OPENALEX_BASE = "https://api.openalex.org"


def load_yaml(path: Path) -> list:
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, list) else []


def search_openalex(title: str, year: str | None = None) -> str | None:
    """Search OpenAlex by title, optionally filter by year. Return best URL (DOI or landing_page)."""
    # Clean title for search: remove HTML, truncate very long
    clean = re.sub(r"<[^>]+>", "", title)
    clean = clean.strip()[:200]
    if not clean:
        return None

    params = {
        "filter": f"display_name.search:{clean}",
        "per-page": 5,
        "sort": "relevance_score:desc",
    }
    if year and str(year).isdigit() and int(year) <= 2025:
        params["filter"] += f",publication_year:{year}"

    try:
        r = requests.get(f"{OPENALEX_BASE}/works", params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        results = data.get("results") or []
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400 and year:
            params["filter"] = f"display_name.search:{clean}"
            try:
                r = requests.get(f"{OPENALEX_BASE}/works", params=params, timeout=15)
                r.raise_for_status()
                data = r.json()
                results = data.get("results") or []
            except Exception:
                return None
        else:
            print(f"  OpenAlex error: {e}", file=sys.stderr)
            return None
    except Exception as e:
        print(f"  OpenAlex error: {e}", file=sys.stderr)
        return None

    if not results:
        return None

    w = results[0]
    doi = (w.get("doi") or "").strip()
    if doi and not doi.startswith("http"):
        doi = f"https://doi.org/{doi}"

    if doi:
        return doi

    loc = w.get("primary_location") or {}
    url = (loc.get("landing_page_url") or loc.get("pdf_url") or "").strip()
    if url:
        return url

    return w.get("id")  # OpenAlex URL as fallback


def main() -> None:
    ap = argparse.ArgumentParser(description="Look up URLs for papers with empty url in publications.yml")
    ap.add_argument("--apply", action="store_true", help="Update YAML with found URLs (backup created first)")
    args = ap.parse_args()

    if not PUBLICATIONS_PATH.exists():
        print(f"Not found: {PUBLICATIONS_PATH}", file=sys.stderr)
        sys.exit(1)

    pubs = load_yaml(PUBLICATIONS_PATH)
    empty = [(i, p) for i, p in enumerate(pubs) if isinstance(p, dict) and (not p.get("url") or not str(p.get("url", "")).strip())]

    if not empty:
        print("No publications with empty url found.")
        return

    print(f"Looking up URLs for {len(empty)} papers via OpenAlex...\n")

    found: list[tuple[int, dict, str]] = []

    for idx, (i, p) in enumerate(empty):
        title = (p.get("title") or "").strip()
        year = p.get("year")
        print(f"[{idx + 1}/{len(empty)}] {title[:60]}...")
        url = search_openalex(title, year)
        if url:
            print(f"  -> {url}")
            found.append((i, p, url))
        else:
            print("  -> (no match)")

    if not found:
        print("\nNo URLs found.")
        return

    print(f"\n--- Found {len(found)} URL(s) ---")
    for i, p, url in found:
        print(f"  {p.get('year')} | {p.get('title', '')[:50]}...")
        print(f"    url: \"{url}\"")

    if args.apply and found:
        backup = PUBLICATIONS_PATH.with_suffix(".yml.bak")
        with open(PUBLICATIONS_PATH, encoding="utf-8") as f:
            orig = f.read()
        with open(backup, "w", encoding="utf-8") as f:
            f.write(orig)
        print(f"\nBackup: {backup}")

        for i, p, url in found:
            pubs[i] = {**p, "url": url}
        with open(PUBLICATIONS_PATH, "w", encoding="utf-8") as f:
            yaml.dump(pubs, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        print("Updated publications.yml")
    else:
        print("\nRun with --apply to write URLs into publications.yml (backup created first).")


if __name__ == "__main__":
    main()
