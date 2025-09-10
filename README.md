# ByteBench Deals

ByteBench Deals is an automated tech & gaming deals site and newsletter. It
fetches product updates from public RSS feeds, generates posts, builds a static
site, and composes a daily email. The entire workflow runs on GitHub
Actions, deploys via Netlify, and sends the newsletter via a Zapier Webhook.

## Structure

- **site.config.json** – Main configuration: site name, timezone, sources, and filters.
- **scripts/** – Automation scripts:
  - `fetch_feeds.py` pulls RSS feeds and writes `data/posts.json`.
  - `write_posts.py` converts entries to Markdown files in `content/`.
  - `build_site.py` renders HTML pages using Jinja2 templates into `dist/`.
  - `make_newsletter.py` creates `dist/newsletter.json` for the email.
- **templates/** – Jinja2 templates for index and post pages.
- **.github/workflows/publish.yml** – GitHub Actions workflow that runs daily.
- **netlify.toml** – Netlify build configuration.

## Running locally

Install dependencies and run the scripts:

```bash
python3 -m pip install -r requirements.txt
python3 scripts/fetch_feeds.py
python3 scripts/write_posts.py
python3 scripts/build_site.py
python3 scripts/make_newsletter.py
```

The static site will be written to `dist/` and the newsletter payload to
`dist/newsletter.json`.

## Automation

This project is designed to run hands‑off via GitHub Actions. The workflow
fetches feeds, builds the site, uploads an artifact, triggers a Netlify build
hook, and posts the newsletter payload to a Zapier Catch Hook. Configure the
following secrets in your repository settings:

- `NETLIFY_BUILD_HOOK_URL` – Netlify build hook URL.
- `ZAPIER_WEBHOOK_URL` – Zapier Webhook catch URL.

Optionally, embed your Skimlinks script into `templates/index.html` and
`templates/post.html` before the closing `</body>` tag to enable automatic
affiliate linking.
