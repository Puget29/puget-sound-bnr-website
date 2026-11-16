#!/usr/bin/env python3
"""Live and preview build of every built main site page for the client's WordPress site (Cloudways, Apache).

    python tools/home-live.py            builds the site first (scripts/stage.mjs), then writes everything below
    python tools/home-live.py --no-stage reuse the current build/stage

Pages (see PAGES): home, about, contact, privacy, the services overview, eight service pages, the Blog index and every saved Blog post. Each built page is written twice into the plugin folder:
  pages/<slug>.preview.html  served at /home-new/ or its nested page route: noindex meta, links stay inside the preview, no tracking tags
  pages/<slug>.live.html     served at the real WordPress URL when the slug is named in BNR_LIVE_PAGES: real links, canonical, index, tracking
Links to pages that are not built yet always point to the real existing WordPress URL.

Output:
  dist-live-home/                               a web root tree, every zip extracts straight into it
    bnr-home-assets/                            css/, js/, vendor/, assets/ (only the files the pages use), favicon, touch icon
    wp-content/plugins/bnr-home-loader/         bnr-home-loader.php, readme.txt, pages/
  dist-live-home-zips/
    bnr-home-assets-video.zip                   the desktop hero video alone
    bnr-home-assets-N.zip                       everything else under bnr-home-assets/, 25 MB or less each
    bnr-home-loader.zip                         the plugin, for Plugins, Add New, Upload
    patch-<stamp>.zip                           ONLY the files that changed since the last build (web root paths), small
The previous build is remembered in build/home-live-manifest.json (file hashes).
Tracking (GTM and Ads) comes from data/tracking.json. Live pages only, previews carry no tags.
"""
import hashlib, json, re, shutil, subprocess, sys, zipfile, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tracking import tracking_blocks

ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / "build" / "stage"
SITE_ASSETS = ROOT / "site" / "assets"
PLUGIN_SRC = ROOT / "wp-plugin" / "bnr-home-loader"
OUT = ROOT / "dist-live-home"
ZIPS = ROOT / "dist-live-home-zips"
STATE = ROOT / "build" / "home-live-manifest.json"
LIVE = "https://www.pugetsoundbnr.com"
A = "/bnr-home-assets/"
MAX_ZIP = 25 * 1024 * 1024
BATCH = 20 * 1024 * 1024          # uncompressed batch size, so every zip stays far below 25 MB
VIDEO = "assets/hero-desktop-original.mp4"

# slug, source file in the stage, real WordPress path it replaces (None = preview only), preview path
# Source files starting with "@root/" are read from site/v4/_root.
SVC = json.loads((ROOT / "tools" / "v4-links.json").read_text(encoding="utf-8"))["servicePages"]
SVC_PAGES = [("services", "overview", "our-services/index.html"), ("kitchen", "kitchen-remodeling", "our-services/kitchen-remodeling/index.html"),
             ("bathroom", "bathroom-remodeling", "our-services/bathroom-remodeling/index.html"), ("roofing", "roofing", "our-services/roofing/index.html"),
             ("deck", "deck-building", "our-services/deck-building/index.html"), ("adu", "adu-garage-conversion", "our-services/adu-garage-conversion/index.html"),
             ("siding", "siding", "our-services/siding/index.html"), ("flooring", "flooring", "our-services/flooring/index.html"),
             ("painting", "painting", "our-services/painting/index.html")]
