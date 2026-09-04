#!/usr/bin/env python3
"""Static site generator for Lightbox Digital. Run: python3 build.py"""
import json, html, pathlib, struct, re, datetime

ROOT = pathlib.Path(__file__).parent
BASE = "https://lightbox-digital.com"
EMAIL = "josh.lightbox@gmail.com"          # public contact address shown on the site
NOTIFY = "josh.lightbox@gmail.com"         # where form submissions are emailed

# Paste a Google Analytics 4 Measurement ID ("G-XXXXXXXXXX") to switch analytics on.
# Empty = no gtag script is emitted at all.
GA4_ID = "G-XNPRM5NLFM"

# Google Tag Manager container. GTM is a delivery mechanism, not a measurement
# tool: it only collects data once a GA4 tag is configured inside the container.
GTM_ID = ""   # container removed — GA4 is wired directly above

GTM_HEAD = """<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','__GTM__');</script>
<!-- End Google Tag Manager -->"""

GTM_BODY = """<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=__GTM__"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""

DASHBOARD = "studio-9f31c7.html"           # private marketing dashboard (noindex, unlinked)

# Reading GA4 numbers back out needs two more IDs, both safe to publish:
#   GA4_PROPERTY_ID  numeric, Admin -> Property settings (NOT the G- id)
#   OAUTH_CLIENT_ID  Google Cloud OAuth 2.0 Web client. Public by design; it
#                    grants nothing on its own — the viewer still has to sign
#                    in with a Google account that can read the property.
# Both can also be pasted straight into the dashboard, which remembers them.
GA4_PROPERTY_ID = ""
OAUTH_CLIENT_ID = ""
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
    V("1220703634", "High Plains Provisions", 26, "2026-08-24", "ai",
      "Another complete commercial, generated with AI.", h="1500ae4e40"),
]

CATS = [("commercials", "Commercials"), ("stories", "Stories"),
        ("events", "Events & Spaces"), ("ai", "AI")]
CATNAME = dict(CATS)

# film-frame numbers for the light-table edge print
REEL["num"] = "00A"
for _i, _v in enumerate(WORK, 1):
    _v["num"] = f"{_i:02d}A"

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
    ("What does a video production cost in Phoenix?",
     "Depends on the project. Say what you want to make and what you want to spend — the quote you get is the price you pay."),
    ("How long does it take?",
     "We agree on a date before filming starts, and the date holds."),
    ("Is the drone work licensed?",
     "Yes — FAA Part 107 certified and insured."),
    ("What are AI videos?",
     "Commercials built with AI-generated footage instead of a camera crew. Faster and far less expensive than a full shoot — and getting better every month. See Dave's Garage on the AI page."),
    ("Who runs Lightbox Digital?",
     "Josh Chappell. The person on your first call is the person behind the camera and the person making the final cut — nothing gets lost between departments, because there aren't any."),
    ("Do you do photography as well as video?",
     "Yes — corporate headshots, brand photography, school portraits and events, family portraits, and sports, shot with the same eye as the films."),
    ("What kinds of businesses do you film?",
     "Schools and universities, construction and trades, medical and dental practices, real estate, attractions, and industrial companies — including Grand Canyon University, Blandford Homes, and Butterfly Wonderland."),
    ("Do you make vertical videos for social media?",
     "Yes. Social content is cut for the feed — vertical and wide versions from the same shoot."),
    ("How do I get a quote?",
     "Email josh.lightbox@gmail.com or use the contact form. You'll get straight answers, a plan, and a real quote — usually within a business day."),
]

# ------------------------------------------------------------- helpers ----
def img_size(path):
    """Read pixel dimensions from a JPEG or PNG header (no dependencies)."""
    with open(path, "rb") as f:
        head = f.read(26)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            w, h = struct.unpack(">II", head[16:24]); return w, h
        f.seek(2)
        while True:
            b = f.read(2)
            if len(b) < 2: return None
            while b[0] != 0xFF: b = b[1:] + f.read(1)
            m = b[1]
            if m in (0xC0,0xC1,0xC2,0xC3,0xC5,0xC6,0xC7,0xC9,0xCA,0xCB,0xCD,0xCE,0xCF):
                f.read(3); h, w = struct.unpack(">HH", f.read(4)); return w, h
            f.seek(struct.unpack(">H", f.read(2))[0] - 2, 1)

FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Anton&family=Fraunces:ital,opsz,wght@1,9..144,340..640&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">'

def esc(s): return html.escape(s, quote=True)

def analytics():
    """Tag Manager container and/or a direct GA4 tag. Nothing is emitted unless
    one of the IDs above is set."""
    out = []
    if GTM_ID:
        out.append(GTM_HEAD.replace("__GTM__", GTM_ID))
    if GA4_ID:
        out.append(f'''<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
gtag('js',new Date());gtag('config','{GA4_ID}',{{anonymize_ip:true}});</script>''')
    return "\n".join(out)

def gtm_body():
    return GTM_BODY.replace("__GTM__", GTM_ID) if GTM_ID else ""

def mailto(subject, label=None):
    href = f"mailto:{EMAIL}?subject={subject.replace(' ', '%20').replace('—', '%E2%80%94')}"
    return f'<a href="{href}">{label or EMAIL}</a>'

TRUST = (f'<p class="trust reveal">5.0 ★ across {len(REVIEWS)} Google reviews'
         '<span>·</span>FAA Part 107 licensed &amp; insured'
         '<span>·</span>Phoenix-based, Valley-wide</p>')

def cta(heading, sub, btn_label="Start a project", subject="Project inquiry"):
    """One CTA band, used site-wide: a clear next step, a one-tap email path,
    and quiet facts instead of pressure."""
    return f'''<section class="cta">
  <h2 class="reveal">{heading}</h2>
  <p class="ctasub reveal">{sub}</p>
  <p class="ctaact reveal"><a class="btn" href="contact.html">{btn_label}</a>
    <span class="or">or email</span> {mailto(subject)}</p>
  {TRUST}
</section>'''

def nav(active):
    items = [("work.html","Our Work"),("about.html","About")]
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
    <p class="fnav"><a href="work.html">Our Work</a> · <a href="ai-videos.html">AI Videos</a> · <a href="photography.html">Photography</a> · <a href="about.html">About</a> · <a href="reviews.html">Reviews</a> · <a href="contact.html">Contact</a></p>
    <p class="fcopy">© 2026 Joshua Chappell LLC · Serving Phoenix, Scottsdale, Mesa, Tempe, Chandler, Gilbert &amp; all of Arizona</p>
  </div>
</footer>
<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Player" hidden>
  <button class="lb-close" id="lbClose" aria-label="Close">✕</button>
  <div class="lb-frame" id="lbFrame"></div>
</div>
<script src="js/main.js?v=13" defer></script>'''

def work_card(v, big=False):
    dur = f"{v['dur']//60}:{v['dur']%60:02d}" if v['dur'] else ""
    if v['file']:
        data = f'data-video="{v["file"]}"'
    else:
        h = f"?h={v['h']}" if v['h'] else ""
        data = f'data-vimeo="{v["id"]}{h}"'
    thumb = f"assets/thumbs/{v['id']}.jpg"
    fno = f'<span class="fno" aria-hidden="true">LBX 500T · {v["num"]}</span>' if v.get("num") else ""
    return f'''<figure class="piece{' big' if big else ''} reveal" data-cat="{v['cat']}">
  <button class="pthumb" {data} aria-label="Play: {esc(v['title'])}">
    <img src="{thumb}" alt="Still from {esc(v['title'])}" width="640" height="360" loading="lazy">
    {fno}<span class="pplay" aria-hidden="true"></span>
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
    "geo":{"@type":"GeoCoordinates","latitude":33.4484,"longitude":-112.0740},
    "areaServed":[{"@type":"City","name":n} for n in ["Phoenix","Scottsdale","Mesa","Tempe","Chandler","Gilbert","Glendale"]] + [{"@type":"State","name":"Arizona"}],
    "hasOfferCatalog":{"@type":"OfferCatalog","name":"Video production & photography services",
        "itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":t,"description":d}} for t,d in SERVICES]},
    "priceRange":"$$","sameAs":list(SOCIALS.values()),
    "knowsAbout":["video production","commercials","AI video generation","drone videography","brand photography","event videography","corporate interviews"],
    "aggregateRating":{"@type":"AggregateRating","ratingValue":"5.0","reviewCount":str(len(REVIEWS)),"bestRating":"5"},
}

def page(fname, title, desc, body, ld_extra=None, og_img="assets/img/hero-poster.jpg", index=True):
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
<meta name="theme-color" content="#0e0c09">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{'index, follow, max-image-preview:large, max-video-preview:-1' if index else 'noindex, nofollow, noarchive'}">
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
<link rel="stylesheet" href="css/style.css?v=13">
<script type="application/ld+json">{ldjson}</script>
{analytics()}
</head>
<body>
{gtm_body()}
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
<section class="hero">
  <video class="hero-video" poster="assets/img/hero-poster.jpg" autoplay muted loop playsinline preload="auto" aria-hidden="true"></video>
  <script>(function(){{var v=document.querySelector('.hero-video');v.src=matchMedia('(max-width:820px)').matches?'assets/video/hero-720.mp4':'assets/video/hero.mp4';}})()</script>
  <div class="hero-scrim" aria-hidden="true"></div>
  <div class="hero-hud" aria-hidden="true"><span class="rec">Rec</span><span>Phoenix, AZ</span></div>
  <div class="hero-inner">
    <p class="eyebrow">Video production &amp; photography · Phoenix, Arizona</p>
    <h1>Films for businesses that are <em class="squiggle">proud of their work</em>.</h1>
    <p class="note">Fewer words, more watching — the reel is 27 seconds. <span class="arrow">↓</span></p>
  </div>
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

<section class="section">
  <p class="label reveal">05 — The studio, in plain words</p>
  <div class="prose">
    <p class="reveal">Lightbox Digital is a video production company and photography studio in Phoenix, Arizona,
    founded and run by Josh Chappell. The studio makes commercials, brand story films, landing-page and recruitment
    videos, social media content, interview and testimonial videos, event films, FAA Part&nbsp;107 licensed drone
    footage, AI-generated commercials, and business photography — corporate headshots, brand shoots, school
    portraits, and event coverage.</p>
    <p class="reveal">Based in Phoenix and working across the Valley — Scottsdale, Mesa, Tempe, Chandler, Gilbert,
    and Glendale — as well as statewide and travel projects. Clients include Grand Canyon University, Blandford
    Homes, Butterfly Wonderland, Arrowhead Lakes Dentistry, Applied Tech, and Baths For The Brave, with a 5.0
    rating across {len(REVIEWS)} Google reviews. One person answers your call, films your project, and cuts the
    final edit.</p>
  </div>
</section>

{cta("Let's make something <em class='squiggle'>good</em>.",
     "Tell us what you're making. You'll get straight answers, a plan, and a real quote — usually within a business day.")}'''

ld_home = [{"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}] + video_ld([REEL]+featured)
W["index.html"] = page("index.html",
    "Phoenix Video Production & Photography | Lightbox Digital",
    "Lightbox Digital makes commercials, brand stories, event films, drone footage, AI video, and photography in Phoenix, AZ. Watch the work — it speaks for itself. 5.0★ on Google.",
    home_body, ld_home)

# ------------------------------------------------------------------ work ----
W["work.html"] = page("work.html",
    "The Work — Video Production in Phoenix | Lightbox Digital",
    "Commercials, stories, event films, and AI video made in Phoenix, AZ. Press play on any of them.",
    f'''
<section class="intro small">
  <p class="eyebrow reveal">The work</p>
  <h1 class="reveal">Press play. <em class="squiggle">That's the pitch.</em></h1>
  <p class="note reveal">Commercial video production for Phoenix businesses — brand films, recruitment and landing videos, event coverage, drone footage, and AI-generated spots, filmed across the Valley.</p>
</section>
<section class="section">
  <div class="grid" id="workgrid">{"".join(work_card(v) for v in [REEL]+WORK)}</div>
  <p class="more reveal">Photos instead? <a href="photography.html">Photography →</a> &nbsp;·&nbsp; Curious about AI? <a href="ai-videos.html">AI Videos →</a></p>
</section>
{cta("Your business belongs up here.",
     "Send us the rough idea — even a sentence. We'll tell you what it takes to film it, and what it costs.")}''',
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
{cta("Curious what AI could make for you?",
     "Describe the spot you have in mind. We'll tell you honestly whether AI is the right tool for it — and what it would cost either way.",
     btn_label="Ask us", subject="AI video question")}''',
    video_ld(ai_vids), og_img="assets/thumbs/daves-garage.jpg")

# ----------------------------------------------------------- photography ----
def photo_item(f, alt):
    dims = img_size(ROOT / "assets/img" / f)
    wh = f' width="{dims[0]}" height="{dims[1]}"' if dims else ""
    return (f'<figure class="pitem reveal"><button class="pimg" data-img="assets/img/{f}" aria-label="View: {esc(alt)}">'
            f'<img src="assets/img/{f}" alt="{esc(alt)}"{wh} loading="lazy"></button></figure>')

photo_items = "".join(photo_item(f, alt) for f, alt in PHOTOS)
W["photography.html"] = page("photography.html",
    "Phoenix Photographer — Portraits, Events & Brand Photography | Lightbox Digital",
    "Brand photography, headshots, portraits, school and event photos in Phoenix, AZ — with the same eye as the films.",
    f'''
<section class="intro small">
  <p class="eyebrow reveal">Photography</p>
  <h1 class="reveal">Same eye, <em class="squiggle">one frame at a time</em>.</h1>
  <p class="note reveal">Phoenix photographer for corporate headshots, brand and product photography, school portraits and events, family portraits, and sports — across the Valley and Arizona.</p>
</section>
<section class="section"><div class="masonry">{photo_items}</div></section>
{cta("Need photos?",
     "Tell us the occasion and roughly when. You'll hear back with availability and a real quote, usually within a business day.",
     btn_label="Book a shoot", subject="Photography inquiry")}''',
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
{cta("The next one could be yours.",
     "Tell us what you're making. You'll get straight answers, a plan, and a real quote — usually within a business day.")}''',
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
        <p>Straight answers, a plan, and a real quote — usually within a business day.
        A sentence is enough to start; you don't need the whole thing figured out.</p>
      </div>
      <p class="mailrow reveal">{mailto("Project inquiry", "Write to us directly")}
        <span class="mailaddr">{EMAIL}</span></p>
      <ol class="steps reveal">
        <li><span>1</span> You write — a line about what you're making.</li>
        <li><span>2</span> We reply within a business day with questions and a plan.</li>
        <li><span>3</span> You get a fixed quote and a date. The date holds.</li>
      </ol>
      <div class="prose reveal">
        <p>Phoenix, Arizona — filming across the Valley and statewide.</p>
        <p class="fsoc">{" · ".join(f'<a href="{u}" rel="me noopener" target="_blank">{n}</a>' for n,u in SOCIALS.items())}</p>
      </div>
    </div>
    <form class="form reveal" id="contactForm" action="https://formsubmit.co/{NOTIFY}" method="POST">
      <input type="hidden" name="_subject" value="New project inquiry — lightbox-digital.com">
      <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
      <label>Name <input name="name" required autocomplete="name" placeholder="Your name"></label>
      <label>Email <input type="email" name="email" required autocomplete="email" placeholder="you@company.com"></label>
      <label>What are we making? <select name="project">
        <option>Commercial</option><option>Landing video</option><option>Social content</option>
        <option>Interview</option><option>Event</option><option>Drone</option>
        <option>AI video</option><option>Photography</option><option>Something else</option></select></label>
      <label>Tell us about it <textarea name="message" rows="5" required
        placeholder="What it's for, roughly when, and anything you already know about budget. A couple of sentences is plenty."></textarea></label>
      <button class="btn" type="submit">Send</button>
      <p class="form-status" id="formStatus" role="status" aria-live="polite"></p>
      <p class="formnote">Goes straight to Josh. No newsletter, no follow-up sequence.</p>
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
    sm.append(f"<url><loc>{loc}</loc><lastmod>2026-07-10</lastmod><priority>{pri.get(p,'0.8')}</priority></url>")
sm.append("</urlset>")
(ROOT/"sitemap.xml").write_text("\n".join(sm))

AI_BOTS = ["GPTBot","OAI-SearchBot","ChatGPT-User","ClaudeBot","Claude-SearchBot","Claude-User",
           "PerplexityBot","Perplexity-User","Google-Extended","Applebot-Extended","CCBot",
           "meta-externalagent","Bytespider","Amazonbot","DuckAssistBot"]
robots = "User-agent: *\nAllow: /\n\n"
robots += "".join(f"User-agent: {b}\nAllow: /\n\n" for b in AI_BOTS)
robots += f"Sitemap: {BASE}/sitemap.xml\n"
(ROOT/"robots.txt").write_text(robots)

faq_txt = "\n".join(f"**{q}**\n{a}\n" for q, a in FAQ)
svc_txt = "\n".join(f"- **{t}** — {d}" for t, d in SERVICES)
rev_txt = "\n".join(f'- "{t}" — {n}, Google review (5 stars)' for n, t in REVIEWS[:6])
(ROOT/"llms.txt").write_text(f"""# Lightbox Digital

