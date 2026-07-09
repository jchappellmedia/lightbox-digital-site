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
Submissions are (1) stored in Supabase (project `lightbox-digital`, table `contact_submissions`,
insert-only RLS via the publishable key in `js/main.js`) and (2) emailed to jchappellmedia@gmail.com
via FormSubmit. The form's `action` posts to FormSubmit directly as a no-JS fallback.

## SEO
JSON-LD (ProfessionalService, VideoObject, FAQPage, Reviews, ImageGallery), unique metas,
OG/Twitter cards, sitemap.xml, robots.txt, llms.txt.