BLOG_POSTS = json.loads((ROOT / "data" / "blog" / "posts.json").read_text(encoding="utf-8")) if (ROOT / "data" / "blog" / "posts.json").exists() else []
PAGES = [
    ("home", "index.html", "/", "/home-new/"),
    ("about", "about/index.html", "/about/", "/home-new/about/"),
    ("contact", "contact/index.html", "/contact-us/", "/home-new/contact/"),
    ("privacy", "privacy/index.html", None, "/home-new/privacy/"),     # /ppc-assets/privacy/ is a real file served by Apache, so this page cannot take over that address
    ("projects", "@root/remodeling-projects/index.html", "/remodeling-projects/", "/home-new/remodeling-projects/"),
] + [(slug, "@root/" + f, SVC[key], "/home-new" + ("/our-services/" if key == "overview" else "/our-services/" + key + "/")) for slug, key, f in SVC_PAGES]
PAGES += [("blog", "@root/blog/index.html", "/blog/", "/home-new/blog/")]
# city pages: preview only (no real address), one per city that has an entry in data/city-facts.json
CITY_FACTS = json.loads((ROOT / "data" / "city-facts.json").read_text(encoding="utf-8")) if (ROOT / "data" / "city-facts.json").exists() else {}
PAGES += [("city-" + s, "@root/service-areas/" + s + "/index.html", None, "/home-new/service-areas/" + s + "/") for s in CITY_FACTS]
PAGES += [("service-areas", "@root/service-areas/index.html", None, "/home-new/service-areas/")]   # hub: preview only, not in BNR_LIVE_PAGES
PAGES += [("blog-" + p["slug"], "@root/blog/" + p["slug"] + "/index.html", p["path"], "/home-new/blog/" + p["slug"] + "/") for p in BLOG_POSTS]
# real WordPress paths of built pages (the targets links point to in live mode, and the ones rewritten to previews in preview mode)
REAL_OF = {"/remodeling-projects/": "projects", "/": "home", "/about/": "about", "/contact-us/": "contact", "/ppc-assets/privacy/": "privacy"}
REAL_OF.update({SVC[key]: slug for slug, key, _f in SVC_PAGES})
REAL_OF["/blog/"] = "blog"
REAL_OF["/service-areas/"] = "service-areas"
for _s in CITY_FACTS:
    REAL_OF["/service-areas/" + _s + "/"] = "city-" + _s
for p in BLOG_POSTS:
    REAL_OF.setdefault(p["path"], "blog-" + p["slug"])
PREVIEW_OF = {slug: prev for slug, _s, _l, prev in PAGES}
# relative links the generated inner pages still carry ("../../" from the service pages is folded into "../" first)
REL = {"../": "/", "../about/": "/about/", "../contact/": "/contact-us/", "../privacy/": "/ppc-assets/privacy/"}


def canon_link(u):
    """A link as written in the page -> its real WordPress form (relative '../' forms resolved)."""
    u = re.sub(r"^(?:\.\./)+", "../", u)
    for k in sorted(REL, key=len, reverse=True):
        if u == k or (u.startswith(k) and u[len(k):][:1] in ("?", "#") and k != "../"):
            return REL[k] + u[len(k):]
    return u


def map_link(u, preview):
    u = canon_link(u)
    if not u.startswith("/") or u.startswith("//"):
        return u
    path = re.split(r"[?#]", u, maxsplit=1)[0]
    rest = u[len(path):]
    if preview and path in REAL_OF:
        return PREVIEW_OF[REAL_OF[path]] + rest
    return u


def rewrite_html(t, preview):
    t = t.replace(LIVE + "/assets/og.jpg", LIVE + A + "assets/og.jpg")           # absolute og and twitter image
    t = re.sub(r'(?<![\w:/.-])(?:\.\./)*assets/', A + "assets/", t)
    jsname = "site.preview.min.js" if preview else "site.min.js"
    t = re.sub(r'(?<=["\'])(?:\.\./)*js/site\.min\.js', A + "js/" + jsname, t)
    t = re.sub(r'(?<=["\'])(?:\.\./)*(css|vendor)/(?=[\w.-]+\.(?:css|js)\b)', A + r"\1/", t)
    t = re.sub(r'(?<=["\'])(?:\.\./)*(favicon\.ico|apple-touch-icon\.png)', A + r"\1", t)
    t = re.sub(r'\sdata-hud="[^"]*"', "", t)                                     # dev overlay, not shipped
    t = re.sub(r'href="/[^"]*" data-blog-slug="([^"]+)"', lambda m: 'href="' + (PREVIEW_OF["blog-" + m.group(1)] if preview else "/" + m.group(1) + "/") + '"', t)
    t = re.sub(r'\sdata-blog-slug="[^"]+"', "", t)
    t = re.sub(r'href="([^"]*)"', lambda m: 'href="' + map_link(m.group(1), preview) + '"', t)
    return t


def rewrite_js(t, preview):
    t = re.sub(r'(?<![\w.-])/assets/', A + "assets/", t)
    if preview:   # the service cards build their links in script
        t = t.replace('"/contact-us/"', '"' + PREVIEW_OF["contact"] + '"')
        for real, slug in REAL_OF.items():     # the home service cards set their links in script
            if real not in ("/", "/about/", "/contact-us/", "/ppc-assets/privacy/"):
                t = t.replace('"' + real + '"', '"' + PREVIEW_OF[slug] + '"')
    return t


