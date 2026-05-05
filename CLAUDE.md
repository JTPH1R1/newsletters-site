# Outreach Media Group — Newsletter Generation Guide

## What This Newsletter Is

Outreach Media Group publishes a daily intelligence newsletter from Blantyre, Malawi. It serves ambitious professionals, investors, entrepreneurs, and business owners in Malawi and across Africa.

**The core mission:** Take complicated financial, economic, and business stories and explain them in plain English. Break down the jargon. Expand the small print. Make it useful for someone who did not study economics but needs to understand what is happening and why it affects them.

---

## The Rules

1. **One story per file.** Each newsletter edition covers ONE topic in depth. No bundling multiple stories into one file.
2. **Multiple sources per story.** Every story must be researched from at least 3–5 sources. Search the web, compare what different outlets are saying, and synthesise into one clear analysis.
3. **Plain English always.** Define every piece of jargon. If you use a term like "IPO", "monetary policy", "fiscal deficit", or "cross-listing" — explain it immediately in simple language as if the reader has never heard it before.
4. **Sources listed at the bottom.** Every edition ends with a `### Sources` section listing all sources as clickable links so readers can fact-check.
5. **Malawi/Africa lens.** Always connect the story back to what it means for Malawi specifically, or for African professionals in general. Even a global story must land locally.
6. **Strictly no political content.** This is an absolute rule with no exceptions. No political parties. No elections. No politicians or political figures by name. No commentary on government leadership or opposition. No policy analysis that names a ruling party or politician. Stories about government economic data (inflation, debt, reserves) are fine — frame them around the numbers and institutions, never around politicians. If a story cannot be told without naming a political figure or party, do not write it.

---

## File Naming Convention

Each file lives in `src/content/newsletters/` and is named by date:

- One story per day: `2026-05-05.md`
- Multiple stories same day: `2026-05-05-dangote.md`, `2026-05-05-traders.md`

---

## Frontmatter Template

```markdown
---
title: "Punchy, specific headline — outcome-focused, not vague"
theme: "One italic sentence that captures the deeper meaning of the story"
excerpt: "1–2 sentences. The homepage summary. Plain English. No jargon."
date: "Tuesday, 5 May 2026"
dateSlug: "2026-05-05"
edition: [NUMBER — increment from last edition]
readTime: "X min read"
question: "A sharp, non-political question for readers to think about or discuss. Should feel personal and relevant."
tags:
  - "Economy"
  - "Africa"
coverImage: ""
coverAlt: ""
coverCredit: ""
advertImage: ""
advertLink: ""
numbers:
  - label: "Metric name"
    value: "Figure"
    meaning: "One plain-English sentence explaining what this number means in practice."
---
```

---

## Article Body Structure

Every article body follows this exact structure:

```markdown
## The Story in 30 Seconds
2–3 sentences. Maximum plain English. A reader should understand the entire story from this alone.

---

## What Is Actually Happening
Factual account. What happened, who did what, when, what was announced. Attribute facts to sources. No analysis yet — just clear facts from multiple sources synthesised into one coherent narrative.

---

## Breaking It Down — Plain English
This is the most important section. Define every technical term used in the story. Use the format:

**What does "[term]" mean?**
Plain English explanation that anyone can understand.

Repeat for every piece of jargon in the story.

---

## What It Means for Africa — and for Malawi
Connect the story to the reader's life. What does this mean for:
- Malawian professionals and entrepreneurs
- Investors in the region
- Ordinary people (prices, jobs, services)
- Malawi's economy specifically

Be specific. Named implications. Quantified where possible.

---

## What To Watch
3–5 forward-looking bullet points with specific signals and thresholds. Tell the reader exactly what to watch for and why it matters.

---

### Sources
- [Article Title — Publication Name](url)
- [Article Title — Publication Name](url)
- [Article Title — Publication Name](url)
```

---

## How to Generate a Newsletter Edition

When the user asks for a newsletter on a topic:

1. **Search the web** using at least 3 different queries to gather information from multiple sources
2. **Collect 3–5 quality sources** — prefer established African business publications (African Business, Further Africa, Nyasa Times, Business Day, CNBC Africa, Semafor) plus international sources (Reuters, FT, Bloomberg, World Bank)
3. **Write the full markdown file** following the structure above exactly
4. **Include the key numbers** in the frontmatter — pick the 3–5 most important figures from the story
5. **Write the plain English breakdowns** — do not assume the reader knows any financial or economic terminology
6. **End with all sources** as clickable links

## Edition Numbering

Check the existing files in `src/content/newsletters/` to find the highest edition number, then increment by 1.

Current editions:
- Edition 1: 2026-04-28.md (Malawi tobacco season, airport, oil shock)
- Edition 2: 2026-05-05.md (Dangote $40bn IPO)
- Edition 3: 2026-05-05-vision2020.md (Malawi vs Rwanda Vision 2020)
- Edition 4: 2026-05-05-china-tariffs.md (China zero tariffs for Africa)
- Edition 5: 2026-05-05-africa-growth.md (Africa's fastest-growing economies)
- Edition 6: 2026-05-05-sumitomo.md (Sumitomo exits Ambatovy nickel mine)
- Edition 7: 2026-05-05-dangote-ethiopia.md (Dangote eyes Ethiopia stock exchange)
- Edition 8: next to be written

---

## Tone

- Direct. Confident. Analytical.
- Never condescending — the reader is intelligent, just not a specialist.
- No filler phrases ("it is worth noting that...", "importantly...", "in conclusion...")
- No hedging — take a clear position on what something means.
- Write like a smart colleague explaining something over coffee, not like a textbook.