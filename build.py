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

# ---------------------------------------------------------------- videos ----
V = lambda id, title, dur, date, ind, blurb, h=None: dict(
    id=id, title=title, dur=dur, date=date, ind=ind, blurb=blurb, h=h)

VIDEOS = [
    # Education
    V("1004647238", "Incito 2022", 228, "2024-08-30", "education",
      "The full Incito 2022 recap — keynotes, hallway conversations, and the energy of a room full of people who wanted to be there."),
    V("1089338714", "GCU Worship Arts Program", None, "2025-06-01", "education",
      "A look inside GCU's Worship Arts program — made so prospective students could feel the place before visiting.", h="a33679bb7c"),
    V("1092229333", "IWE — Day in the Life", 105, "2025-06-10", "education",
      "One student's actual day, start to finish. The most honest enrollment pitch there is."),
    V("1092230232", "MNE Promo", 179, "2025-06-10", "education",
      "A school promo built around what families actually care about when they're choosing."),
    V("654280242", "Inspiring Teachers", 39, "2021-12-07", "education",
      "A short thank-you to the teachers who make a school worth choosing. Bring tissues."),
    V("1004652992", "President's Message", 61, "2024-08-30", "education",
      "A president's message that doesn't feel like a hostage video — real lighting, real audio, real warmth."),
    V("1004645760", "Construction Student Story", 69, "2024-08-30", "education",
      "A student who found her thing in a construction training program. Her story, her words."),
    # Construction / Trades / Industrial
    V("1004646002", "Treston × Cornerstone Ad", 73, "2024-08-30", "construction",
      "A spot for Treston and Cornerstone that puts the craftsmanship front and center."),
    V("1099054535", "Allen Land and Fire Commercial", 24, "2025-07-05", "construction",
      "Twenty-four seconds of heavy machinery doing satisfying things. For a land-clearing and fire-mitigation crew."),
    V("1103919211", "Applied Tech", 61, "2025-07-23", "construction",
      "Inside Applied Tech's world — the kind of technical work that's invisible until you film it right."),
    V("480986594", "Baths For The Brave — Dennis Sheffield", 271, "2020-11-18", "construction",
      "A veteran gets a donated bath remodel from the Baths For The Brave crew. Trades work with a lot of heart."),
    # Medical
    V("396854352", "Arrowhead Lakes Dentistry", 139, "2020-03-11", "medical",
      "A tour of Arrowhead Lakes Dentistry that makes the office feel familiar before your first visit."),
    V("960746274", "Rags To Riches Ad", 29, "2024-06-17", "medical",
      "Twenty-nine seconds, no wasted frames. Built to stop the scroll."),
    # Commercial / Everything Else
    V("1004647012", "Ad One", 79, "2024-08-30", "commercial",
      "A commercial taken from rough idea to finished cut, start to finish."),
    V("1041569506", "NCAA Coverage", 83, "2024-12-22", "commercial",
      "NCAA event coverage, shot for broadcast and social at the same time."),
    V("385325737", "Blandford Homes — Estates at Mandarin Grove", 119, "2020-01-16", "commercial",
      "A walkthrough of Blandford Homes' Estates at Mandarin Grove — luxury real estate, treated like cinema."),
    V("882198847", "Butterfly Wonderland", None, "2023-11-01", "commercial",
      "America's largest butterfly conservatory. Some days this job doesn't feel like work.", h="b06b5e4591"),
    V("705537712", "Oculus Giveaway", 114, "2022-05-02", "commercial",
      "A giveaway campaign for an Oculus headset that people actually shared."),
]

PHOTOS = [
    ("family-portrait-hug.jpg", "Candid family portrait of a couple hugging, natural light"),
    ("school-portrait.jpg", "Professional school portrait of a smiling student"),
    ("portrait_2", ""),  # placeholder replaced below
]
PHOTOS = [
    ("studio-portrait-1.jpg", "Studio portrait with dramatic professional lighting"),
    ("family-portrait-hug.jpg", "Candid family portrait of a couple hugging outdoors"),
    ("football-action.jpg", "High-speed football action shot at a Phoenix game"),
    ("school-portrait.jpg", "Professional school portrait of a smiling student"),
    ("ocean-landscape.jpg", "Dramatic ocean landscape photography"),
    ("studio-portrait-2.jpg", "Clean corporate headshot on studio backdrop"),
    ("posed-portrait.png", "Posed editorial portrait with styled lighting"),
    ("studio-portrait-3.jpg", "Environmental portrait with cinematic color grade"),
    ("relaxed-portrait.jpg", "Relaxed natural-light lifestyle portrait"),
    ("gorilla-wildlife.jpg", "Wildlife photography — gorilla portrait"),
    ("school-event.jpg", "School event photography, students engaged in activities"),
    ("classroom-learning.jpg", "Documentary classroom photo of hands-on learning"),
    ("videography-bts.jpg", "Behind the scenes on a Lightbox Digital video shoot"),
]

