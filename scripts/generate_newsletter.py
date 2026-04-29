#!/usr/bin/env python3
"""
The Flame of Fortune — Newsletter Generator with Source Images
Calls Claude API (with web search), generates newsletter content,
then fetches og:image from each source article for legally-sound,
contextually accurate images with full attribution.

How images work:
  1. Claude returns a source_url for each story
  2. We fetch that URL and extract the og:image meta tag
  3. Publishers deliberately set og:image for external sharing (Twitter cards,
     LinkedIn previews, WhatsApp previews) — this is standard editorial practice
  4. Every image is displayed with "Image: [Source]" attribution and a link back
  5. Falls back to curated Unsplash topics if no og:image found

Required env vars:
  ANTHROPIC_API_KEY    — console.anthropic.com
  UNSPLASH_ACCESS_KEY  — unsplash.com/developers (optional, for fallbacks)
"""

import os, re, sys, json, datetime
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

ROOT        = Path(__file__).parent.parent
CONTENT_DIR = ROOT / "src" / "content" / "newsletters"
CONTENT_DIR.mkdir(parents=True, exist_ok=True)

TODAY        = datetime.date.today()
DATE_SLUG    = TODAY.strftime("%Y-%m-%d")
DATE_DISPLAY = TODAY.strftime("%A, %d %B %Y")
OUTPUT_FILE  = CONTENT_DIR / f"{DATE_SLUG}.md"

try:
    import anthropic
except ImportError:
    os.system(f"{sys.executable} -m pip install anthropic --quiet")
    import anthropic

try:
    import requests
    from requests.exceptions import RequestException
except ImportError:
    os.system(f"{sys.executable} -m pip install requests --quiet")
    import requests
    from requests.exceptions import RequestException


# ── OG:IMAGE EXTRACTION ───────────────────────────────────────────────────────

class OGParser(HTMLParser):
    """Minimal HTML parser — extracts meta og:image, og:image:url, twitter:image."""
    def __init__(self):
        super().__init__()
        self.image = None
        self.site_name = None
        self._done = False

    def handle_starttag(self, tag, attrs):
        if self._done:
            return
        if tag == "meta":
            d = dict(attrs)
            prop = d.get("property", "") or d.get("name", "")
            content = d.get("content", "")
            if not content:
                return
            if prop in ("og:image", "og:image:url") and not self.image:
                self.image = content
            if prop in ("og:site_name", "twitter:site") and not self.site_name:
                self.site_name = content
        # Stop parsing after </head>
        if tag == "body":
            self._done = True


def fetch_og_image(url: str, timeout: int = 8) -> dict:
    """
    Fetch a URL and extract its og:image and site name.
    Returns {"image": url_or_None, "site_name": str_or_None}
    """
    if not url or not url.startswith("http"):
        return {"image": None, "site_name": None}

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; FlameOfFortuneBot/1.0; "
            "+https://readomg.netlify.app)"
        ),
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=timeout,
                            allow_redirects=True, stream=True)
        resp.raise_for_status()

        # Only read the first 50KB — enough to get <head> meta tags
        chunk = b""
        for part in resp.iter_content(chunk_size=4096):
            chunk += part
            if len(chunk) >= 50_000:
                break

        html = chunk.decode("utf-8", errors="replace")
        parser = OGParser()
        parser.feed(html)

        img = parser.image
        # Make relative URLs absolute
        if img and not img.startswith("http"):
            img = urljoin(url, img)

        # Derive site name from URL if not found in meta
        site_name = parser.site_name
        if not site_name:
            parsed = urlparse(url)
            host = parsed.netloc.replace("www.", "")
            site_name = host.split(".")[0].title()

        if img:
            print(f"    og:image found: {img[:70]}...")
        else:
            print(f"    No og:image at {url[:60]}")

        return {"image": img, "site_name": site_name}

    except RequestException as e:
        print(f"    Fetch error for {url[:60]}: {e}")
        return {"image": None, "site_name": None}


# ── FALLBACK IMAGES (Unsplash curated, topic-matched) ─────────────────────────

