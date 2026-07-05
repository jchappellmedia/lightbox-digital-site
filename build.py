#!/usr/bin/env python3
"""Static site generator for Lightbox Digital. Run: python3 build.py"""
import json, html, pathlib

ROOT = pathlib.Path(__file__).parent
BASE = "https://lightbox-digital.com"
EMAIL = "josh.lightbox@gmail.com"
SOCIALS = {
    "Instagram": "https://www.instagram.com/joshrchappell/",
    "Facebook": "https://www.facebook.com/people/Lightbox-Digital/61571745974669/",
    "X": "https://x.com/LightboxDig",
    "Vimeo": "https://vimeo.com/lightboxdigital",
}

# ---------------------------------------------------------------- work ----
# cat: commercials | stories | events | ai   src: vimeo id or file path
V = lambda id, title, dur, date, cat, line, h=None, file=None: dict(
    id=id, title=title, dur=dur, date=date, cat=cat, line=line, h=h, file=file)

REEL = V("1103241704", "Demo Reel", 27, "2025-07-21", "reel",
         "Twenty-seven seconds of what we do.")

WORK = [
    # Commercials
    V("1099054535", "Allen Land & Fire", 24, "2025-07-05", "commercials",
      "A commercial for a land-clearing crew."),
    V("1004646002", "Treston × Cornerstone", 73, "2024-08-30", "commercials",
      "A commercial about craftsmanship."),
    V("960746274", "Rags To Riches", 29, "2024-06-17", "commercials",
      "A 29-second ad. No wasted frames."),
    V("1103919211", "Applied Tech", 61, "2025-07-23", "commercials",
      "Industrial work, filmed right."),
    V("396854352", "Arrowhead Lakes Dentistry", 139, "2020-03-11", "commercials",
      "A practice film that feels like a first visit."),
    V("882198847", "Butterfly Wonderland", None, "2023-11-01", "commercials",
      "America's largest butterfly conservatory.", h="b06b5e4591"),
    V("1004647012", "Ad One", 79, "2024-08-30", "commercials",
      "From rough idea to finished cut."),
    V("705537712", "Oculus Giveaway", 114, "2022-05-02", "commercials",
      "A giveaway people actually shared."),
    # Stories
    V("480986594", "Baths For The Brave", 271, "2020-11-18", "stories",
      "A veteran. A donated remodel. A lot of heart."),
    V("1092229333", "IWE — Day in the Life", 105, "2025-06-10", "stories",
      "One student's actual day, start to finish."),
    V("1089338714", "GCU Worship Arts", None, "2025-06-01", "stories",
      "Inside a university program.", h="a33679bb7c"),
    V("1004645760", "Construction Student", 69, "2024-08-30", "stories",
      "She found her thing. Her story, her words."),
    V("654280242", "Inspiring Teachers", 39, "2021-12-07", "stories",
      "A thank-you to teachers. Bring tissues."),
    V("1004652992", "President's Message", 61, "2024-08-30", "stories",
      "A leadership message with real warmth."),
    V("1092230232", "MNE", 179, "2025-06-10", "stories",
      "A school, seen the way families see it."),
    # Events & Spaces
    V("1004647238", "Incito 2022", 228, "2024-08-30", "events",
      "A full event, distilled."),
    V("1041569506", "NCAA Coverage", 83, "2024-12-22", "events",
      "Shot for broadcast and social at once."),
    V("385325737", "Blandford Homes — Mandarin Grove", 119, "2020-01-16", "events",
      "Luxury real estate, treated like cinema."),
    # AI
    V("daves-garage", "Dave's Garage", 27, "2025-09-02", "ai",
      "A complete commercial, generated with AI.", file="assets/video/daves-garage.mp4"),
]

CATS = [("commercials", "Commercials"), ("stories", "Stories"),
        ("events", "Events & Spaces"), ("ai", "AI")]
CATNAME = dict(CATS)