REVIEWS = [
    ("Carissa Harris", "Josh was great to work with on my company's product launch video. From pre-shoot meetings, to coordinating on site at our factory and the studio, to delivering the final product, everything went smoothly. He took his time to get the best angles and best lighting. Everything went smoothly and the final product was exactly what we needed."),
    ("Jason Gillespie", "Josh is a fantastic video resource and is a pleasure to work with. He has excellent suggestions and quickly gets a grasp of the vision we have for each project. He's flexible, performs well under pressure, and delivers great finished products. I would highly recommend him."),
    ("Ashley Leslie", "Josh was an absolute pleasure to work with for the corporate videos we had created for a special event. He went above and beyond with our limited timeframe and was extremely communicative throughout the entire process! We highly recommend Josh Chappell Video and Photography!"),
    ("Olivia McFadden", "I really enjoyed working with Josh for a client video shoot. He was professional, prepared, and organized. The final videos looked amazing. I would 100% work with him again."),
    ("Ivy Coppo", "Josh is amazing! Talented, thoughtful on details and very creative. We used him at Blandford Homes to shoot our community video and it is one of my favorite videos we have."),
    ("Brian Gottlieb", "Josh is exceptional! We've worked with him for years during our Baths for the Brave bath crash. He captures the moment to perfection — I highly recommend!"),
    ("Sarah Gerber", "Amazing quality of work! Such professionally done photos and edited in a timely manner. Josh was incredibly professional and fun to work with. He did family photos for us with our 2 year old and 6 week old. They are precious photos."),
    ("Jake Price", "Josh was very easy to work with and quick to respond to emails. His video quality is outstanding!"),
    ("Kevin McKamey", "Josh took some great photos of our business workshop, refined the pictures and delivered them to us for quick review as promised. We appreciated his professional manner and quick response to our last minute request."),
    ("Melody Hudson", "Simply put, Josh's work is amazing! His creative vision mixed with his talent result in a partnership that produces great work to visually help tell our client's stories."),
    ("Esmeralda Acosta", "Very professional and knowledgeable. Totally recommend him."),
]

SERVICES = [
    ("Website Landing Videos", "The video at the top of your homepage is usually the first impression you make. I build ones that make people stick around — and actually click the button.", "M4 6h16v10H4z M8 20h8 M12 16v4"),
    ("Social Media Videos", "Short, scroll-stopping videos cut for each platform. The goal isn't likes — it's customers who remember you when they're ready to buy.", "M12 3v18 M3 12h18"),
    ("Commercial Ads", "Real commercials, from first idea to final cut. Big-agency polish without the big-agency invoice — and you talk to the same person the whole way through.", "M23 7l-7 5 7 5V7z M1 5h15v14H1z"),
    ("Professional Interviews", "Good lighting, clean audio, and questions that put people at ease. You'll come across exactly like the expert you are — even if you hate being on camera.", "M12 1a4 4 0 0 1 4 4v6a4 4 0 0 1-8 0V5a4 4 0 0 1 4-4z M19 10a7 7 0 0 1-14 0 M12 17v6"),
    ("Brand Photography", "Headshots, product shots, team photos — pictures that make your whole brand feel put-together, everywhere they show up.", "M23 19V8l-4 2V7H1v12h22z M12 13m-3 0a3 3 0 1 0 6 0a3 3 0 1 0-6 0"),
    ("Drone Videography", "FAA Part 107 licensed aerial footage that makes your project look epic. Legal, insured, and honestly just fun to watch.", "M12 2l3 7h7l-6 5 2 8-6-4-6 4 2-8-6-5h7z"),
    ("Event Recap Content", "Your event lasts a day — the video works for months. I catch the moments and testimonials that prove to everyone what they missed.", "M8 2v4 M16 2v4 M3 8h18 M3 4h18v18H3z"),
    ("Vertical + Standard Formats", "I shoot horizontal and vertical at the same time, so one shoot covers your website, YouTube, and Instagram — without paying for two.", "M7 2h10v20H7z M2 7h4v10H2z M18 7h4v10h-4z"),
]