UNSPLASH_KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "")

# Curated Unsplash fallbacks that are contextually relevant
FALLBACKS: dict[str, list[str]] = {
    "economy": [
        "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=1200&q=80",
        "https://images.unsplash.com/photo-1559526324-593bc073d938?w=1200&q=80",
        "https://images.unsplash.com/photo-1579532537598-459ecdaf39cc?w=1200&q=80",
    ],
    "infrastructure": [
        "https://images.unsplash.com/photo-1486325212027-8081e485255e?w=1200&q=80",
        "https://images.unsplash.com/photo-1518623001395-125242310d0c?w=1200&q=80",
        "https://images.unsplash.com/photo-1476357471311-43c0db9fb2b4?w=1200&q=80",
    ],
    "africa": [
        "https://images.unsplash.com/photo-1523805009345-7448845a9e53?w=1200&q=80",
        "https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=1200&q=80",
        "https://images.unsplash.com/photo-1489749798305-4fea3ae63d43?w=1200&q=80",
    ],
    "lifestyle": [
        "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=1200&q=80",
        "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=1200&q=80",
        "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=1200&q=80",
    ],
    "tech": [
        "https://images.unsplash.com/photo-1677442135703-1787eea5ce01?w=1200&q=80",
        "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1200&q=80",
        "https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=1200&q=80",
    ],
    "global": [
        "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=1200&q=80",
        "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=1200&q=80",
        "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=1200&q=80",
    ],
}

_fallback_counters: dict[str, int] = {}

def get_fallback(category_key: str) -> str:
    """Rotate through curated fallbacks for variety."""
    options = FALLBACKS.get(category_key, FALLBACKS["global"])
    idx = _fallback_counters.get(category_key, 0)
    _fallback_counters[category_key] = (idx + 1) % len(options)
    return options[idx]


def fetch_unsplash_image(query: str) -> str | None:
    """Fetch a relevant image from Unsplash API if key is available."""
    if not UNSPLASH_KEY:
        return None
    try:
        r = requests.get(
            "https://api.unsplash.com/photos/random",
            params={"query": query, "orientation": "landscape", "content_filter": "high"},
            headers={"Authorization": f"Client-ID {UNSPLASH_KEY}"},
            timeout=8
        )
        if r.status_code == 200:
            data = r.json()
            return data["urls"]["regular"] + "&w=1200"
    except Exception:
        pass
    return None


# ── CLAUDE PROMPT ─────────────────────────────────────────────────────────────

SYSTEM = """You are the content engine for The Flame of Fortune — a premium daily newsletter for ambitious professionals, investors, entrepreneurs, and lifestyle-conscious readers in Malawi and across Africa.

Use your web_search tool to find REAL, CURRENT stories. Then return ONLY valid JSON — no markdown fences, no preamble, nothing else.

RULES:
1. Search for real news from today or this week. Include the actual source article URL for each story.
2. No political content — parties, elections, political figures, controversies.
3. Select 5-6 stories across at least 3 different categories.
4. Always include: at least 1 Malawi story, 1 African story, 1 global story, 1 lifestyle story.
5. Professional analyst standard: specific, named parties, quantified implications.
6. For source_url, provide the direct URL to the specific article you found, NOT just the homepage.

Return this exact JSON structure:
{
  "title": "Punchy outcome-focused title",
  "theme": "One italic through-line sentence",
  "excerpt": "1-2 sentence index summary",
  "cover_query": "4-word Unsplash fallback query e.g. 'Malawi business leaders meeting'",
  "cover_alt": "Descriptive alt text",
  "tags": ["tag1","tag2","tag3"],
  "read_time": "7 min read",
  "question": "Sharp non-political community question",
  "numbers": [
    {"label": "metric name", "value": "figure", "meaning": "one-line implication"}
  ],
  "stories": [
    {
      "category": "MALAWI | ECONOMY",
      "category_key": "economy",
      "emoji": "📍",
      "headline": "Strong specific headline",
      "source": "Publication Name",
      "source_url": "https://exact-article-url.com/article-slug",
      "fallback_query": "4-word Unsplash query e.g. 'tobacco auction Malawi farm'",
      "image_alt": "Descriptive alt text for the image",
      "what_happened": "2-3 sentences. Plain facts with numbers.",
      "what_it_means": "3-5 sentences. Named parties. Quantified. No hedging.",
      "what_to_watch": "1-2 forward-looking sentences with specific thresholds."
    }
  ]
}"""

