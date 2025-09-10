#!/usr/bin/env python3
"""
write_posts.py

Reads `data/posts.json` (produced by `fetch_feeds.py`) and writes each entry
to an individual markdown file in the `content` directory. Each file contains
YAML front matter with basic metadata followed by the summary text from the
feed entry. Filenames are prefixed with today's date and a slugified title.
"""

import json
import os
from datetime import datetime
from slugify import slugify


def main() -> None:
    data_file = os.path.join("data", "posts.json")
    if not os.path.exists(data_file):
        print(f"{data_file} not found. Run fetch_feeds.py first.")
        return
    with open(data_file) as f:
        posts = json.load(f)

    output_dir = "content"
    os.makedirs(output_dir, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")

    for post in posts:
        title = post.get("title", "untitled")
        slug = slugify(title)[:50]
        filename = f"{today}-{slug}.md"
        filepath = os.path.join(output_dir, filename)
        front_matter = [
            f"title: {title}",
            f"published: {post.get('published', '')}",
            f"source: {post.get('source', '')}",
            f"link: {post.get('link', '')}",
        ]
        summary = post.get("summary", "")
        with open(filepath, "w") as f:
            f.write("---\n")
            for line in front_matter:
                f.write(line + "\n")
            f.write("---\n\n")
            f.write(summary)
    print(f"Wrote {len(posts)} markdown posts to {output_dir}")


if __name__ == "__main__":
    main()