INDUSTRIES = {
    "education": dict(
        slug="education.html", name="Education",
        img="education-speaker.jpg",
        tagline="Videos that help families say yes",
        h1="Education Video Production in Phoenix",
        desc="Video production for schools, universities, and training programs in Phoenix — campus stories and day-in-the-life films that actually grow enrollment.",
        long="Here's the thing about choosing a school: families decide with their hearts first, then find reasons to back it up. A good campus film, a day-in-the-life promo, a teacher spotlight — these let a student feel what it's like to belong before they ever visit. I've made this kind of video for universities, charter schools, and career training programs all over Arizona, and I've watched it move enrollment numbers."),
    "construction": dict(
        slug="construction.html", name="Construction, Trades & Industrial",
        img="construction-site.jpg",
        tagline="Show off the work. Win the bid.",
        h1="Construction & Industrial Video Production in Phoenix",
        desc="Video for contractors, trades, and industrial companies in Phoenix — job site footage, drone shots, and commercials that prove your work and win more bids.",
        long="Your best salesperson is the work you've already finished — most people just never get to see it. Commercial spots, project walkthroughs, recruiting videos, drone passes over an active job site: that's the proof your estimators wish they had in every meeting. I've filmed everything from excavation crews to high-tech manufacturing floors, and my job is simple — make the quality of your work impossible to miss."),
    "medical": dict(
        slug="medical.html", name="Medical",
        img="medical-shoot.jpg",
        tagline="Patients trust you before they meet you",
        h1="Medical Practice Video Production in Phoenix",
        desc="Video for medical and dental practices in Phoenix — practice tours, provider intros, and patient stories that build trust before the first appointment.",
        long="Picking a doctor or dentist is personal — most patients are nervous before they ever call. A practice tour, a friendly provider intro, a real patient telling their story: these turn a stranger's website into a familiar place. New patients walk in already knowing your team, your office, and your vibe. That trust is worth more than any ad."),
    "commercial": dict(
        slug="commercial.html", name="Commercial & Everything Else",
        img="gimbal-operator.jpg",
        tagline="If it matters to you, it'll look amazing",
        h1="Commercial Video Production in Phoenix — Every Industry",
        desc="Real estate, attractions, events, product launches, nonprofits — commercial video production in Phoenix for every business with a story worth telling.",
        long="Not everything fits in a neat category — honestly, those are some of my favorite projects. Luxury home walkthroughs, a butterfly conservatory, NCAA event coverage, giveaway campaigns, nonprofit stories. Different worlds, same approach: figure out what makes it special, film it beautifully, and deliver it in the formats where your audience actually spends their time."),
}

# ------------------------------------------------------------- templates ----
FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">'

def esc(s): return html.escape(s, quote=True)

def nav(active):
    items = [("index.html","Home"),("portfolio.html","Our Work"),("photography.html","Photography"),
             ("about.html","About"),("reviews.html","Reviews")]
    links = "".join(f'<a href="{h}"{" class=active" if h==active else ""}>{t}</a>' for h,t in items)
    return f'''<header class="nav" id="nav">
  <a class="brand" href="index.html" aria-label="Lightbox Digital home"><img class="brand-logo" src="assets/img/logo-mark-dark.png" alt="" width="34" height="33"> LIGHTBOX <span>DIGITAL</span></a>
  <nav class="nav-links" id="navLinks" aria-label="Primary">{links}
    <div class="nav-drop"><button aria-haspopup="true" aria-expanded="false">Industries ▾</button>
      <div class="drop-menu">
        <a href="education.html">Education</a>
        <a href="construction.html">Construction &amp; Trades</a>
        <a href="medical.html">Medical</a>
        <a href="commercial.html">Everything Else</a>
      </div></div>
    <a href="contact.html" class="btn btn-sm">Let's Talk</a>
  </nav>
  <button class="burger" id="burger" aria-label="Open menu" aria-controls="navLinks" aria-expanded="false"><span></span><span></span><span></span></button>
</header>'''

def footer():
    soc = " ".join(f'<a href="{u}" rel="me noopener" target="_blank">{n}</a>' for n,u in SOCIALS.items())
    return f'''<footer class="footer">
  <div class="footer-grid">
    <div>
      <p class="brand"><img class="brand-logo" src="assets/img/logo-mark-dark.png" alt="" width="30" height="29"> LIGHTBOX <span>DIGITAL</span></p>
      <p>Phoenix photo + video production.<br>One-man film crew for businesses that want to look incredible.</p>
      <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
    <nav aria-label="Site"><h3>Site</h3>
      <a href="index.html">Home</a><a href="portfolio.html">Video Portfolio</a><a href="photography.html">Photography</a><a href="about.html">About Josh</a><a href="reviews.html">Reviews</a><a href="contact.html">Contact</a>
    </nav>
    <nav aria-label="Industries"><h3>Industries</h3>
      <a href="education.html">Education</a><a href="construction.html">Construction &amp; Trades</a><a href="medical.html">Medical</a><a href="commercial.html">Everything Else</a>
    </nav>
    <div><h3>Follow</h3><p class="soc">{soc}</p>
      <p>Serving Phoenix, Scottsdale, Mesa, Tempe, Chandler, Gilbert, Glendale &amp; all of Arizona.</p></div>
  </div>
  <p class="copy">© 2026 Joshua Chappell LLC · Lightbox Digital · Phoenix, Arizona</p>
</footer>
<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Video player" hidden>
  <button class="lb-close" id="lbClose" aria-label="Close video">✕</button>
  <div class="lb-frame" id="lbFrame"></div>
</div>
<script src="js/main.js" defer></script>'''

