#!/usr/bin/env python3
"""
make_newsletter.py

Constructs a simple newsletter payload from the posts collected in `data/posts.json`.
The result is written to `dist/newsletter.json` with subject, HTML, and plain
text versions. This file is sent via a Zapier webhook configured in the
GitHub Actions workflow.
"""

import json
import os
from datetime import datetime


def main() -> None:
    data_file = os.path.join("data", "posts.json")
    if not os.path.exists(data_file):
        print("No posts to build newsletter. Run fetch_feeds.py first.")
        return
    with open(data_file) as f:
        posts = json.load(f)

    date_str = datetime.now().strftime("%Y-%m-%d")
    subject = f"ByteBench Deals - {date_str}"
    newsletter = {
        "subject": subject,
        "html": "",
        "text": "",
    }
    html_parts = [f"<h1>{subject}</h1>"]
    text_parts = [subject]
    # Limit to first 10 posts for email brevity
    for post in posts[:10]:
        title = post.get("title", "untitled")
        link = post.get("link", "")
        summary = post.get("summary", "")
        html_parts.append(f"<h2><a href=\"{link}\">{title}</a></h2><p>{summary}</p>")
        text_parts.append(f"{title}\n{link}\n{summary}\n")
    newsletter["html"] = "\n".join(html_parts)
    newsletter["text"] = "\n\n".join(text_parts)
    os.makedirs("dist", exist_ok=True)
    with open(os.path.join("dist", "newsletter.json"), "w") as f:
        json.dump(newsletter, f, indent=2)
    print(f"Created newsletter.json with {min(10, len(posts))} items")


if __name__ == "__main__":
    main()
