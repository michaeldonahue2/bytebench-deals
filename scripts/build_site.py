#!/usr/bin/env python3
"""
build_site.py

This script uses Jinja2 templates located in the `templates` directory to
generate a static HTML site from the data collected by `fetch_feeds.py`. It
produces individual HTML pages for each post and an index page listing all
entries. Output is written to the `dist` directory.
"""

import os
import json
from slugify import slugify
from jinja2 import Environment, FileSystemLoader


def main() -> None:
    # Load configuration for site name
    with open("site.config.json") as cfg:
        config = json.load(cfg)

    data_file = os.path.join("data", "posts.json")
    if not os.path.exists(data_file):
        print("No posts to build. Run fetch_feeds.py first.")
        return
    with open(data_file) as f:
        posts = json.load(f)

    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader("templates"))
    post_template = env.get_template("post.html")
    index_template = env.get_template("index.html")

    dist_dir = "dist"
    os.makedirs(dist_dir, exist_ok=True)

    entries = []
    for post in posts:
        title = post.get("title", "untitled")
        slug = slugify(title)[:50]
        filename = f"{slug}.html"
        html = post_template.render(
            title=title,
            summary=post.get("summary", ""),
            link=post.get("link", ""),
            source=post.get("source", ""),
            published=post.get("published", ""),
        )
        with open(os.path.join(dist_dir, filename), "w") as f:
            f.write(html)
        entries.append(
            {
                "title": title,
                "url": filename,
                "source": post.get("source", ""),
                "published": post.get("published", ""),
            }
        )

    index_html = index_template.render(site_name=config.get("site_name", "Site"), entries=entries)
    with open(os.path.join(dist_dir, "index.html"), "w") as f:
        f.write(index_html)
    print(f"Built site with {len(entries)} posts into {dist_dir}")


if __name__ == "__main__":
    main()
