# Lightbox Digital — Website

Handcrafted, SEO-optimized static site for [Lightbox Digital](https://lightbox-digital.com/), a Phoenix, AZ video production & photography studio.

Design: a darkroom / light-table theme — film-frame thumbnails with glowing sprocket holes and edge print, contact-sheet photo grid, safelight-red grease-pencil accents, full-bleed hero reel, and photos that "develop in" on scroll.

**Live:** https://lightbox-digital.com/

## Structure
- Pages: home, work (filterable: Commercials / Stories / Events & Spaces / AI), AI videos, photography, about, reviews, contact, 404
- Ranking / geo landings: Phoenix video production, Phoenix commercial video, Phoenix drone (Part 107), Scottsdale, Tempe
- 20 films: 19 Vimeo embeds + self-hosted AI commercial (assets/video/daves-garage.mp4)
- Old page URLs (portfolio/education/construction/medical/commercial/our-work/construstion-trades-industrial) redirect to work.html via meta-refresh stubs (GitHub Pages does not support true HTTP 301s on a plain static site)

## Editing
Content lives in `build.py` (WORK list, reviews, services, FAQ, copy). After editing:
```bash
python3 build.py
```
Then commit + push — GitHub Pages deploys automatically. Styles: `css/style.css`, interactions: `js/main.js`.
When changing CSS/JS, bump the `?v=` number in build.py so browsers fetch the new files.

## Contact form
Submissions are emailed to jchappellmedia@gmail.com via FormSubmit (AJAX from `js/main.js`,
with the form's `action` posting to FormSubmit directly as a no-JS fallback).

## SEO
JSON-LD (ProfessionalService + LocalBusiness, VideoObject, FAQPage, Reviews, ImageGallery), unique metas,
OG/Twitter cards, sitemap.xml, robots.txt (AI crawlers allowed), llms.txt.
