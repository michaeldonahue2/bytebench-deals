#!/usr/bin/env python3
"""
fetch_feeds.py

This script reads the `site.config.json` file to determine which RSS feeds to
fetch. It uses the feedparser library to download and parse each feed and
collects basic metadata for each entry (title, link, summary, published date,
and source name). The aggregated posts are written to `data/posts.json` for
downstream processing.

Run this script before `write_posts.py` and `build_site.py`.
"""

import json
import os
import logging
from datetime import datetime

import feedparser

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def main() -> None:
    # Read configuration
    with open("site.config.json") as cfg_file:
        config = json.load(cfg_file)
    sources = config.get("sources", [])
    posts: list[dict] = []

    for source in sources:
        if source.get("type") != "rss":
            continue
        url = source.get("url")
        name = source.get("name")
        if not url:
            continue
        logging.info(f"Fetching feed: {name} from {url}")
        try:
            feed = feedparser.parse(url)
        except Exception as exc:
            logging.warning(f"Failed to parse feed {url}: {exc}")
            continue
        for entry in feed.entries:
            posts.append(
                {
                    "title": entry.get("title", "").strip(),
                    "link": entry.get("link", ""),
                    "summary": entry.get("summary", ""),
                    "published": entry.get("published", ""),
                    "source": name,
                }
            )

    # Ensure the output directory exists
    out_dir = "data"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "posts.json")
    with open(out_path, "w") as f:
        json.dump(posts, f, indent=2)
    logging.info(f"Wrote {len(posts)} posts to {out_path}")


if __name__ == "__main__":
    main()
