# -*- coding: utf-8 -*-
"""Build the static site for gaviria.ca into ./docs (FR at /, EN at /en/, ES at /es/)."""
import os, shutil, html, json
from urllib.parse import quote
from content import CONTENT

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "docs")  # GitHub Pages publishes this folder
DOMAIN = "https://gaviria.ca/"
EMAIL = "alex@gaviria.ca"
PHONE = "+1 581 996 6149"
PHONE_TEL = "+15819966149"
LINKEDIN = "https://www.linkedin.com/in/alejandroalexgaviria/"
ORDER = ["fr", "en", "es"]
LANG_NAMES = {"fr": "FR", "en": "EN", "es": "ES"}
LANG_FULL = {"fr": "Français", "en": "English", "es": "Español"}

def e(s):
    return html.escape(s, quote=True)

def fr_typo(s):
    # French (Quebec) typography: non-breaking space before colon, inside guillemets
    return s.replace(" :", " :").replace("« ", "« ").replace(" »", " »")

ICONS = [
    '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1F3A5F" stroke-width="1.5" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="1"/><path d="M3 9h18M9 21V9"/></svg>',
    '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1F3A5F" stroke-width="1.5" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h10"/></svg>',
    '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1F3A5F" stroke-width="1.5" aria-hidden="true"><path d="M4 5h16v11H9l-5 4z"/></svg>',
    '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1F3A5F" stroke-width="1.5" aria-hidden="true"><path d="M6 3h9l3 3v15H6z"/><path d="M9 11h6M9 15h6"/></svg>',
]

def badge(label):
    # E2Y badge, paper colourway (for the blue method section)
    return (f'<svg class="badge" viewBox="0 0 120 120" role="img" aria-label="{e(label)}">'
            '<rect width="120" height="120" rx="2" fill="#F7F4EE"/>'
            '<text x="13" y="48" font-family="Source Serif 4, Georgia, serif" font-weight="600" font-size="40" fill="#14213D">E2</text>'
            '<g transform="translate(55 49) scale(0.5)"><polyline points="60,116 60,64 18,6" fill="none" stroke="#1F3A5F" stroke-width="18"/>'
            '<line x1="60" y1="64" x2="102" y2="6" stroke="#A3541A" stroke-width="18"/></g></svg>')