> Video production company and photography studio in Phoenix, Arizona, founded and run by
> Josh Chappell. Makes commercials, brand story films, landing and recruitment videos,
> social content, interview and testimonial videos, event films, FAA Part 107 licensed
> drone footage, AI-generated commercials, and business photography.
> Rated 5.0 across {len(REVIEWS)} Google reviews.

Contact: {EMAIL}
Website: {BASE}/
Service area: Phoenix, Scottsdale, Mesa, Tempe, Chandler, Gilbert, Glendale, and all of Arizona (travel projects too).
How it works: one person answers your call, films your project, and cuts the final edit.
Pricing: quoted per project — the quote you get is the price you pay.

## Services
{svc_txt}

## Pages
- [Home]({BASE}/): demo reel, selected work, services, FAQ
- [Work]({BASE}/work.html): {len(WORK)+1} films — commercials, stories, events & spaces, AI
- [AI Videos]({BASE}/ai-videos.html): AI-generated commercials, incl. "Dave's Garage"
- [Photography]({BASE}/photography.html): headshots, brand, school portraits, sports, events
- [About]({BASE}/about.html): the studio, founded by Josh Chappell
- [Reviews]({BASE}/reviews.html): {len(REVIEWS)} five-star Google reviews
- [Contact]({BASE}/contact.html): inquiry form — replies within a business day