PHOTOS = [
    ("studio-portrait-1.jpg", "Studio portrait with dramatic lighting"),
    ("family-portrait-hug.jpg", "Candid family portrait outdoors"),
    ("football-action.jpg", "Football action shot"),
    ("school-portrait.jpg", "School portrait of a smiling student"),
    ("ocean-landscape.jpg", "Ocean landscape"),
    ("studio-portrait-2.jpg", "Corporate headshot on studio backdrop"),
    ("posed-portrait.png", "Editorial portrait"),
    ("studio-portrait-3.jpg", "Environmental portrait, cinematic color"),
    ("relaxed-portrait.jpg", "Natural-light lifestyle portrait"),
    ("gorilla-wildlife.jpg", "Wildlife photography — gorilla"),
    ("school-event.jpg", "School event photography"),
    ("classroom-learning.jpg", "Hands-on learning in a classroom"),
    ("videography-bts.jpg", "Behind the scenes on a shoot"),
]

REVIEWS = [
    ("Carissa Harris", "Josh was great to work with on my company's product launch video. From pre-shoot meetings, to coordinating on site at our factory and the studio, to delivering the final product, everything went smoothly. He took his time to get the best angles and best lighting."),
    ("Jason Gillespie", "A fantastic video resource and a pleasure to work with. Excellent suggestions, quickly gets a grasp of the vision, flexible, performs well under pressure, and delivers great finished products."),
    ("Ashley Leslie", "An absolute pleasure to work with for the corporate videos we had created for a special event. Went above and beyond with our limited timeframe and was extremely communicative throughout."),
    ("Olivia McFadden", "Professional, prepared, and organized. The final videos looked amazing. I would 100% work with him again."),
    ("Ivy Coppo", "Talented, thoughtful on details and very creative. We used Lightbox at Blandford Homes to shoot our community video and it is one of my favorite videos we have."),
    ("Brian Gottlieb", "Exceptional! We've worked together for years during our Baths for the Brave bath crash. He captures the moment to perfection — I highly recommend!"),
    ("Sarah Gerber", "Amazing quality of work! Professionally done photos, edited in a timely manner. Family photos with our 2 year old and 6 week old — they are precious."),
    ("Jake Price", "Very easy to work with and quick to respond. The video quality is outstanding!"),
    ("Kevin McKamey", "Great photos of our business workshop, refined and delivered for quick review as promised. Professional manner and quick response to our last minute request."),
    ("Melody Hudson", "Simply put, the work is amazing. Creative vision and talent that produces great work to visually help tell our clients' stories."),
    ("Esmeralda Acosta", "Very professional and knowledgeable. Totally recommend."),
]

SERVICES = [
    ("Commercials", "Concept to final cut."),
    ("Landing videos", "The first thing your website says."),
    ("Social content", "Cut for the feed, vertical and wide."),
    ("Interviews", "Good light, clean sound, real people."),
    ("Events", "The day, kept."),
    ("Drone", "FAA Part 107 licensed aerials."),
    ("Photography", "Headshots, brands, events."),
    ("AI video", "Generated commercials, made carefully."),
]

FAQ = [
    ("Where does Lightbox Digital work?",
     "Phoenix and the whole Valley — Scottsdale, Mesa, Tempe, Chandler, Gilbert, Glendale. Arizona-wide and travel projects too."),
    ("What do you make?",
     "Commercials, landing videos, social content, interviews, event films, drone footage, AI-generated video, and photography."),
    ("What does it cost?",
     "Depends on the project. Say what you want to make and what you want to spend — the quote you get is the price you pay."),
    ("How long does it take?",
     "We agree on a date before filming starts, and the date holds."),
    ("Is the drone work licensed?",
     "Yes — FAA Part 107 certified and insured."),
    ("What are AI videos?",
     "Commercials built with AI-generated footage instead of a camera crew. Faster and far less expensive than a full shoot — and getting better every month. See Dave's Garage on the AI page."),
]

# ------------------------------------------------------------- helpers ----
FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,340..640;1,9..144,340..640&family=Inter:wght@400;500&display=swap" rel="stylesheet">'

def esc(s): return html.escape(s, quote=True)

def nav(active):
    items = [("work.html","Work"),("ai-videos.html","AI Videos"),("photography.html","Photography"),("about.html","About")]
    links = "".join(f'<a href="{h}"{" class=active" if h==active else ""}>{t}</a>' for h,t in items)
    return f'''<header class="nav">
  <a class="brand" href="index.html" aria-label="Lightbox Digital home"><img src="assets/img/mark-ink.png" alt="" width="30" height="31"><span>Lightbox&nbsp;Digital</span></a>
  <nav class="nav-links" id="navLinks" aria-label="Primary">{links}<a href="contact.html" class="contact-link{' active' if active=='contact.html' else ''}">Contact</a></nav>
  <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false"><span></span><span></span></button>
</header>'''