def page(code):
    c = CONTENT[code]
    t = fr_typo if code == "fr" else (lambda s: s)
    T = lambda s: e(t(s))
    depth = "" if c["dir"] == "" else "../"
    asset = depth + "assets/"
    ids = c["ids"]
    mailto = f"mailto:{EMAIL}?subject={quote(c['mail_subject'])}"
    # language links
    lang_links = []
    for l in ORDER:
        target = depth + CONTENT[l]["dir"] if CONTENT[l]["dir"] else (depth or "./")
        if l == code:
            lang_links.append(f'<strong aria-current="true" lang="{CONTENT[l]["lang"]}" title="{LANG_FULL[l]}">{LANG_NAMES[l]}</strong>')
        else:
            lang_links.append(f'<a href="{target}" lang="{CONTENT[l]["lang"]}" hreflang="{CONTENT[l]["lang"]}" title="{LANG_FULL[l]}">{LANG_NAMES[l]}</a>')
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{CONTENT[l]["lang"]}" href="{DOMAIN}{CONTENT[l]["dir"]}">' for l in ORDER
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{DOMAIN}">'
    nav = "".join(f'<a href="{h}">{e(n)}</a>' for h, n in c["nav"])
    domains = "".join(
        f'<article class="card"><p class="card__num">0{i+1}</p><h3>{T(title)}</h3><ul>' +
        "".join(f"<li>{T(x)}</li>" for x in items) + "</ul></article>"
        for i, (title, items) in enumerate(c["domains"])
    )
    tools = "".join(f"<li>{ICONS[i]}<span>{T(x)}</span></li>" for i, x in enumerate(c["tools"]))
    loop = "".join(f"<li><b>{T(a)}</b><span>{T(b)}</span></li>" for a, b in c["loop"])
    principles = "".join(f"<li><span>{T(p)}</span></li>" for p in c["principles"])
    metrics = "".join(f"<div><dt>{e(a)}</dt><dd>{T(b)}</dd></div>" for a, b in c["proof"])
    bio = "".join(f"<p>{T(p)}</p>" for p in c["bio"])
    manifesto = "".join(f"<li><div><h3>{T(a)}</h3><p>{T(b)}</p></div></li>" for a, b in c["manifesto"])
    m = c["motto"]
    motto_lines = [
        f'<p><b>{m[0][0]}</b>{e(m[0][1])}<b>{m[1][0]}</b>{e(m[1][1])}</p>',
        f'<p><b>{m[2][0]}</b>{e(m[2][1])}<b>{m[3][0]}</b>{e(m[3][1])}</p>',
        f'<p><b>{m[4][0]}</b>{e(m[4][1])}<b>{m[5][0]}</b>{e(m[5][1])}</p>',
        f'<p><b class="act">{m[6][0]}</b>{e(m[6][1])}</p>',
    ]
    motto_text = "".join(a + b for a, b in m)
    jsonld = {
        "@context": "https://schema.org", "@type": "Person",
        "name": "Alejandro Gaviria", "alternateName": "Alex Gaviria",
        "jobTitle": c["title"].split("— ")[-1], "url": DOMAIN + c["dir"],
        "email": EMAIL, "telephone": PHONE_TEL, "sameAs": [LINKEDIN],
        "knowsLanguage": ["fr", "en", "es"],
    }
    return f"""<!doctype html>
<html lang="{c['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(c['title'])}</title>
<meta name="description" content="{T(c['description'])}">
<link rel="canonical" href="{DOMAIN}{c['dir']}">
{alternates}
<meta property="og:type" content="website">
<meta property="og:title" content="{e(c['title'])}">
<meta property="og:description" content="{T(c['description'])}">
<meta property="og:url" content="{DOMAIN}{c['dir']}">
<meta property="og:image" content="{DOMAIN}assets/img/og.jpg">
<meta property="og:locale" content="{c['og_locale']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1F3A5F">
<link rel="icon" href="{depth}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{asset}img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<link rel="stylesheet" href="{asset}site.css">
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">{e(c['skip'])}</a>
<header class="header">
<nav class="wrap nav" aria-label="{e(c['nav_label'])}">
<a class="wordmark" href="./"><span class="mono" aria-hidden="true">AG</span><span class="wm">Alejandro <span>/Alex/</span> Gaviria</span></a>
<div class="nav__links">
<span class="nav__sections">{nav}</span>
<span class="langs" role="group" aria-label="{e(c['lang_label'])}">{''.join(lang_links)}</span>
<a class="btn btn--primary" href="#{ids['contact']}">{e(c['nav_cta'])}</a>
</div>
</nav>
</header>

<main id="main">
<section class="wrap hero" aria-labelledby="hero-title">
<div class="stack">
<p class="label">{T(c['hero_label'])}</p>
<h1 id="hero-title">{T(c['hero_title'])}</h1>
<p class="lede">{T(c['hero_lede'])}</p>
<div class="btns">
<a class="btn btn--decision" href="{mailto}">{T(c['hero_cta'])}</a>
<a class="btn btn--ghost" href="#{ids['offer']}">{T(c['hero_cta2'])}</a>
</div>
</div>
<img class="hero__photo" src="{asset}img/hero.jpg" width="1000" height="1250" alt="{e(c['hero_alt'])}" style="order:-1" fetchpriority="high">
</section>

<section class="section section--white" aria-labelledby="problem-title">
<div class="wrap split">
<div class="stack" style="gap:12px"><p class="label">{T(c['problem_label'])}</p><h2 class="h2" id="problem-title">{T(c['problem_title'])}</h2></div>
<p style="font-size:19px;line-height:30px">{T(c['problem_text'])}</p>
</div>
</section>

<section class="section" id="{ids['offer']}" aria-labelledby="offer-title">
<div class="wrap stack-lg">
<div class="stack narrow" style="gap:12px">
<p class="label">{T(c['offer_label'])}</p>
<h2 class="h2" id="offer-title">{T(c['offer_title'])}</h2>
<p class="lede">{T(c['offer_lede'])}</p>
</div>
<div class="cards">{domains}</div>
<div class="stack" style="gap:20px">
<p class="label">{T(c['tools_label'])}</p>
<ul class="tools">{tools}</ul>
</div>
<div class="band">
<div class="band__text"><span class="band__mark" aria-hidden="true"></span><p>{T(c['band_text'])}</p></div>
<a class="btn btn--primary" href="{mailto}">{T(c['band_cta'])}</a>
</div>
</div>
</section>

<section class="section section--brand" id="{ids['method']}" aria-labelledby="method-title">
<div class="wrap stack-lg">
<div class="method__head">
{badge(c['badge_alt'])}
<div class="stack">
<p class="label">{T(c['method_label'])}</p>
<h2 class="h2" id="method-title">{T(c['method_title'])}</h2>
<p class="lede">{T(c['method_text'])}</p>
</div>
</div>
<ol class="loop">{loop}</ol>
</div>
</section>

<section class="section" id="{ids['principles']}" aria-labelledby="principles-title">
<div class="wrap stack" style="gap:40px">
<div class="stack narrow" style="gap:12px"><p class="label">{T(c['principles_label'])}</p><h2 class="h2" id="principles-title">{T(c['principles_title'])}</h2></div>
<ol class="numbered">{principles}</ol>
</div>
</section>

<section class="section section--white" aria-labelledby="proof-title">
<div class="wrap stack" style="gap:32px">
<h2 class="label" id="proof-title" style="font-family:var(--font-sans)">{T(c['proof_label'])}</h2>
<dl class="metrics">{metrics}</dl>
<figure>
<img src="{asset}img/equipe.jpg" width="1400" height="933" alt="{e(c['team_alt'])}" loading="lazy">
<figcaption>{T(c['team_caption'])}</figcaption>
</figure>
</div>
</section>

<section class="section" id="{ids['about']}" aria-labelledby="about-title">
<div class="wrap about">
<img class="about__photo" src="{asset}img/portrait.jpg" width="800" height="800" alt="{e(c['about_alt'])}" loading="lazy">
<div class="stack">
<p class="label">{T(c['about_label'])}</p>
<h2 class="h2" id="about-title">Alejandro <span>/Alex/</span> Gaviria</h2>
{bio}
</div>
</div>
</section>

<section class="section section--white" id="{ids['manifesto']}" aria-labelledby="manifesto-title">
<div class="wrap stack">
<p class="label">{T(c['manifesto_label'])}</p>
<h2 class="h2" id="manifesto-title">{T(c['manifesto_title'])}</h2>
<p class="lede">{T(c['manifesto_intro'])}</p>
<ol class="numbered manifesto" style="margin-top:16px">{manifesto}</ol>
<p style="margin-top:16px;font-size:19px;line-height:30px">{T(c['manifesto_close'])}</p>
<div class="motto" aria-label="{e(motto_text)}">{''.join(motto_lines)}</div>
</div>
</section>

<section class="section" id="{ids['contact']}" aria-labelledby="contact-title">
<div class="wrap contact">
<div class="stack">
<p class="label">{T(c['contact_label'])}</p>
<h2 class="h2" id="contact-title">{T(c['contact_title'])}</h2>
<p class="muted">{T(c['contact_text'])}</p>
</div>
<div class="contact__links">
<a class="btn--decision" href="{mailto}"><span>{EMAIL}</span><span aria-hidden="true">→</span></a>
<a href="{LINKEDIN}" rel="me noopener"><span>LinkedIn</span><span aria-hidden="true">→</span></a>
<a class="quiet" href="tel:{PHONE_TEL}"><span>{PHONE}</span><span aria-hidden="true">→</span></a>
</div>
</div>
</section>
</main>

<footer class="footer">
<div class="wrap footer__row"><span class="mono mono--lg" aria-hidden="true">AG</span><span>© 2026 Alejandro /Alex/ Gaviria · gaviria.ca · {T(c['footer'])}</span></div>
</footer>
</body>
</html>
"""

def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets", "img"))
    shutil.copy(os.path.join(HERE, "site.css"), os.path.join(OUT, "assets", "site.css"))
    for f in os.listdir(os.path.join(HERE, "img")):
        shutil.copy(os.path.join(HERE, "img", f), os.path.join(OUT, "assets", "img", f))
    shutil.copy(os.path.join(HERE, "favicon.svg"), os.path.join(OUT, "favicon.svg"))
    for code in ORDER:
        d = os.path.join(OUT, CONTENT[code]["dir"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as fh:
            fh.write(page(code))
    with open(os.path.join(OUT, "CNAME"), "w") as fh:
        fh.write("gaviria.ca\n")
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    with open(os.path.join(OUT, "robots.txt"), "w") as fh:
        fh.write("User-agent: *\nAllow: /\nSitemap: https://gaviria.ca/sitemap.xml\n")
    urls = "".join(f"<url><loc>{DOMAIN}{CONTENT[l]['dir']}</loc></url>" for l in ORDER)
    with open(os.path.join(OUT, "sitemap.xml"), "w") as fh:
        fh.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    print("built", OUT)

if __name__ == "__main__":
    main()