def video_card(v, lazy=True):
    dur = f"{v['dur']//60}:{v['dur']%60:02d}" if v['dur'] else ""
    h = f"?h={v['h']}" if v['h'] else ""
    load = ' loading="lazy"' if lazy else ""
    return f'''<article class="vcard reveal" data-ind="{v['ind']}">
  <button class="vthumb" data-vimeo="{v['id']}{h}" aria-label="Play video: {esc(v['title'])}">
    <img src="assets/thumbs/{v['id']}.jpg" alt="{esc(v['title'])} — video thumbnail" width="640" height="360"{load}>
    <span class="play" aria-hidden="true"></span>{f'<span class="dur">{dur}</span>' if dur else ''}
  </button>
  <h3>{esc(v['title'])}</h3>
  <p>{esc(v['blurb'])}</p>
</article>'''

def video_ld(vs):
    items = []
    for v in vs:
        d = {"@type":"VideoObject","name":v["title"],"description":v["blurb"],
             "thumbnailUrl":f"{BASE}/assets/thumbs/{v['id']}.jpg",
             "uploadDate":v["date"],
             "embedUrl":f"https://player.vimeo.com/video/{v['id']}" + (f"?h={v['h']}" if v['h'] else "")}
        if v["dur"]: d["duration"] = f"PT{v['dur']//60}M{v['dur']%60}S"
        items.append(d)
    return items

ORG = {
    "@type":"ProfessionalService",
    "@id": BASE+"/#org",
    "name":"Lightbox Digital",
    "alternateName":"Lightbox Digital — Phoenix Video Production",
    "description":"Phoenix video production and photography company. Commercial ads, website landing videos, social media content, drone videography, interviews, event coverage and brand photography for education, construction, medical and more.",
    "url": BASE+"/",
    "logo": BASE+"/assets/img/logo-lockup.png",
    "image": BASE+"/assets/img/hero-poster.jpg",
    "email": EMAIL,
    "founder":{"@type":"Person","name":"Josh Chappell","jobTitle":"Videographer & Photographer","sameAs":SOCIALS["Instagram"]},
    "address":{"@type":"PostalAddress","addressLocality":"Phoenix","addressRegion":"AZ","addressCountry":"US"},
    "areaServed":[{"@type":"City","name":n} for n in ["Phoenix","Scottsdale","Mesa","Tempe","Chandler","Gilbert","Glendale"]] + [{"@type":"State","name":"Arizona"}],
    "priceRange":"$$",
    "sameAs": list(SOCIALS.values()),
    "knowsAbout":["video production","commercial video","drone videography","brand photography","social media video","event videography","corporate interviews"],
    "aggregateRating":{"@type":"AggregateRating","ratingValue":"5.0","reviewCount":str(len(REVIEWS)),"bestRating":"5"},
}

