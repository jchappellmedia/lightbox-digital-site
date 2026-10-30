# Lightbox Digital — Website

Handcrafted, SEO-optimized static site for [Lightbox Digital](https://lightbox-digital.com/), a Phoenix, AZ video production & photography studio.

Design: a darkroom / light-table theme — film-frame thumbnails with glowing sprocket holes and edge print, contact-sheet photo grid, safelight-red grease-pencil accents, full-bleed hero reel, and photos that "develop in" on scroll.

**Live:** https://lightbox-digital.com/

## Structure
- Pages: home, work (filterable: Commercials / Stories / Events & Spaces / AI), AI videos, photography, about, reviews, contact, 404
- 20 films: 19 Vimeo embeds + self-hosted AI commercial (assets/video/daves-garage.mp4)
- Old page URLs (portfolio/education/construction/medical/commercial) redirect to work.html

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

## SEO & indexing
- sitemap.xml carries image and video extensions (all films on work.html, photos on
  photography/about) and per-page lastmod that only changes when a page's output changes
- IndexNow: a key file at the root plus .github/workflows/indexnow.yml pings Bing/Yandex
  with every sitemap URL after each deploy to main
- 404 and the old redirect stubs are noindex; the private dashboard is noindex and unlinked
- Images: thumbs capped at 1280px, photos at 1600px, JPEG q80 progressive
JSON-LD (ProfessionalService, VideoObject, FAQPage, Reviews, ImageGallery), unique metas,
OG/Twitter cards, sitemap.xml, robots.txt, llms.txt.