## Notable clients & projects
Grand Canyon University, Blandford Homes, Butterfly Wonderland, Baths For The Brave,
Arrowhead Lakes Dentistry, Applied Tech, Allen Land & Fire, NCAA event coverage.

## Frequently asked questions
{faq_txt}
## What clients say
{rev_txt}
""")
print("wrote sitemap.xml, robots.txt, llms.txt")

# ------------------------------------------- private marketing dashboard ---
# Not linked, not in the sitemap, not in llms.txt, and marked noindex — so it
# has no effect on search or AI-answer results.

def audit(src):
    t = re.search(r"<title>(.*?)</title>", src, re.S)
    d = re.search(r'<meta name="description" content="(.*?)">', src, re.S)
    m = re.search(r'<main id="main">(.*)</main>', src, re.S)
    txt = re.sub(r"<script.*?</script>", " ", m.group(1) if m else src, flags=re.S)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", txt))
    imgs = re.findall(r"<img\s[^>]*>", src)
    ld = re.search(r'application/ld\+json">(.*?)</script>', src, re.S)
    types = []
    if ld:
        try:
            types = sorted({str(e.get("@type", "?")) for e in json.loads(ld.group(1))["@graph"]})
        except Exception:
            pass
    return {"title": html.unescape(t.group(1)) if t else "",
            "desc": html.unescape(d.group(1)) if d else "",
            "h1": len(re.findall(r"<h1[^>]*>", src)),
            "words": len(txt.split()), "imgs": len(imgs),
            "alts": len([i for i in imgs if re.search(r'alt="[^"]', i)]),
            "schema": types,
            "links": len(set(re.findall(r'href="([a-z0-9\-]+\.html)"', src))),
            "ctas": len(re.findall(r'class="btn"', src)),
            "mailto": len(re.findall(r'href="mailto:', src)),
            "kb": round(len(src.encode()) / 1024, 1)}

AUD = {f: audit(s) for f, s in W.items() if f not in REDIRECTS and f != "404.html"}
band = lambda n, lo, hi: "g" if lo <= n <= hi else "w"

seo_rows = "".join(
    f"<tr><td class='pg'>{f}</td>"
    f"<td class='{band(len(a['title']),30,65)}'>{len(a['title'])}</td>"
    f"<td class='{band(len(a['desc']),70,165)}'>{len(a['desc'])}</td>"
    f"<td class='{'g' if a['words']>=250 else 'w'}'>{a['words']}</td>"
    f"<td class='{'g' if a['h1']==1 else 'w'}'>{a['h1']}</td>"
    f"<td class='{'g' if a['alts']==a['imgs'] else 'w'}'>{a['alts']}/{a['imgs']}</td>"
    f"<td>{len(a['schema'])}</td><td>{a['links']}</td><td>{a['kb']}</td></tr>"
    for f, a in AUD.items())

conv_rows = "".join(
    f"<tr><td class='pg'>{f}</td><td class='{'g' if a['ctas'] else 'w'}'>{a['ctas']}</td>"
    f"<td class='{'g' if a['mailto'] else 'w'}'>{a['mailto']}</td>"
    f"<td>{'form + email' if f=='contact.html' else 'email'}</td></tr>"
    for f, a in AUD.items())

vid_rows = "".join(
    f"<tr><td class='pg'>{esc(v['title'])}</td><td>{CATNAME.get(v['cat'],'Reel')}</td>"
    f"<td>{v['date']}</td><td>{str(v['dur'])+'s' if v['dur'] else '—'}</td>"
    f"<td>{'self-hosted' if v['file'] else 'Vimeo'}</td></tr>"
    for v in [REEL] + WORK)

all_schema = sorted({t for a in AUD.values() for t in a["schema"]})
total_words = sum(a["words"] for a in AUD.values())
total_ctas = sum(a["ctas"] for a in AUD.values())
total_mail = sum(a["mailto"] for a in AUD.values())
llms_kb = round(len((ROOT / "llms.txt").read_text().encode()) / 1024, 1)
sitemap_n = (ROOT / "sitemap.xml").read_text().count("<url>")
built = datetime.datetime.now().strftime("%b %d, %Y at %H:%M")

CHECKLIST = [
    ("Google Business Profile — the single biggest lever for \"video production near me\"",
     "https://business.google.com/"),
    ("Google Search Console — submit sitemap.xml, watch real search queries",
     "https://search.google.com/search-console"),
    ("Bing Webmaster Tools — also feeds ChatGPT and Copilot search results",
     "https://www.bing.com/webmasters"),
    ("Google Analytics 4 — create a property, paste the ID into build.py",
     "https://analytics.google.com/"),
]
check_items = "".join(
    f'<li><label><input type="checkbox" data-k="c{i}"> {esc(t)}</label>'
    f' <a href="{u}" target="_blank" rel="noopener">open →</a></li>'
    for i, (t, u) in enumerate(CHECKLIST))

dash_css = """
<style>
.dash{max-width:1180px;margin:0 auto;padding:2.5rem clamp(1rem,4vw,2.2rem) 4rem}
.dash h1{font-size:clamp(1.9rem,4vw,2.8rem);margin-bottom:.4rem}
.dash .sub{font-family:var(--mono);font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.dblock{margin-top:3rem}
.dblock > h2{font-family:var(--mono);font-size:.74rem;letter-spacing:.18em;text-transform:uppercase;
  color:var(--amber);border-bottom:1px dashed rgba(232,176,75,.3);padding-bottom:.55rem;margin-bottom:1.2rem}
.dnote{color:var(--muted);font-size:.88rem;max-width:52rem;line-height:1.6;margin-bottom:1.1rem}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1rem}
.card{border:1px solid var(--line);background:var(--film);padding:1.1rem 1.2rem}
.card b{display:block;font-family:var(--display);font-size:1.9rem;color:var(--cream);line-height:1.1}
.card span{font-family:var(--mono);font-size:.64rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
table.d{width:100%;border-collapse:collapse;font-family:var(--mono);font-size:.76rem}
table.d th{text-align:left;font-weight:500;color:var(--amber);letter-spacing:.1em;text-transform:uppercase;
  font-size:.62rem;padding:.5rem .6rem;border-bottom:1px solid var(--line)}
table.d td{padding:.5rem .6rem;border-bottom:1px solid rgba(240,233,220,.06);color:#cfc6b8}
table.d td.pg{color:var(--cream)}
table.d td.g{color:#7fb069}table.d td.w{color:var(--amber)}
table.d td.bad{color:var(--red)}
.scroll{overflow-x:auto}
.status{display:inline-block;font-family:var(--mono);font-size:.66rem;letter-spacing:.1em;text-transform:uppercase;
  padding:.3rem .7rem;border:1px solid var(--line)}
.status.on{color:#7fb069;border-color:rgba(127,176,105,.4)}
.status.off{color:var(--amber);border-color:rgba(232,176,75,.35)}
.chk{list-style:none;padding:0;display:grid;gap:.8rem}
.chk li{display:flex;gap:.8rem;align-items:baseline;flex-wrap:wrap;font-size:.9rem;color:#cfc6b8}
.chk label{display:flex;gap:.6rem;align-items:baseline;cursor:pointer;flex:1;min-width:16rem}
.chk a{font-family:var(--mono);font-size:.68rem;color:var(--amber)}
.chk input:checked + *,.chk label:has(:checked){opacity:.45;text-decoration:line-through}
.tiny{font-family:var(--mono);font-size:.66rem;letter-spacing:.08em;color:var(--muted);text-transform:uppercase}
.setup{border:1px solid var(--line);background:var(--film);padding:1.2rem 1.3rem;margin-top:1rem}
.setup ol{margin:.7rem 0 0 1.1rem;color:#cfc6b8;font-size:.9rem;line-height:1.8}
.setup code{font-family:var(--mono);font-size:.8rem;color:var(--amber);background:#0a0806;padding:.15rem .4rem}
.cfgrow{display:grid;gap:.9rem;margin-top:1.1rem;max-width:34rem}
.cfgrow label{display:grid;gap:.35rem;font-family:var(--mono);font-size:.64rem;letter-spacing:.12em;
  text-transform:uppercase;color:var(--amber)}
.cfgrow input{background:#0a0806;border:1px solid var(--line);color:var(--cream);padding:.6rem .7rem;
  font-family:var(--mono);font-size:.8rem}
.cfgrow input:focus{outline:2px solid var(--amber);border-color:transparent}
.spark{width:100%;height:66px;display:block;margin:1.4rem 0 .3rem}
.spark polyline{fill:none;stroke:var(--amber);stroke-width:2;vector-effect:non-scaling-stroke}
.spark path{fill:rgba(232,176,75,.10);stroke:none}
.err{color:var(--red);font-family:var(--mono);font-size:.72rem;line-height:1.6}
.evrow strong{color:var(--amber)}
details.ref summary{font-family:var(--mono);font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;
  color:var(--muted);cursor:pointer;padding:.5rem 0}
details.ref[open] summary{color:var(--amber)}
</style>"""

dash_js = """
<script>
(function(){
  var PAGES = __PAGES__, ASSETS = __ASSETS__;
  var tb = document.getElementById('liveRows'), sum = document.getElementById('liveSum');
  async function check(u){
    var t0 = performance.now();
    try{
      var r = await fetch(u, {cache:'no-store'});
      var b = await r.blob();
      return {u:u, ok:r.ok, s:r.status, ms:Math.round(performance.now()-t0), kb:b.size/1024};
    }catch(e){ return {u:u, ok:false, s:'ERR', ms:0, kb:0}; }
  }
  async function run(){
    tb.innerHTML = '<tr><td colspan="4">checking…</td></tr>';
    var all = PAGES.concat(ASSETS), out = [], totalKb = 0, slowest = 0;
    for (var i=0;i<all.length;i++){
      var r = await check(all[i]);
      out.push(r); totalKb += r.kb; if (r.ms > slowest) slowest = r.ms;
    }
    tb.innerHTML = out.map(function(r){
      return '<tr><td class="pg">'+r.u+'</td><td class="'+(r.ok?'g':'bad')+'">'+(r.ok?'200 OK':r.s)+
             '</td><td>'+r.kb.toFixed(1)+'</td><td>'+r.ms+'</td></tr>';
    }).join('');
    var bad = out.filter(function(r){return !r.ok;}).length;
    sum.textContent = out.length+' resources · '+totalKb.toFixed(0)+' KB total · slowest '+slowest+
                      ' ms · '+(bad? bad+' FAILING':'all reachable');
    sum.className = 'tiny' + (bad ? ' bad' : '');
  }
  document.getElementById('recheck').addEventListener('click', run);
  run();

  // gtag.js registers each measurement ID on window.google_tag_manager, whether
  // it arrived directly or through a GTM container — so a G- key means GA4 is
  // genuinely loaded and collecting, not merely that a container exists.
  var reg = window.google_tag_manager || {};
  var gaIds = Object.keys(reg).filter(function(k){ return /^G-/.test(k); });
  var gtmIds = Object.keys(reg).filter(function(k){ return /^GTM-/.test(k); });
  var live = gaIds.length > 0;
  var el = document.getElementById('gaStatus');
  el.textContent = live ? ('Collecting — ' + gaIds.join(', '))
                        : (gtmIds.length ? 'Tag Manager loaded, no GA4 tag inside it'
                                         : 'Nothing connected yet');
  el.className = 'status ' + (live ? 'on' : 'off');

  // navigation timing is only final after the load event
  function showLoad(){
    var nav = performance.getEntriesByType('navigation')[0];
    var ms = (nav && nav.duration) ? nav.duration : performance.now();
    document.getElementById('loadMs').textContent = Math.round(ms) + ' ms';
  }
  if (document.readyState === 'complete') showLoad();
  else addEventListener('load', function(){ setTimeout(showLoad, 0); });

  document.querySelectorAll('.chk input').forEach(function(box){
    var k = 'lbx-' + box.dataset.k;
    try{ box.checked = localStorage.getItem(k) === '1'; }catch(e){}
    box.addEventListener('change', function(){
      try{ localStorage.setItem(k, box.checked ? '1' : '0'); }catch(e){}
    });
  });
})();
</script>"""

dash_js = (dash_js
           .replace("__PAGES__", json.dumps(list(AUD.keys())))
           .replace("__ASSETS__", json.dumps(["css/style.css", "js/main.js", "sitemap.xml",
                                              "robots.txt", "llms.txt",
                                              "assets/video/hero-720.mp4"])))

ga_js = """
<script src="https://accounts.google.com/gsi/client" async defer></script>
<script>
(function(){
  var K = { prop:'lbx-ga-prop', client:'lbx-ga-client' };
  var $ = function(i){ return document.getElementById(i); };
  var cfg = { prop:'', client:'' }, token = null;

  function get(k, fb){ try { return localStorage.getItem(k) || fb || ''; } catch(e){ return fb || ''; } }
  function loadCfg(){ cfg.prop = get(K.prop, '__PROP__'); cfg.client = get(K.client, '__CLIENT__'); }
  function say(msg, ok){ var e = $('gaErr'); e.className = ok ? 'tiny' : 'err'; e.textContent = msg || ''; }
  function paint(){
    var ready = !!(cfg.prop && cfg.client);
    $('gaCfg').hidden = ready;
    $('gaAuthRow').hidden = !ready || !!token;
    $('gaData').hidden = !token;
    if (cfg.prop) $('cfgProp').value = cfg.prop;
    if (cfg.client) $('cfgClient').value = cfg.client;
  }

  $('cfgSave').addEventListener('click', function(){
    var pr = $('cfgProp').value.trim().replace(/[^0-9]/g,'');
    var cl = $('cfgClient').value.trim();
    if (!pr || !cl) { say('Both IDs are needed.'); return; }
    try { localStorage.setItem(K.prop, pr); localStorage.setItem(K.client, cl); } catch(e){}
    cfg.prop = pr; cfg.client = cl; say(''); paint();
  });
  $('gaReset').addEventListener('click', function(e){
    e.preventDefault();
    try { localStorage.removeItem(K.prop); localStorage.removeItem(K.client); } catch(x){}
    cfg = { prop:'', client:'' }; token = null; say(''); paint();
  });

  function auth(next){
    if (!(window.google && google.accounts && google.accounts.oauth2)) {
      say("Google's sign-in library did not load — check the connection and reload."); return;
    }
    try {
      google.accounts.oauth2.initTokenClient({
        client_id: cfg.client,
        scope: 'https://www.googleapis.com/auth/analytics.readonly',
        callback: function(r){
          if (r.error) { say('Sign-in failed: ' + r.error); return; }
          token = r.access_token; say(''); paint(); next();
        }
      }).requestAccessToken();
    } catch(e){ say('Could not start sign-in: ' + e.message); }
  }

  async function api(method, body){
    var r = await fetch('https://analyticsdata.googleapis.com/v1beta/properties/' + cfg.prop + ':' + method, {
      method:'POST',
      headers:{ Authorization:'Bearer ' + token, 'Content-Type':'application/json' },
      body: JSON.stringify(body)
    });
    if (!r.ok) throw new Error('HTTP ' + r.status + ' — ' + (await r.text()).slice(0,240));
    return r.json();
  }

  var M = function(a){ return a.map(function(n){ return { name:n }; }); };
  var RANGE = [{ startDate:'28daysAgo', endDate:'today' }];
  function val(res,row,i){ try { return res.rows[row].metricValues[i].value; } catch(e){ return '0'; } }
  function dim(res,row,i){ try { return res.rows[row].dimensionValues[i].value; } catch(e){ return ''; } }
  function num(v){ return Number(v||0).toLocaleString(); }
  function mins(sec){ sec = Math.round(Number(sec)||0); return Math.floor(sec/60)+'m '+('0'+(sec%60)).slice(-2)+'s'; }
  function esc(s){ return String(s).replace(/[&<>]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c]; }); }
  function card(b,s){ return '<div class="card"><b>'+b+'</b><span>'+s+'</span></div>'; }
  function table(head, rows, cols){
    return '<div class="scroll"><table class="d"><thead><tr>' +
      head.map(function(h){ return '<th>'+h+'</th>'; }).join('') + '</tr></thead><tbody>' +
      (rows || '<tr><td colspan="'+cols+'">Nothing recorded in this window yet.</td></tr>') +
      '</tbody></table></div>';
  }
  function spark(rows){
    if (!rows || !rows.length) return '';
    var v = rows.map(function(r){ return Number(r.metricValues[0].value)||0; });
    var max = Math.max.apply(null, v) || 1, n = v.length;
    var pts = v.map(function(x,i){ return (i/((n-1)||1)*100).toFixed(2)+','+(100-x/max*100).toFixed(2); });
    return '<svg class="spark" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">'
         + '<path d="M0,100 L'+pts.join(' L')+' L100,100 Z"/>'
         + '<polyline points="'+pts.join(' ')+'"/></svg>';
  }

  async function refresh(){
    say('Fetching from Google Analytics…', true);
    try {
      var r = await Promise.all([
        api('runReport', { dateRanges:RANGE, metrics:M(['activeUsers','newUsers','sessions','screenPageViews','bounceRate','averageSessionDuration']) }),
        api('runReport', { dateRanges:RANGE, dimensions:M(['date']), metrics:M(['activeUsers']), orderBys:[{ dimension:{ dimensionName:'date' } }] }),
        api('runReport', { dateRanges:RANGE, dimensions:M(['pagePath']), metrics:M(['screenPageViews','bounceRate']), limit:10, orderBys:[{ metric:{ metricName:'screenPageViews' }, desc:true }] }),
        api('runReport', { dateRanges:RANGE, dimensions:M(['sessionDefaultChannelGroup']), metrics:M(['sessions']), limit:8, orderBys:[{ metric:{ metricName:'sessions' }, desc:true }] }),
        api('runReport', { dateRanges:RANGE, dimensions:M(['eventName']), metrics:M(['eventCount']), limit:15, orderBys:[{ metric:{ metricName:'eventCount' }, desc:true }] }),
        api('runRealtimeReport', { metrics:M(['activeUsers']) })
      ]);
      var tot=r[0], day=r[1], pages=r[2], src=r[3], ev=r[4], rt=r[5];

      $('gaCards').innerHTML =
        card(num(val(tot,0,0)), 'Visitors · 28 days') +
        card(num(val(tot,0,1)), 'First-time') +
        card(num(val(tot,0,2)), 'Sessions') +
        card(num(val(tot,0,3)), 'Page views') +
        card((Number(val(tot,0,4))*100).toFixed(1)+'%', 'Bounce rate') +
        card(mins(val(tot,0,5)), 'Average visit') +
        card(num(val(rt,0,0)), 'On the site now');

      $('gaSpark').innerHTML = spark(day.rows) + '<p class="tiny">Visitors per day · last 28 days</p>';

      $('gaPages').innerHTML = table(['Page','Views','Bounce'],
        (pages.rows||[]).map(function(_,i){
          return '<tr><td class="pg">'+esc(dim(pages,i,0))+'</td><td>'+num(val(pages,i,0))+
                 '</td><td>'+(Number(val(pages,i,1))*100).toFixed(0)+'%</td></tr>'; }).join(''), 3);

      $('gaSrc').innerHTML = table(['How they found you','Sessions'],
        (src.rows||[]).map(function(_,i){
          return '<tr><td class="pg">'+esc(dim(src,i,0))+'</td><td>'+num(val(src,i,0))+'</td></tr>';
        }).join(''), 2);

      var LABEL = { email_click:'Clicked your email address', generate_lead:'Sent the contact form',
                    cta_click:'Pressed a button', video_play:'Played a film' };
      $('gaEv').innerHTML = table(['What visitors did','Times'],
        (ev.rows||[]).map(function(_,i){
          var n = dim(ev,i,0), l = LABEL[n];
          return '<tr class="evrow"><td class="pg">'+(l ? '<strong>'+l+'</strong> — ' : '')+esc(n)+
                 '</td><td>'+num(val(ev,i,0))+'</td></tr>'; }).join(''), 2);

      $('gaMeta').textContent = 'Property ' + cfg.prop + ' · last 28 days · pulled ' + new Date().toLocaleTimeString();
      say('');
    } catch(e){
      var m = String(e.message || e);
      if (m.indexOf('403') > -1) m += '   That usually means the Analytics Data API is not enabled in the Cloud project, or this Google account cannot read that property.';
      if (m.indexOf('401') > -1) m += '   The sign-in expired — click "Show my numbers" again.';
      if (m.indexOf('404') > -1) m += '   Check the Property ID: it is the numeric one in Admin › Property settings, not the G- code.';
      say(m);
    }
  }

  $('gaSignIn').addEventListener('click', function(){ auth(refresh); });
  $('gaRefresh').addEventListener('click', function(){ token ? refresh() : auth(refresh); });
  loadCfg(); paint();
})();
</script>
"""
ga_js = ga_js.replace("__PROP__", GA4_PROPERTY_ID).replace("__CLIENT__", OAUTH_CLIENT_ID)

dash_body = f'''{dash_css}
<section class="dash">
  <p class="sub">Private · not indexed · not linked from the site</p>
  <h1>Studio dashboard</h1>
  <p class="sub">Built {built} · rebuilt every time the site deploys</p>

  <div class="dblock">
    <h2>At a glance</h2>
    <div class="cards">
      <div class="card"><b>{len(AUD)}</b><span>Live pages</span></div>
      <div class="card"><b>{len([REEL])+len(WORK)}</b><span>Films published</span></div>
      <div class="card"><b>{len(PHOTOS)}</b><span>Photos</span></div>
      <div class="card"><b>{len(REVIEWS)}</b><span>5★ reviews</span></div>
      <div class="card"><b>{total_words:,}</b><span>Indexable words</span></div>
      <div class="card"><b>{total_ctas}</b><span>Calls to action</span></div>
      <div class="card"><b>{total_mail}</b><span>Email links</span></div>
      <div class="card"><b>{sitemap_n}</b><span>URLs in sitemap</span></div>
    </div>
  </div>

  <div class="dblock">
    <h2>Live site check</h2>
    <p class="dnote">Runs in your browser every time you open this page — it actually fetches each
    page and asset from the live site, so a broken link or a bloated file shows up here first.
    This page loaded in <strong id="loadMs">—</strong>.</p>
    <p><button class="btn" id="recheck" type="button">Re-run checks</button></p>
    <div class="scroll"><table class="d">
      <thead><tr><th>Resource</th><th>Status</th><th>KB</th><th>ms</th></tr></thead>
      <tbody id="liveRows"></tbody>
    </table></div>
    <p class="tiny" id="liveSum" style="margin-top:.9rem"></p>
  </div>

  <div class="dblock">
    <h2>Traffic, bounce rate &amp; clicks</h2>
    <p><span id="gaStatus" class="status off">Checking…</span></p>

    <div class="setup" id="gaCfg" hidden>
      <p class="dnote" style="margin:0">The tag on your site <em>writes</em> data to Google Analytics.
      Pulling those numbers back onto this page needs two more IDs. Neither is a password — the figures
      only appear after you sign in with your Google account, so anyone else who opens this page sees
      an empty panel.</p>
      <ol>
        <li><strong>Property ID</strong> — in Analytics: <em>Admin › Property settings</em>. A plain
        number like <code>123456789</code>, not the G- code.</li>
        <li><strong>OAuth Client ID</strong> — at
        <a href="https://console.cloud.google.com/apis/credentials" target="_blank" rel="noopener">console.cloud.google.com</a>:
        make a project, enable the <em>Google Analytics Data API</em>, then
        <em>Credentials › Create credentials › OAuth client ID › Web application</em>. Under
        <em>Authorised JavaScript origins</em> add <code>https://lightbox-digital.com</code>.
        Copy the ID ending <code>.apps.googleusercontent.com</code>.</li>
      </ol>
      <div class="cfgrow">
        <label>GA4 Property ID <input id="cfgProp" placeholder="123456789" inputmode="numeric"></label>
        <label>OAuth Client ID <input id="cfgClient" placeholder="…apps.googleusercontent.com"></label>
        <p><button class="btn" id="cfgSave" type="button">Save</button></p>
      </div>
    </div>

    <p id="gaAuthRow" hidden><button class="btn" id="gaSignIn" type="button">Show my numbers</button>
      <span class="tiny" style="margin-left:1rem">Signs in with Google · read-only</span></p>

    <div id="gaData" hidden>
      <div class="cards" id="gaCards"></div>
      <div id="gaSpark"></div>
      <div class="dblock"><h2>Most-viewed pages</h2><div id="gaPages"></div></div>
      <div class="dblock"><h2>How they found you</h2><div id="gaSrc"></div></div>
      <div class="dblock"><h2>What they clicked</h2><div id="gaEv"></div></div>
      <p class="tiny" id="gaMeta" style="margin-top:1.2rem"></p>
      <p style="margin-top:.8rem"><button class="btn" id="gaRefresh" type="button">Refresh</button>
        <a href="#" id="gaReset" class="tiny" style="margin-left:1.2rem">reset connection</a></p>
    </div>

    <p id="gaErr" class="err" style="margin-top:1.1rem"></p>

    <details class="ref" style="margin-top:1.6rem">
      <summary>Where these numbers live inside Google Analytics itself</summary>
      <div class="scroll"><table class="d">
        <thead><tr><th>What you want to know</th><th>Where it shows up</th></tr></thead>
        <tbody>
          <tr><td class="pg">How many people came, and from where</td>
              <td>Reports › Acquisition › Traffic acquisition</td></tr>
          <tr><td class="pg">Bounce rate</td>
              <td>Reports › Engagement › Pages and screens — GA shows engagement rate; bounce is its mirror</td></tr>
          <tr><td class="pg">What people click</td>
              <td>Reports › Engagement › Events — <strong>email_click</strong>, <strong>cta_click</strong>,
              <strong>video_play</strong>, <strong>generate_lead</strong></td></tr>
          <tr><td class="pg">Which films get watched</td>
              <td>Events › <strong>video_play</strong> — one row per film title</td></tr>
          <tr><td class="pg">How many turned into an email</td>
              <td>Events › <strong>generate_lead</strong> and <strong>email_click</strong></td></tr>
        </tbody>
      </table></div>
      <p class="dnote" style="margin-top:1rem">Search Console answers a different question — what people
      typed into Google to find you, and where you rank:
      <a href="https://search.google.com/search-console" target="_blank" rel="noopener">search.google.com/search-console</a>.</p>
    </details>
  </div>

  <div class="dblock">
    <h2>Path to an email</h2>
    <p class="dnote">Every page ends with a way to reach you. This is the map of that — buttons that
    lead to the contact form, and one-tap email links that skip the form entirely.</p>
    <div class="scroll"><table class="d">
      <thead><tr><th>Page</th><th>Buttons</th><th>Email links</th><th>How they reach you</th></tr></thead>
      <tbody>{conv_rows}</tbody>
    </table></div>
  </div>

  <div class="dblock">
    <h2>Search health, page by page</h2>
    <p class="dnote">Green is in the ideal range, amber is worth a look. Title 30–65 characters,
    description 70–165, 250+ words of real copy, exactly one H1, every image with alt text.</p>
    <div class="scroll"><table class="d">
      <thead><tr><th>Page</th><th>Title len</th><th>Desc len</th><th>Words</th><th>H1</th>
      <th>Alt text</th><th>Schema</th><th>Links</th><th>KB</th></tr></thead>
      <tbody>{seo_rows}</tbody>
    </table></div>
  </div>

  <div class="dblock">
    <h2>AI answer-engine readiness</h2>
    <div class="cards">
      <div class="card"><b>{len(AI_BOTS)}</b><span>AI crawlers allowed</span></div>
      <div class="card"><b>{llms_kb} KB</b><span>llms.txt brief</span></div>
      <div class="card"><b>{len(FAQ)}</b><span>Q&amp;A pairs</span></div>
      <div class="card"><b>{len(all_schema)}</b><span>Schema types</span></div>
    </div>
    <p class="dnote" style="margin-top:1.1rem">Schema published across the site:
    {esc(", ".join(all_schema))}.</p>
  </div>

  <div class="dblock">
    <h2>Film inventory</h2>
    <div class="scroll"><table class="d">
      <thead><tr><th>Title</th><th>Category</th><th>Date</th><th>Length</th><th>Hosted</th></tr></thead>
      <tbody>{vid_rows}</tbody>
    </table></div>
  </div>

  <div class="dblock">
    <h2>Off-site setup — the things code can't do</h2>
    <p class="dnote">These live outside the website and move the needle more than anything on it.
    Ticks are saved in this browser.</p>
    <ul class="chk">{check_items}</ul>
  </div>
</section>
{dash_js}
{ga_js}'''

(ROOT / DASHBOARD).write_text(page(DASHBOARD, "Studio Dashboard — Lightbox Digital",
    "Private marketing dashboard.", dash_body, index=False))
print("wrote", DASHBOARD, "(private, noindex)")