def page(fname, title, desc, body, ld_extra=None, og_img="assets/img/hero-poster.jpg", bodycls=""):
    ld = [dict(ORG)]
    ld.append({"@type":"WebSite","name":"Lightbox Digital","url":BASE+"/","publisher":{"@id":BASE+"/#org"}})
    crumbs = [{"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"}]
    if fname != "index.html":
        crumbs.append({"@type":"ListItem","position":2,"name":title.split("|")[0].split("—")[0].strip(),"item":f"{BASE}/{fname}"})
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
<link rel="stylesheet" href="css/style.css">
<script type="application/ld+json">{ldjson}</script>
</head>
<body class="{bodycls}">
{nav(fname)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>'''

W = {}

# ------------------------------------------------------------------ home ----
FAQ = [
    ("What areas does Lightbox Digital serve?",
     "I'm based in Phoenix and work all over the Valley — Scottsdale, Mesa, Tempe, Chandler, Gilbert, Glendale. Somewhere further out in Arizona, or a travel project? Just ask."),
    ("What types of video do you produce?",
     "Commercials, website landing videos, social media clips, interviews, event recaps, and drone footage — plus brand photography and headshots. And I shoot horizontal and vertical at the same time, so one shoot covers every platform."),
    ("How much does video production cost?",
     "Honest answer: it depends on what we're making. A one-day social shoot and a multi-location commercial are very different projects. Tell me your goals and your budget, and I'll build something that fits — no surprise invoices, delivered when I said it would be."),
    ("Are you licensed for drone footage?",
     "Yep — FAA Part 107 certified for commercial drone work. So the aerial shots are legal, insured, and gorgeous."),
    ("Why does professional video matter for my business?",
     "Because people buy from businesses they trust, and nothing builds trust faster than seeing you in action. Video does the convincing before the first phone call — and one good shoot can feed your website, ads, and social feeds for months."),
]

featured_ids = ["1099054535","396854352","1092229333","385325737","480986594","1041569506"]
featured = [v for v in VIDEOS if v["id"] in featured_ids]

home_ind_cards = "".join(f'''<a class="icard reveal" href="{d['slug']}">
  <img src="assets/img/{d['img']}" alt="{esc(d['name'])} video production example" loading="lazy" width="600" height="400">
  <div class="icard-body"><h3>{esc(d['name'])}</h3><p>{esc(d['tagline'])}</p><span class="link">See examples →</span></div>
</a>''' for d in INDUSTRIES.values())

svc_cards = "".join(f'''<div class="scard reveal">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="{p}"/></svg>
  <h3>{esc(t)}</h3><p>{esc(d)}</p>
</div>''' for t,d,p in SERVICES)

faq_html = "".join(f'''<details class="faq reveal"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>''' for q,a in FAQ)

rev_strip = "".join(f'''<figure class="rquote"><p>“{esc(t[:180])}{'…' if len(t)>180 else ''}”</p><figcaption>— {esc(n)} <span class="stars" aria-label="5 star Google review">★★★★★</span></figcaption></figure>''' for n,t in REVIEWS[:6])

home_body = f'''
<section class="hero">
  <video class="hero-video" autoplay muted loop playsinline poster="assets/img/hero-poster.jpg" aria-hidden="true">
    <source src="assets/video/hero.mp4" type="video/mp4">
  </video>
  <div class="hero-overlay"></div>
  <div class="hero-inner">
    <p class="kicker reveal">Phoenix Video Production &amp; Photography</p>
    <h1 class="reveal">Get More Qualified Leads with <em>Premium Visual Storytelling</em></h1>
    <p class="lede reveal">I'm Josh — a one-man film crew in Phoenix. I make videos and photos people actually stop for, whether you run a school, a job site, a practice, or something entirely your own.</p>
    <div class="cta-row reveal">
      <a class="btn btn-lg" href="contact.html">Let's Make Something Awesome</a>
      <a class="btn btn-ghost btn-lg" href="portfolio.html">Watch Our Work</a>
    </div>
    <ul class="trust reveal" aria-label="Trust indicators">
      <li>★ 5.0 — {len(REVIEWS)} Google reviews</li><li>FAA Part 107 drone certified</li><li>Based in Phoenix, AZ</li>
    </ul>
  </div>
</section>

<section class="section">
  <p class="kicker reveal">Industries We Serve</p>
  <h2 class="reveal">Whatever you do, I'll make it look incredible</h2>
  <div class="igrid">{home_ind_cards}</div>
</section>

<section class="section section-alt">
  <p class="kicker reveal">Featured Work</p>
  <h2 class="reveal">Go ahead, press play</h2>
  <div class="vgrid">{"".join(video_card(v) for v in featured)}</div>
  <p class="center reveal"><a class="btn btn-ghost" href="portfolio.html">See the full portfolio →</a></p>
</section>

<section class="section">
  <p class="kicker reveal">What I Do</p>
  <h2 class="reveal">Everything you need, from one person who actually cares</h2>
  <div class="sgrid">{svc_cards}</div>
</section>

<section class="section section-alt">
  <p class="kicker reveal">Client Reviews</p>
  <h2 class="reveal">Don't take my word for it</h2>
  <div class="rstrip">{rev_strip}</div>
  <p class="center reveal"><a class="btn btn-ghost" href="reviews.html">Read all {len(REVIEWS)} reviews →</a></p>
</section>

<section class="section split">
  <img class="reveal" src="assets/img/josh-chappell.jpg" alt="Josh Chappell, owner and lead videographer of Lightbox Digital in Phoenix, Arizona" loading="lazy" width="500" height="640">
  <div>
    <p class="kicker reveal">Meet Your Videographer</p>
    <h2 class="reveal">I'm Josh Chappell — your business' new biggest fan</h2>
    <p class="reveal">Full-time visual storyteller, FAA Part 107 drone certified, and genuinely obsessed with other people's businesses. After years of filming for tech companies and schools around Phoenix, I fell in love with the entrepreneurial story — yours included. I show up prepared, deliver on time, and stay on budget. That shouldn't be rare, but here we are.</p>
    <p class="reveal"><a class="btn btn-ghost" href="about.html">More about Josh →</a></p>
  </div>
</section>

<section class="section section-alt">
  <p class="kicker reveal">FAQ</p>
  <h2 class="reveal">Things people usually ask me</h2>
  <div class="faqwrap">{faq_html}</div>
</section>

<section class="section cta-final">
  <h2 class="reveal">Let's make something awesome.</h2>
  <p class="reveal">Tell me what you've got in mind — I'll come back with ideas, a plan, and a real quote.</p>
  <a class="btn btn-lg reveal" href="contact.html">Start Your Project</a>
</section>'''

ld_home = [{"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}] + video_ld(featured)
W["index.html"] = page("index.html",
    "Phoenix Video Production & Photography | Lightbox Digital",
    "Award-quality video production in Phoenix, AZ. Commercial ads, drone footage, social content & brand photography that gets you more qualified leads. 5.0★ on Google.",
    home_body, ld_home)

# -------------------------------------------------------- industry pages ----
for key, d in INDUSTRIES.items():
    vids = [v for v in VIDEOS if v["ind"] == key]
    body = f'''
<section class="page-hero" style="background-image:url('assets/img/{d['img']}')">
  <div class="hero-overlay"></div>
  <div class="hero-inner">
    <p class="kicker reveal">Industry · {esc(d['name'])}</p>
    <h1 class="reveal">{esc(d['h1'])}</h1>
    <p class="lede reveal">{esc(d['desc'])}</p>
    <a class="btn btn-lg reveal" href="contact.html">Let's Make Something Awesome</a>
  </div>
</section>
<section class="section">
  <div class="prose reveal"><p>{esc(d['long'])}</p></div>
  <h2 class="reveal">See for yourself</h2>
  <div class="vgrid">{"".join(video_card(v) for v in vids)}</div>
</section>
<section class="section cta-final">
  <h2 class="reveal">Want something like this for your business?</h2>
  <p class="reveal">Tell me what you're picturing — I'll tell you what it takes.</p>
  <a class="btn btn-lg reveal" href="contact.html">Get a Quote</a>
</section>'''
    W[d["slug"]] = page(d["slug"],
        f"{d['h1']} | Lightbox Digital",
        d["desc"][:158],
        body, video_ld(vids), og_img=f"assets/img/{d['img']}")

# ------------------------------------------------------------- portfolio ----
filters = '<div class="filters reveal" role="group" aria-label="Filter videos">' + \
  '<button class="fbtn active" data-f="all">All</button>' + \
  "".join(f'<button class="fbtn" data-f="{k}">{esc(d["name"].split(",")[0].split(" &")[0])}</button>' for k,d in INDUSTRIES.items()) + '</div>'

port_body = f'''
<section class="page-hero small" style="background-image:url('assets/img/cinema-camera.jpg')">
  <div class="hero-overlay"></div>
  <div class="hero-inner">
    <h1 class="reveal">Video Portfolio</h1>
    <p class="lede reveal">{len(VIDEOS)} projects — schools, job sites, dental chairs, luxury homes, a butterfly conservatory. Sound on for the good stuff.</p>
  </div>
</section>
<section class="section">
  {filters}
  <div class="vgrid" id="vgrid">{"".join(video_card(v) for v in VIDEOS)}</div>
  <p class="center reveal">Looking for stills instead? <a href="photography.html">Browse the photography portfolio →</a></p>
</section>
<section class="section cta-final">
  <h2 class="reveal">Picture your business up there?</h2>
  <a class="btn btn-lg reveal" href="contact.html">Let's Make Something Awesome</a>
</section>'''
W["portfolio.html"] = page("portfolio.html",
    "Video Portfolio — Phoenix Video Production Examples | Lightbox Digital",
    "Watch real client work: commercials, brand films, drone footage, interviews & event videos produced in Phoenix, AZ by Lightbox Digital.",
    port_body, video_ld(VIDEOS), og_img="assets/img/cinema-camera.jpg")

# ----------------------------------------------------------- photography ----
photo_items = "".join(f'''<figure class="pitem reveal"><button class="pthumb" data-img="assets/img/{f}" aria-label="View photo: {esc(alt)}"><img src="assets/img/{f}" alt="{esc(alt)}" loading="lazy"></button></figure>''' for f,alt in PHOTOS)
ld_photos = [{"@type":"ImageGallery","name":"Lightbox Digital Photography Portfolio",
              "url":f"{BASE}/photography.html",
              "image":[f"{BASE}/assets/img/{f}" for f,_ in PHOTOS]}]
W["photography.html"] = page("photography.html",
    "Phoenix Photographer — Portraits, Events & Brand Photography | Lightbox Digital",
    "Professional photography in Phoenix, AZ: brand photography, headshots, portraits, school and event photography by Josh Chappell of Lightbox Digital.",
    f'''
<section class="page-hero small" style="background-image:url('assets/img/videography-bts.jpg')">
  <div class="hero-overlay"></div>
  <div class="hero-inner"><h1 class="reveal">Photography Portfolio</h1>
  <p class="lede reveal">Portraits, brand shoots, schools, sports, events — same eye as the films, one frame at a time.</p></div>
</section>
<section class="section"><div class="masonry">{photo_items}</div></section>
<section class="section cta-final"><h2 class="reveal">Need photos that make you look as good as you are?</h2>
<a class="btn btn-lg reveal" href="contact.html">Book a Shoot</a></section>''',
    ld_photos, og_img="assets/img/videography-bts.jpg")

# ----------------------------------------------------------------- about ----
ld_about = [{"@type":"Person","name":"Josh Chappell","jobTitle":"Videographer, Photographer & Founder",
             "worksFor":{"@id":BASE+"/#org"},"image":f"{BASE}/assets/img/josh-chappell.jpg",
             "email":f"mailto:{EMAIL}","sameAs":list(SOCIALS.values()),
             "address":{"@type":"PostalAddress","addressLocality":"Phoenix","addressRegion":"AZ"},
             "knowsAbout":["videography","photography","drone operation","visual storytelling"]}]
W["about.html"] = page("about.html",
    "About Josh Chappell — Phoenix Videographer & Photographer | Lightbox Digital",
    "Meet Josh Chappell: full-time visual storyteller, FAA Part 107 drone certified videographer and photographer behind Lightbox Digital in Phoenix, Arizona.",
    f'''
<section class="section split about-top">
  <img class="reveal" src="assets/img/josh-chappell.jpg" alt="Black and white portrait of Josh Chappell, Phoenix videographer and photographer" width="500" height="640">
  <div>
    <p class="kicker reveal">About Lightbox Digital</p>
    <h1 class="reveal">I'm Josh Chappell — Your Business' New Biggest Fan.</h1>
    <p class="lede reveal">Full-time visual storyteller. FAA Part 107 drone certified. Videographer, photographer, and creator.</p>
    <div class="prose">
      <p class="reveal">Through years of experience serving cutting-edge technology and educational corporations in Phoenix, I've fallen in love with the entrepreneurial story. I'm here to take your vision and transform it into a visual masterpiece — dedicated to delivering exactly what you want, on time and within budget.</p>
      <p class="reveal">I take pride in delivering videos with personality, character, and a real-life feel — striking a balance between professional and creative that represents your business goals.</p>
      <p class="reveal">The right videographer makes you stand out and reach your audience in a professional yet personal way. By capturing high-end, high-quality images of your business, you can turn up the volume on your reach, revenue, and reality.</p>
      <p class="reveal"><strong>With my lens in hand, I'm ready to capture your journey, frame by frame. Are you?</strong></p>
    </div>
    <a class="btn btn-lg reveal" href="contact.html">Work With Josh</a>
  </div>
</section>
<section class="section section-alt split">
  <div>
    <p class="kicker reveal">Behind the scenes</p>
    <h2 class="reveal">Boutique attention, big-agency craft</h2>
    <p class="reveal">One dedicated creative from first call to final cut — no handoffs, no telephone game. Professional cinema cameras, lighting, audio, and licensed drone work on every production.</p>
  </div>
  <img class="reveal" src="assets/img/bts-interview.jpg" alt="Behind the scenes of a Lightbox Digital interview shoot with professional lighting" loading="lazy" width="600" height="420">
</section>''',
    ld_about, og_img="assets/img/josh-chappell.jpg")

# --------------------------------------------------------------- reviews ----
rev_cards = "".join(f'''<figure class="rcard reveal">
  <div class="stars" aria-label="5 out of 5 stars">★★★★★</div>
  <blockquote><p>{esc(t)}</p></blockquote>
  <figcaption>{esc(n)} · <span>Google review</span></figcaption>
</figure>''' for n,t in REVIEWS)
ld_rev = [{"@type":"LocalBusiness","@id":BASE+"/#org","name":"Lightbox Digital",
           "image":BASE+"/assets/img/hero-poster.jpg",
           "address":{"@type":"PostalAddress","addressLocality":"Phoenix","addressRegion":"AZ","addressCountry":"US"},
           "aggregateRating":{"@type":"AggregateRating","ratingValue":"5.0","reviewCount":str(len(REVIEWS)),"bestRating":"5"},
           "review":[{"@type":"Review","reviewRating":{"@type":"Rating","ratingValue":"5","bestRating":"5"},
                      "author":{"@type":"Person","name":n},"reviewBody":t} for n,t in REVIEWS]}]
W["reviews.html"] = page("reviews.html",
    "Reviews — 5.0★ Rated Phoenix Video Production | Lightbox Digital",
    f"Read {len(REVIEWS)} five-star Google reviews for Lightbox Digital, Phoenix's trusted video production and photography company.",
    f'''
<section class="page-hero small" style="background-image:url('assets/img/bts-filming.jpg')">
  <div class="hero-overlay"></div>
  <div class="hero-inner"><h1 class="reveal">Client Reviews</h1>
  <p class="lede reveal">★★★★★ 5.0 across {len(REVIEWS)} Google reviews. Here's what people say about working with me.</p></div>
</section>
<section class="section"><div class="rgrid">{rev_cards}</div></section>
<section class="section cta-final"><h2 class="reveal">Let's earn the next one together.</h2>
<a class="btn btn-lg reveal" href="contact.html">Start Your Project</a></section>''',
    ld_rev, og_img="assets/img/bts-filming.jpg")

# --------------------------------------------------------------- contact ----
ld_contact = [{"@type":"ContactPage","name":"Contact Lightbox Digital","url":BASE+"/contact.html"}]
W["contact.html"] = page("contact.html",
    "Contact — Get a Video Production Quote in Phoenix | Lightbox Digital",
    "Tell us about your project and get a custom video production or photography quote. Lightbox Digital — Phoenix, AZ. Email josh.lightbox@gmail.com.",
    f'''
<section class="section split contact-wrap">
  <div>
    <p class="kicker reveal">Contact</p>
    <h1 class="reveal">Let's Make Something Awesome!</h1>
    <p class="lede reveal">Tell me what you're building. I'll come back with ideas, a plan, and a straightforward quote — usually within a business day.</p>
    <div class="prose reveal">
      <p><strong>Josh Chappell</strong><br>Lightbox Digital · Phoenix, Arizona<br>
      <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p class="soc">{" ".join(f'<a href="{u}" rel="me noopener" target="_blank">{n}</a>' for n,u in SOCIALS.items())}</p>
    </div>
    <img class="reveal contact-img" src="assets/img/cinema-camera.jpg" alt="Cinema camera used on Lightbox Digital productions" loading="lazy" width="600" height="400">
  </div>
  <form class="form reveal" action="https://formsubmit.co/{EMAIL}" method="POST">
    <input type="hidden" name="_subject" value="New project inquiry — lightbox-digital site">
    <input type="text" name="_honey" style="display:none">
    <label>Name <input name="name" required autocomplete="name"></label>
    <label>Email <input type="email" name="email" required autocomplete="email"></label>
    <label>Phone (optional) <input type="tel" name="phone" autocomplete="tel"></label>
    <label>What are we making? <select name="project">
      <option>Commercial / ad</option><option>Website landing video</option><option>Social media content</option>
      <option>Interview / testimonial</option><option>Event coverage</option><option>Drone footage</option>
      <option>Photography</option><option>Something else</option></select></label>
    <label>Tell us about your project <textarea name="message" rows="5" required></textarea></label>
    <button class="btn btn-lg" type="submit">Send Inquiry</button>
    <p class="fine">We typically reply within one business day.</p>
  </form>
</section>''',
    ld_contact)

# ------------------------------------------------------------------- 404 ----
W["404.html"] = page("404.html", "Page Not Found | Lightbox Digital",
    "That page has moved. Explore Lightbox Digital's Phoenix video production portfolio, services, and contact info.",
    '''<section class="section cta-final" style="min-height:55vh;display:flex;flex-direction:column;justify-content:center">
<h1>404 — that scene got cut.</h1><p>The page you're looking for moved or never made the final edit.</p>
<p><a class="btn btn-lg" href="index.html">Back to the homepage</a></p></section>''')

# ------------------------------------------------------------ write files ---
for f, htmlsrc in W.items():
    (ROOT / f).write_text(htmlsrc)
    print("wrote", f, len(htmlsrc)//1024, "KB")

# sitemap
pages = [p for p in W if p != "404.html"]
sm = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
pri = {"index.html":"1.0","portfolio.html":"0.9","contact.html":"0.9"}
for p in pages:
    loc = BASE+"/" if p=="index.html" else f"{BASE}/{p}"
    sm.append(f"<url><loc>{loc}</loc><lastmod>2026-07-03</lastmod><priority>{pri.get(p,'0.8')}</priority></url>")
sm.append("</urlset>")
(ROOT/"sitemap.xml").write_text("\n".join(sm))

(ROOT/"robots.txt").write_text(f"""User-agent: *
Allow: /

Sitemap: {BASE}/sitemap.xml
""")

(ROOT/"llms.txt").write_text(f"""# Lightbox Digital

> Phoenix, Arizona video production and photography company owned by Josh Chappell.
> Premium visual storytelling — commercial ads, website landing videos, social media
> content, professional interviews, event recaps, FAA Part 107 drone videography,
> and brand photography. Rated 5.0 with {len(REVIEWS)} Google reviews.

Contact: {EMAIL}
Service area: Phoenix, Scottsdale, Mesa, Tempe, Chandler, Gilbert, Glendale, and all of Arizona.

## Pages
- [Home]({BASE}/): services, industries, featured work, FAQ
- [Video Portfolio]({BASE}/portfolio.html): {len(VIDEOS)} client productions with Vimeo embeds
- [Education]({BASE}/education.html): enrollment-driving video for schools and universities
- [Construction, Trades & Industrial]({BASE}/construction.html): videos that win bids
- [Medical]({BASE}/medical.html): patient-trust videos for practices
- [Commercial & Everything Else]({BASE}/commercial.html): real estate, attractions, events
- [Photography]({BASE}/photography.html): portraits, brand, school, sports, events
- [About]({BASE}/about.html): Josh Chappell, FAA Part 107 certified videographer
- [Reviews]({BASE}/reviews.html): all {len(REVIEWS)} five-star Google reviews
- [Contact]({BASE}/contact.html): project inquiry form

## Notable clients & projects
Grand Canyon University, Blandford Homes, Butterfly Wonderland, Jacuzzi, Charter One,
Baths For The Brave, Arrowhead Lakes Dentistry, Applied Tech, NCAA event coverage.
""")

print("wrote sitemap.xml, robots.txt, llms.txt")