def footer():
    soc = " · ".join(f'<a href="{u}" rel="me noopener" target="_blank">{n}</a>' for n,u in SOCIALS.items())
    return f'''<footer class="footer">
  <div class="footer-inner">
    <p class="fmark"><img src="assets/img/mark-ink.png" alt="" width="26" height="27"> Lightbox Digital</p>
    <p>Video production &amp; photography — Phoenix, Arizona.<br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <p class="fsoc">{soc}</p>
    <p class="fnav"><a href="work.html">Work</a> · <a href="ai-videos.html">AI Videos</a> · <a href="photography.html">Photography</a> · <a href="about.html">About</a> · <a href="reviews.html">Reviews</a> · <a href="contact.html">Contact</a></p>
    <p class="fcopy">© 2026 Joshua Chappell LLC · Serving Phoenix, Scottsdale, Mesa, Tempe, Chandler, Gilbert &amp; all of Arizona</p>
  </div>
</footer>
<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Player" hidden>
  <button class="lb-close" id="lbClose" aria-label="Close">✕</button>
  <div class="lb-frame" id="lbFrame"></div>
</div>
<script src="js/main.js?v=3" defer></script>'''

def work_card(v, big=False):
    dur = f"{v['dur']//60}:{v['dur']%60:02d}" if v['dur'] else ""
    if v['file']:
        data = f'data-video="{v["file"]}"'
    else:
        h = f"?h={v['h']}" if v['h'] else ""
        data = f'data-vimeo="{v["id"]}{h}"'
    thumb = f"assets/thumbs/{v['id']}.jpg"
    return f'''<figure class="piece{' big' if big else ''} reveal" data-cat="{v['cat']}">
  <button class="pthumb" {data} aria-label="Play: {esc(v['title'])}">
    <img src="{thumb}" alt="Still from {esc(v['title'])}" width="640" height="360" loading="lazy">
    <span class="pplay" aria-hidden="true"></span>
  </button>
  <figcaption><strong>{esc(v['title'])}</strong> <em>{esc(v['line'])}</em>{f'<span class="pdur">{dur}</span>' if dur else ''}</figcaption>
</figure>'''

def video_ld(vs):
    out = []
    for v in vs:
        d = {"@type":"VideoObject","name":v["title"],"description":v["line"],
             "thumbnailUrl":f"{BASE}/assets/thumbs/{v['id']}.jpg","uploadDate":v["date"]}
        if v["file"]:
            d["contentUrl"] = f"{BASE}/{v['file']}"
        else:
            d["embedUrl"] = f"https://player.vimeo.com/video/{v['id']}" + (f"?h={v['h']}" if v['h'] else "")
        if v["dur"]: d["duration"] = f"PT{v['dur']//60}M{v['dur']%60}S"
        out.append(d)
    return out

ORG = {
    "@type":"ProfessionalService","@id":BASE+"/#org","name":"Lightbox Digital",
    "description":"Video production and photography in Phoenix, Arizona. Commercials, brand stories, event films, drone footage, AI-generated video, and photography.",
    "url":BASE+"/","logo":BASE+"/assets/img/mark-ink.png","image":BASE+"/assets/img/hero-poster.jpg",
    "email":EMAIL,
    "founder":{"@type":"Person","name":"Josh Chappell","jobTitle":"Founder","sameAs":SOCIALS["Instagram"]},
    "address":{"@type":"PostalAddress","addressLocality":"Phoenix","addressRegion":"AZ","addressCountry":"US"},
    "areaServed":[{"@type":"City","name":n} for n in ["Phoenix","Scottsdale","Mesa","Tempe","Chandler","Gilbert","Glendale"]] + [{"@type":"State","name":"Arizona"}],
    "priceRange":"$$","sameAs":list(SOCIALS.values()),
    "knowsAbout":["video production","commercials","AI video generation","drone videography","brand photography","event videography","corporate interviews"],
    "aggregateRating":{"@type":"AggregateRating","ratingValue":"5.0","reviewCount":str(len(REVIEWS)),"bestRating":"5"},
}