USER = f"""Today is {DATE_DISPLAY}. Research and generate today's full Flame of Fortune newsletter. Search across Malawi news, African business, global markets, tech/AI, and lifestyle/wellness. For every story, include the direct URL to the specific article. Prioritise stories from the last 48-72 hours."""


# ── CALL CLAUDE ───────────────────────────────────────────────────────────────

def call_claude() -> dict:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY not set.\n"
            "Get a key at console.anthropic.com\n"
            "export ANTHROPIC_API_KEY=sk-ant-..."
        )

    client = anthropic.Anthropic(api_key=key)
    print(f"Researching stories for {DATE_DISPLAY}...")

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=5000,
        system=SYSTEM,
        messages=[{"role": "user", "content": USER}],
        tools=[{"type": "web_search_20250305", "name": "web_search"}]
    )

    for block in reversed(response.content):
        if block.type == "text":
            text = block.text.strip()
            text = re.sub(r'^```(?:json)?\s*\n?', '', text, flags=re.MULTILINE)
            text = re.sub(r'\n?```$', '', text, flags=re.MULTILINE)
            return json.loads(text.strip())

    raise ValueError("No text response from Claude")


# ── RESOLVE IMAGES FOR ALL STORIES ───────────────────────────────────────────

def resolve_images(data: dict) -> list[dict]:
    """
    For each story, try to get an image in this priority order:
      1. og:image from the source_url (most contextually accurate)
      2. Unsplash API search (if key available)
      3. Curated Unsplash fallback (always works, rotates for variety)
    Returns a list of image dicts: {"url", "source_name", "source_url", "alt"}
    """
    story_images = []

    for story in data.get("stories", []):
        source_url = story.get("source_url", "")
        source_name = story.get("source", "Source")
        category_key = story.get("category_key", "global")
        fallback_query = story.get("fallback_query", f"{category_key} Africa")
        image_alt = story.get("image_alt", story.get("headline", ""))

        image_url = None
        image_credit = None

        # Priority 1: og:image from the source article
        if source_url:
            print(f"  Fetching og:image from: {source_url[:60]}...")
            og = fetch_og_image(source_url)
            if og["image"]:
                image_url = og["image"]
                image_credit = og["site_name"] or source_name

        # Priority 2: Unsplash API (topic-matched)
        if not image_url and UNSPLASH_KEY:
            print(f"  Trying Unsplash for: '{fallback_query}'")
            image_url = fetch_unsplash_image(fallback_query)
            if image_url:
                image_credit = "Unsplash"

        # Priority 3: Curated fallback
        if not image_url:
            print(f"  Using curated fallback for category: {category_key}")
            image_url = get_fallback(category_key)
            image_credit = "Unsplash"

        story_images.append({
            "url": image_url,
            "credit": image_credit or source_name,
            "source_url": source_url,
            "alt": image_alt,
        })

    return story_images


def resolve_cover_image(data: dict, story_images: list[dict]) -> dict:
    """
    Cover image: use the first story's og:image if available,
    otherwise fetch from Unsplash using the cover_query.
    """
    # Try first story's image as cover
    if story_images and story_images[0]["url"]:
        first = story_images[0]
        # Try to get a fresh og:image specifically sized for cover
        source_url = data["stories"][0].get("source_url", "") if data.get("stories") else ""
        if source_url:
            og = fetch_og_image(source_url)
            if og["image"]:
                return {"url": og["image"], "credit": og["site_name"] or data["stories"][0].get("source", ""), "alt": data.get("cover_alt", data["title"])}

    # Fallback: Unsplash API
    cover_query = data.get("cover_query", "Malawi business Africa")
    cover_url = None
    if UNSPLASH_KEY:
        cover_url = fetch_unsplash_image(cover_query)
    if not cover_url:
        cover_url = get_fallback("africa")

    return {"url": cover_url, "credit": "Unsplash", "alt": data.get("cover_alt", data["title"])}


