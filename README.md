# Lightbox Digital — Website

Handcrafted, SEO-optimized static site for [Lightbox Digital](https://lightbox-digital.com/), a Phoenix, AZ video production & photography studio.

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

## SEO
JSON-LD (ProfessionalService, VideoObject, FAQPage, Reviews, ImageGallery), unique metas,
OG/Twitter cards, sitemap.xml, robots.txt, llms.txt.
