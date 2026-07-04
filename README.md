# Lightbox Digital — Website

Modern, SEO-optimized static website for [Lightbox Digital](https://lightbox-digital.com/), a Phoenix, AZ video production and photography company by Josh Chappell.

**Live site:** https://lightbox-digital.com/

## What's inside

- 11 hand-tuned static pages (home, 4 industry pages, video portfolio, photography, about, reviews, contact, 404)
- 18 Vimeo productions embedded via a click-to-play lightbox (zero iframe weight until play)
- Self-hosted images + hero background video (no Squarespace dependency)
- Contact form via FormSubmit → josh.lightbox@gmail.com

## SEO

- Unique titles/descriptions, canonical URLs, Open Graph + Twitter cards on every page
- JSON-LD structured data: ProfessionalService, VideoObject (per video), FAQPage,
  Review/AggregateRating, Person, ImageGallery, BreadcrumbList
- `sitemap.xml`, `robots.txt`, and `llms.txt` (AI-search discovery)
- Semantic HTML, descriptive alt text, lazy-loaded media

## Editing

Page content lives in `build.py` (videos, reviews, services, copy). After editing:

```bash
python3 build.py
```

This regenerates all HTML files. Styles are in `css/style.css`, interactions in `js/main.js`.

## Custom domain

To use `lightbox-digital.com`: add a `CNAME` file containing the domain, point DNS
(CNAME record `www` → `jchappellmedia.github.io`, A records for apex to GitHub Pages IPs),
then set the domain in repo Settings → Pages. Update `BASE` in `build.py` and rebuild.