# ── BUILD MARKDOWN ─────────────────────────────────────────────────────────────

def esc(s: str) -> str:
    return '"' + str(s).replace('\\', '\\\\').replace('"', '\\"') + '"'

def esc_url(s: str) -> str:
    return str(s).replace('"', '%22').replace('(', '%28').replace(')', '%29')


def build_markdown(data: dict, edition: int, story_images: list[dict], cover: dict) -> str:
    numbers_yaml = "\n".join(
        f'  - label: {esc(n["label"])}\n    value: {esc(str(n["value"]))}\n    meaning: {esc(n["meaning"])}'
        for n in data.get("numbers", [])
    )
    tags_yaml = "\n".join(f'  - {esc(t)}' for t in data.get("tags", []))

    frontmatter = f"""---
title: {esc(data['title'])}
theme: {esc(data['theme'])}
excerpt: {esc(data['excerpt'])}
date: {esc(DATE_DISPLAY)}
dateSlug: {esc(DATE_SLUG)}
edition: {edition}
readTime: {esc(data.get('read_time', '7 min read'))}
question: {esc(data['question'])}
coverImage: {esc(cover['url'])}
coverAlt: {esc(cover['alt'])}
coverCredit: {esc(cover['credit'])}
tags:
{tags_yaml}
numbers:
{numbers_yaml}
---"""

    stories_md = ""
    for i, story in enumerate(data.get("stories", [])):
        img = story_images[i] if i < len(story_images) else {"url": "", "credit": "", "source_url": "", "alt": ""}

        # Build image markdown with attribution caption
        img_md = ""
        if img["url"]:
            source_url = img.get("source_url") or story.get("source_url", "")
            credit = img.get("credit", story.get("source", "Source"))
            alt = img.get("alt", story.get("headline", ""))
            img_md = f'![{alt}]({esc_url(img["url"])})\n*Image source: [{credit}]({source_url or "#"})*\n'

        stories_md += f"""
## {story['emoji']} {story['headline']}

### {story['category']}

> **Source:** [{story['source']}]({story.get('source_url', '#')}) · {DATE_DISPLAY}

{img_md}
### What Happened

{story['what_happened']}

### What It Means

{story['what_it_means']}

> **What To Watch:** {story['what_to_watch']}

---
"""

    return f"{frontmatter}\n{stories_md.strip()}\n"


# ── EDITION NUMBER ─────────────────────────────────────────────────────────────

def get_edition() -> int:
    existing = [f for f in CONTENT_DIR.glob("*.md") if f.name != OUTPUT_FILE.name]
    return len(existing) + 1


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    if OUTPUT_FILE.exists():
        print(f"Today's edition already exists: {OUTPUT_FILE.name}")
        print("Delete it to regenerate.")
        return

    edition = get_edition()
    print(f"\n🔥 Flame of Fortune — Edition #{edition} | {DATE_DISPLAY}\n")
    if not UNSPLASH_KEY:
        print("No UNSPLASH_ACCESS_KEY — will use og:images + curated fallbacks.\n")

    # 1. Generate content via Claude
    data = call_claude()
    print(f"\nContent ready: \"{data['title']}\"\n")

    # 2. Resolve images from source URLs
    print("Resolving images from source articles...")
    story_images = resolve_images(data)

    print("\nResolving cover image...")
    cover = resolve_cover_image(data, story_images)

    # 3. Build markdown
    md = build_markdown(data, edition, story_images, cover)
    OUTPUT_FILE.write_text(md, encoding="utf-8")

    print(f"\nSaved: src/content/newsletters/{DATE_SLUG}.md")
    print(f"🔥 Edition #{edition} complete — {len([i for i in story_images if i['url']])} images resolved.\n")


if __name__ == "__main__":
    main()