def finish_head(html, slug, live_path, preview):
    html = re.sub(r"<!-- DEMO: remove this noindex line[^>]*-->\s*", "", html)
    keep_original_blog_canonical = preview and (slug == "blog" or slug.startswith("blog-"))
    url = LIVE + (live_path if keep_original_blog_canonical or not preview else PREVIEW_OF[slug])
    html, n = re.subn(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', html, count=1)
    assert n == 1, f"{slug}: canonical"
    html, n = re.subn(r'(<meta property="og:url" content=")[^"]*(")', r"\g<1>" + url + r"\2", html, count=1)
    if n != 1:
        print(f"note: {slug} has no og:url tag")
    robots = "noindex, nofollow" if preview else "index, follow"
    html, n = re.subn(r'<meta name="robots" content="[^"]*">', f'<meta name="robots" content="{robots}">', html, count=1)
    assert n == 1, f"{slug}: robots"
    if not preview:
        head, noscript = tracking_blocks()
        if head:
            html, n = re.subn(r'(<meta name="viewport"[^>]*>)', lambda m: m.group(1) + "\n" + head, html, count=1)
            assert n == 1, "viewport"
        if noscript:
            html, n = re.subn(r"(<body[^>]*>)", lambda m: m.group(1) + "\n" + noscript, html, count=1)
            assert n == 1, "body"
    return html


def main():
    if "--no-stage" not in sys.argv:
        subprocess.run(["node", "scripts/stage.mjs"], cwd=ROOT, check=True)

    css = (STAGE / "css" / "site.min.css").read_text(encoding="utf-8")
    js_src = (STAGE / "js" / "site.min.js").read_text(encoding="utf-8")
    js_live, js_prev = rewrite_js(js_src, False), rewrite_js(js_src, True)

    built = {}      # (slug, kind) -> html
    for slug, src, live_path, prev_path in PAGES:
        raw = ((ROOT / "site" / "v4" / "_root" / src[6:]) if src.startswith("@root/") else (STAGE / src)).read_text(encoding="utf-8")
        built[(slug, "preview")] = finish_head(rewrite_html(raw, True), slug, live_path, True)
        if live_path:
            built[(slug, "live")] = finish_head(rewrite_html(raw, False), slug, live_path, False)

    old_offer = "Save Up to $700 on Home Remodeling"
    new_offer = "10% Off for New Clients"
    built = {key: html.replace(old_offer, new_offer) for key, html in built.items()}

    # fresh output (ignore errors from a folder a server still has open on Windows)
    if OUT.exists():
        shutil.rmtree(OUT, ignore_errors=True)
    base = OUT / "bnr-home-assets"
    (base / "css").mkdir(parents=True); (base / "js").mkdir(); (base / "vendor").mkdir()
    (base / "css" / "site.min.css").write_text(css, encoding="utf-8", newline="")
    (base / "js" / "site.min.js").write_text(js_live, encoding="utf-8", newline="")
    (base / "js" / "site.preview.min.js").write_text(js_prev, encoding="utf-8", newline="")
    shutil.copy(STAGE / "vendor" / "gsap.min.js", base / "vendor" / "gsap.min.js")
    for f in ("favicon.ico", "apple-touch-icon.png"):
        shutil.copy(STAGE / f, base / f)

    # only the asset files the pages use (html, js and css mention them; srcset siblings come along because they are named too)
    corpus = "".join(built.values()) + js_live + css
    names = set(re.findall(r"bnr-home-assets/assets/([\w./-]+?\.(?:webp|jpg|jpeg|png|svg|mp4|bin|json|woff2|txt|avif))", corpus))
    names |= {"fonts/OFL-Outfit.txt", "fonts/OFL-HankenGrotesk.txt"}
    missing = []
    for nme in sorted(names):
        src = next((b / nme for b in (STAGE / "assets", SITE_ASSETS) if (b / nme).is_file()), None)
        if src is None:
            missing.append(nme); continue
        dst = base / "assets" / nme
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, dst)
    if missing:
        sys.exit("MISSING ASSETS (referenced, not found): " + ", ".join(missing))

    # leftovers that would still point at the old layout
    for (slug, kind), h in built.items():
        bad = re.findall(r'(?<![\w.-])/assets/[\w./-]+|(?<=["\'])(?:\.\./)*(?:css|js|vendor)/[\w.-]+|href="\.\./[^"]*"|src="\.\./[^"]*"', h)
        if bad:
            sys.exit(f"{slug} {kind}: unrewritten paths: " + ", ".join(sorted(set(bad))[:8]))
        if kind == "live" and "noindex" in h:
            sys.exit(f"{slug} live page contains noindex")
        if kind == "preview" and ("noindex" not in h or "googletagmanager" in h):
            sys.exit(f"{slug} preview page must have noindex and no tracking")
        if re.search(r"whatsapp|wa\.me", h, re.I):
            sys.exit(f"{slug} {kind}: WhatsApp found")

    # plugin
    plug = OUT / "wp-content" / "plugins" / "bnr-home-loader"
    (plug / "pages").mkdir(parents=True)
    for f in PLUGIN_SRC.iterdir():
        if f.is_file():
            shutil.copy(f, plug / f.name)
    for (slug, kind), h in built.items():
        (plug / "pages" / f"{slug}.{kind}.html").write_text(h, encoding="utf-8", newline="")
    (plug / "pages" / "pages.json").write_text(json.dumps({s: {"preview": pv, "live": lv} for s, _x, lv, pv in PAGES}, indent=1))

    # zips
    ZIPS.mkdir(exist_ok=True)
    for old_zip in ZIPS.glob("*.zip"):          # full zips are rebuilt every time, earlier patch zips are kept
        if not old_zip.name.startswith("patch-"):
            old_zip.unlink()
    files = sorted(f for f in OUT.rglob("*") if f.is_file() and f.suffix != ".md")

    def make(name, items, prefix=None):
        p = ZIPS / name
        with zipfile.ZipFile(p, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
            for f in items:
                arc = f.relative_to(OUT).as_posix()
                if prefix:
                    arc = arc.replace("wp-content/plugins/", "", 1)
                zf.write(f, arc)
        return p

    video = base / VIDEO
    out_zips = [make("bnr-home-assets-video.zip", [video])]
    rest = [f for f in files if f.is_relative_to(base) and f != video]
    batches, cur, size = [], [], 0
    for f in rest:
        s = f.stat().st_size
        if cur and size + s > BATCH:
            batches.append(cur); cur, size = [], 0
        cur.append(f); size += s
    batches.append(cur)
    for i, b in enumerate(batches, 1):
        out_zips.append(make(f"bnr-home-assets-{i}.zip", b))
    out_zips.append(make("bnr-home-loader.zip", [f for f in files if f.is_relative_to(plug)], prefix=True))

    # lead handler plugin, zipped with the plugin folder at the top level (Plugins, Add New, Upload Plugin)
    lead_src = ROOT / "wp-plugin" / "bnr-lead-handler"
    lead_zip = ZIPS / "bnr-lead-handler.zip"
    with zipfile.ZipFile(lead_zip, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for f in sorted(lead_src.rglob("*")):
            if f.is_file():
                zf.write(f, "bnr-lead-handler/" + f.relative_to(lead_src).as_posix())
    out_zips.append(lead_zip)

    # patch zip: only files that changed since the last build
    rel = lambda f: f.relative_to(OUT).as_posix()
    manifest = {rel(f): hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
    old = json.loads(STATE.read_text()) if STATE.exists() else None
    if old is not None:
        changed = [f for f in files if old.get(rel(f)) != manifest[rel(f)]]
        gone = sorted(set(old) - set(manifest))
        stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
        if changed:
            pz = make(f"patch-{stamp}.zip", changed)
            out_zips.append(pz)
            print(f"patch zip: {pz.name} with {len(changed)} file(s)")
        else:
            print("patch zip: nothing changed since the last build")
        if gone:
            print("files no longer in the build (delete on the server if you want):", gone)
    else:
        print("first build: no patch zip (the full zips are the baseline)")
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(manifest, indent=0))

    print("pages:", ", ".join(f"{s}.{k} {len(h.encode()) // 1024}KB" for (s, k), h in built.items()), "| files", len(files))
    for z in out_zips:
        sz = z.stat().st_size
        print(f"  {z.name}: {sz / 1048576:.2f} MB", "OK" if sz <= MAX_ZIP else "TOO BIG")
        if sz > MAX_ZIP:
            sys.exit("zip over 25 MB")


if __name__ == "__main__":
    main()