def page(fname, title, desc, body, ld_extra=None, og_img="assets/img/hero-poster.jpg"):
    ld = [dict(ORG),
          {"@type":"WebSite","name":"Lightbox Digital","url":BASE+"/","publisher":{"@id":BASE+"/#org"}}]
    crumbs = [{"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"}]
    if fname != "index.html":
        crumbs.append({"@type":"ListItem","position":2,"name":title.split("—")[0].split("|")[0].strip(),"item":f"{BASE}/{fname}"})
    ld.append({"@type":"BreadcrumbList","itemListElement":crumbs})
    if ld_extra: ld += ld_extra
    ldjson = json.dumps({"@context":"https://schema.org","@graph":ld}, ensure_ascii=False)
    url = f"{BASE}/{fname}" if fname != "index.html" else BASE+"/"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large, max-video-preview:-1">
<meta name="author" content="Josh Chappell">
<meta name="geo.region" content="US-AZ"><meta name="geo.placename" content="Phoenix">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Lightbox Digital">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@LightboxDig">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{BASE}/{og_img}">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
{FONT}
<link rel="stylesheet" href="css/style.css?v=3">
<script type="application/ld+json">{ldjson}</script>
</head>
<body>
{nav(fname)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>'''

W = {}

# ------------------------------------------------------------------ home ----
featured = [v for v in WORK if v["id"] in
            ("1099054535","480986594","882198847","daves-garage","1092229333","385325737")]

quotes = "".join(f'''<blockquote class="quote reveal"><p>“{esc(t)}”</p><cite>— {esc(n)}, Google review</cite></blockquote>'''
                 for n,t in [(REVIEWS[3][0], REVIEWS[3][1]), (REVIEWS[5][0], REVIEWS[5][1]), (REVIEWS[7][0], REVIEWS[7][1])])

svc_list = "".join(f'<li class="reveal"><strong>{esc(t)}</strong><span>{esc(d)}</span></li>' for t,d in SERVICES)
faq_html = "".join(f'<details class="faq reveal"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in FAQ)

home_body = f'''
<section class="intro">
  <p class="eyebrow reveal">Video production &amp; photography · Phoenix, Arizona</p>
  <h1 class="reveal">Films for businesses that are <em class="squiggle">proud of their work</em>.</h1>
  <p class="note reveal">Fewer words, more watching — the reel is 27 seconds. <span class="arrow">↓</span></p>
</section>

<section class="reelwrap">
  {work_card(REEL, big=True)}
</section>

<section class="section">
  <p class="label reveal">01 — Selected work</p>
  <div class="grid">{"".join(work_card(v) for v in featured)}</div>
  <p class="more reveal"><a href="work.html">All work →</a></p>
</section>

<section class="section">
  <p class="label reveal">02 — What we make</p>
  <ul class="svc">{svc_list}</ul>
</section>

<section class="section">
  <p class="label reveal">03 — Kind words</p>
  <div class="quotes">{quotes}</div>
  <p class="more reveal"><a href="reviews.html">All {len(REVIEWS)} reviews, five stars each →</a></p>
</section>

<section class="section">
  <p class="label reveal">04 — Questions</p>
  <div class="faqwrap">{faq_html}</div>
</section>

<section class="cta">
  <h2 class="reveal">Let's make something <em class="squiggle">good</em>.</h2>
  <p class="reveal"><a class="btn" href="contact.html">Start a project</a> <span class="or">or write to</span> <a href="mailto:{EMAIL}">{EMAIL}</a></p>
</section>'''

ld_home = [{"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}] + video_ld([REEL]+featured)
W["index.html"] = page("index.html",
    "Phoenix Video Production & Photography | Lightbox Digital",
    "Lightbox Digital makes commercials, brand stories, event films, drone footage, AI video, and photography in Phoenix, AZ. Watch the work — it speaks for itself. 5.0★ on Google.",
    home_body, ld_home)

# ------------------------------------------------------------------ work ----
filters = '<div class="filters reveal" role="group" aria-label="Filter">' + \
  '<button class="fbtn active" data-f="all">All</button>' + \
  "".join(f'<button class="fbtn" data-f="{k}">{esc(n)}</button>' for k,n in CATS) + '</div>'

W["work.html"] = page("work.html",
    "The Work — Video Production in Phoenix | Lightbox Digital",
    "Commercials, stories, event films, and AI video made in Phoenix, AZ. Press play on any of them.",
    f'''
<section class="intro small">
  <p class="eyebrow reveal">The work</p>
  <h1 class="reveal">Press play. <em class="squiggle">That's the pitch.</em></h1>
</section>
<section class="section">
  {filters}
  <div class="grid" id="workgrid">{"".join(work_card(v) for v in [REEL]+WORK)}</div>
  <p class="more reveal">Photos instead? <a href="photography.html">Photography →</a></p>
</section>
<section class="cta">
  <h2 class="reveal">Your business belongs up here.</h2>
  <p class="reveal"><a class="btn" href="contact.html">Start a project</a></p>
</section>''',
    video_ld([REEL]+WORK), og_img="assets/img/cinema-camera.jpg")

# ------------------------------------------------------------------- ai ----
ai_vids = [v for v in WORK if v["cat"]=="ai"]
W["ai-videos.html"] = page("ai-videos.html",
    "AI Video Production in Phoenix — AI-Generated Commercials | Lightbox Digital",
    "AI-generated commercials from Lightbox Digital in Phoenix, AZ. Full ads made with AI — a fraction of the cost of a shoot. Watch Dave's Garage.",
    f'''
<section class="intro small">
  <p class="eyebrow reveal">AI videos</p>
  <h1 class="reveal">Commercials, <em class="squiggle">generated</em>.</h1>
  <p class="note reveal">Some ads don't need a camera anymore. We write, direct, and craft complete commercials with AI-generated footage — real ideas, real editing, a fraction of the cost of a full production. It's new, it's quick, and it's already good. Judge for yourself.</p>
</section>
<section class="section">
  <div class="grid">{"".join(work_card(v, big=True) for v in ai_vids)}</div>
</section>
<section class="section">
  <p class="label reveal">Good to know</p>
  <div class="prose reveal">
    <p>AI video works best for product spots, concept ads, and ideas that would be expensive to film — exotic locations, impossible camera moves, things that don't exist yet. You still get real direction, real writing, real sound design, and a real editor making it all land. When your story needs real people and real places, we bring the cameras. Often the best answer is both.</p>
  </div>
</section>
<section class="cta">
  <h2 class="reveal">Curious what AI could make for you?</h2>
  <p class="reveal"><a class="btn" href="contact.html">Ask us</a></p>
</section>''',
    video_ld(ai_vids), og_img="assets/thumbs/daves-garage.jpg")

# ----------------------------------------------------------- photography ----
photo_items = "".join(f'''<figure class="pitem reveal"><button class="pimg" data-img="assets/img/{f}" aria-label="View: {esc(alt)}"><img src="assets/img/{f}" alt="{esc(alt)}" loading="lazy"></button></figure>''' for f,alt in PHOTOS)
W["photography.html"] = page("photography.html",
    "Phoenix Photographer — Portraits, Events & Brand Photography | Lightbox Digital",
    "Brand photography, headshots, portraits, school and event photos in Phoenix, AZ — with the same eye as the films.",
    f'''
<section class="intro small">
  <p class="eyebrow reveal">Photography</p>
  <h1 class="reveal">Same eye, <em class="squiggle">one frame at a time</em>.</h1>
</section>
<section class="section"><div class="masonry">{photo_items}</div></section>
<section class="cta">
  <h2 class="reveal">Need photos?</h2>
  <p class="reveal"><a class="btn" href="contact.html">Book a shoot</a></p>
</section>''',
    [{"@type":"ImageGallery","name":"Lightbox Digital Photography","url":f"{BASE}/photography.html",
      "image":[f"{BASE}/assets/img/{f}" for f,_ in PHOTOS]}],
    og_img="assets/img/videography-bts.jpg")

# ----------------------------------------------------------------- about ----
ld_about = [{"@type":"Person","name":"Josh Chappell","jobTitle":"Founder, Lightbox Digital",
             "image":f"{BASE}/assets/img/josh-chappell.jpg","email":f"mailto:{EMAIL}",
             "sameAs":list(SOCIALS.values()),
             "address":{"@type":"PostalAddress","addressLocality":"Phoenix","addressRegion":"AZ"}}]
W["about.html"] = page("about.html",
    "About — Lightbox Digital, Phoenix Video Production",
    "Lightbox Digital is a Phoenix video production and photography studio founded by Josh Chappell. FAA Part 107 licensed. On time, on budget, no drama.",
    f'''
<section class="section about">
  <div class="about-grid">
    <img class="reveal" src="assets/img/josh-chappell.jpg" alt="Josh Chappell, founder of Lightbox Digital" width="500" height="640">
    <div>
      <p class="eyebrow reveal">About</p>
      <h1 class="reveal">Lightbox Digital is run by <em class="squiggle">Josh Chappell</em>.</h1>
      <div class="prose">
        <p class="reveal">Years of filming for schools and companies around Phoenix taught us one thing: every business that's good at what it does has a story worth watching. Our job is to get it on camera without making anyone feel like an actor.</p>
        <p class="reveal">The craft matters — cinema cameras, real lighting, clean sound, FAA Part 107 licensed drone work. But the promise is simpler: easy process, honest quotes, delivered on time.</p>
        <p class="reveal"><strong>Lens in hand, ready when you are.</strong></p>
      </div>
      <p class="reveal"><a class="btn" href="contact.html">Work with us</a></p>
    </div>
  </div>
</section>
<section class="section">
  <p class="label reveal">Behind the scenes</p>
  <div class="about-grid flip">
    <div class="prose">
      <p class="reveal">The person on your first call is the person behind the camera and the person making the final cut. Nothing gets lost between departments, because there aren't any.</p>
    </div>
    <img class="reveal" src="assets/img/bts-interview.jpg" alt="Behind the scenes on a Lightbox Digital interview shoot" loading="lazy" width="600" height="420">
  </div>
</section>''',
    ld_about, og_img="assets/img/josh-chappell.jpg")

# --------------------------------------------------------------- reviews ----
rev_items = "".join(f'''<blockquote class="quote reveal"><p>“{esc(t)}”</p><cite>— {esc(n)} · ★★★★★ Google</cite></blockquote>''' for n,t in REVIEWS)
ld_rev = [{"@type":"LocalBusiness","@id":BASE+"/#org","name":"Lightbox Digital",
           "image":BASE+"/assets/img/hero-poster.jpg",
           "address":{"@type":"PostalAddress","addressLocality":"Phoenix","addressRegion":"AZ","addressCountry":"US"},
           "aggregateRating":{"@type":"AggregateRating","ratingValue":"5.0","reviewCount":str(len(REVIEWS)),"bestRating":"5"},
           "review":[{"@type":"Review","reviewRating":{"@type":"Rating","ratingValue":"5","bestRating":"5"},
                      "author":{"@type":"Person","name":n},"reviewBody":t} for n,t in REVIEWS]}]
W["reviews.html"] = page("reviews.html",
    "Reviews — 5.0★ on Google | Lightbox Digital, Phoenix",
    f"{len(REVIEWS)} Google reviews, five stars each. What clients say about working with Lightbox Digital in Phoenix, AZ.",
    f'''
<section class="intro small">
  <p class="eyebrow reveal">Reviews</p>
  <h1 class="reveal">{len(REVIEWS)} reviews. <em class="squiggle">Five stars each.</em></h1>
</section>
<section class="section"><div class="quotes col">{rev_items}</div></section>
<section class="cta">
  <h2 class="reveal">The next one could be yours.</h2>
  <p class="reveal"><a class="btn" href="contact.html">Start a project</a></p>
</section>''',
    ld_rev, og_img="assets/img/bts-filming.jpg")

# --------------------------------------------------------------- contact ----
W["contact.html"] = page("contact.html",
    "Contact — Lightbox Digital, Phoenix Video Production",
    "Tell us what you want to make. Straight answers, a plan, and a real quote — usually within a business day. Phoenix, AZ.",
    f'''
<section class="section contact">
  <div class="about-grid">
    <div>
      <p class="eyebrow reveal">Contact</p>
      <h1 class="reveal">Tell us what you want to <em class="squiggle">make</em>.</h1>
      <div class="prose reveal">
        <p>Straight answers, a plan, and a real quote — usually within a business day.</p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a><br>Phoenix, Arizona</p>
        <p class="fsoc">{" · ".join(f'<a href="{u}" rel="me noopener" target="_blank">{n}</a>' for n,u in SOCIALS.items())}</p>
      </div>
    </div>
    <form class="form reveal" action="https://formsubmit.co/{EMAIL}" method="POST">
      <input type="hidden" name="_subject" value="New project inquiry — lightbox-digital.com">
      <input type="text" name="_honey" style="display:none">
      <label>Name <input name="name" required autocomplete="name"></label>
      <label>Email <input type="email" name="email" required autocomplete="email"></label>
      <label>What are we making? <select name="project">
        <option>Commercial</option><option>Landing video</option><option>Social content</option>
        <option>Interview</option><option>Event</option><option>Drone</option>
        <option>AI video</option><option>Photography</option><option>Something else</option></select></label>
      <label>Tell us about it <textarea name="message" rows="5" required></textarea></label>
      <button class="btn" type="submit">Send</button>
    </form>
  </div>
</section>''',
    [{"@type":"ContactPage","name":"Contact Lightbox Digital","url":BASE+"/contact.html"}])

# ------------------------------------------------------------------- 404 ----
W["404.html"] = page("404.html", "Page Not Found | Lightbox Digital",
    "That page didn't make the final cut. Head back to the work.",
    '''<section class="intro"><p class="eyebrow">404</p>
<h1>That scene got <em class="squiggle">cut</em>.</h1>
<p class="note"><a class="btn" href="index.html">Back to the homepage</a></p></section>''')

# ------------------------------------------------------- redirect stubs ----
REDIRECTS = {"portfolio.html":"work.html", "education.html":"work.html",
             "construction.html":"work.html", "medical.html":"work.html",
             "commercial.html":"work.html"}
for old, new in REDIRECTS.items():
    W[old] = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta http-equiv="refresh" content="0;url={new}"><link rel="canonical" href="{BASE}/{new}">
<title>Moved — Lightbox Digital</title></head>
<body><p>This page moved to <a href="{new}">{new}</a>.</p></body></html>'''

# ------------------------------------------------------------ write files ---
for f, src in W.items():
    (ROOT / f).write_text(src)
    print("wrote", f, len(src)//1024, "KB")

pages = [p for p in W if p not in REDIRECTS and p != "404.html"]
sm = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
pri = {"index.html":"1.0","work.html":"0.9","ai-videos.html":"0.9","contact.html":"0.9"}
for p in pages:
    loc = BASE+"/" if p=="index.html" else f"{BASE}/{p}"
    sm.append(f"<url><loc>{loc}</loc><lastmod>2026-07-05</lastmod><priority>{pri.get(p,'0.8')}</priority></url>")
sm.append("</urlset>")
(ROOT/"sitemap.xml").write_text("\n".join(sm))

(ROOT/"robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")

(ROOT/"llms.txt").write_text(f"""# Lightbox Digital

> Video production and photography studio in Phoenix, Arizona, founded by Josh Chappell.
> Makes commercials, brand stories, event films, FAA Part 107 drone footage,
> AI-generated video, and photography. Rated 5.0 across {len(REVIEWS)} Google reviews.

Contact: {EMAIL}
Service area: Phoenix, Scottsdale, Mesa, Tempe, Chandler, Gilbert, Glendale, all of Arizona.

## Pages
- [Home]({BASE}/): demo reel, selected work, services, FAQ
- [Work]({BASE}/work.html): {len(WORK)+1} films — commercials, stories, events & spaces, AI
- [AI Videos]({BASE}/ai-videos.html): AI-generated commercials, incl. "Dave's Garage"
- [Photography]({BASE}/photography.html): portraits, brand, school, sports, events
- [About]({BASE}/about.html): the studio, founded by Josh Chappell
- [Reviews]({BASE}/reviews.html): {len(REVIEWS)} five-star Google reviews
- [Contact]({BASE}/contact.html): inquiry form

## Notable clients & projects
Grand Canyon University, Blandford Homes, Butterfly Wonderland, Baths For The Brave,
Arrowhead Lakes Dentistry, Applied Tech, Allen Land & Fire, NCAA event coverage.
""")
print("wrote sitemap.xml, robots.txt, llms.txt")
