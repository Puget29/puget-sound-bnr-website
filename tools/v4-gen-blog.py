# Local Blog index and post pages for the v4 site. Executed after the shared page helpers.
import json as _blog_json
import re as _blog_re
from html.parser import HTMLParser as _BlogParser
from urllib.parse import urlparse as _blog_urlparse, urljoin as _blog_urljoin
from pathlib import Path as _BlogPath

_BLOG_ROOT = _BlogPath(__file__).resolve().parents[1]
_BLOG_DATA = _BLOG_ROOT / "data" / "blog"
_BLOG_RAW = _blog_json.loads((_BLOG_DATA / "posts.raw.json").read_text(encoding="utf-8"))
_BLOG_SAVED = {post["slug"]: post for post in _blog_json.loads((_BLOG_DATA / "posts.json").read_text(encoding="utf-8"))}
_BLOG_CATS = {c["id"]: c["name"] for c in _blog_json.loads((_BLOG_DATA / "categories.raw.json").read_text(encoding="utf-8"))}
_BLOG_OVERRIDES = _blog_json.loads((_BLOG_DATA / "body-overrides.json").read_text(encoding="utf-8")) if (_BLOG_DATA / "body-overrides.json").exists() else {}
_BLOG_IMAGES = _blog_json.loads((_BLOG_DATA / "images.json").read_text(encoding="utf-8"))
_BLOG_IMAGE_MAP = {x["url"]: x for x in _BLOG_IMAGES}
_BLOG_SITE_HOSTS = {"pugetsoundbnr.com", "www.pugetsoundbnr.com"}
_BLOG_INTERNAL_PATHS = {v for v in URLS.values() if isinstance(v, str)} | set(URLS.get("servicePages", {}).values()) | {"/", "/blog/"} | {"/service-areas/" + c + "/" for c in ("renton", "kirkland", "bellevue")}
# Old WordPress pages that no longer exist, pointed at the closest page that does (live addresses, the staged build maps them again).
_BLOG_OLD_PAGES = {
    "/deck-repair-seattle/": "/our-services/deck-building/",
    "/seattle-home-addition/": "/our-services/adu-garage-conversion/",
    "/seattle-basement-remodel/": "/our-services/",
    "/vinyl-siding-seattle/": URLS["siding"],
    "/seattle-prodigy-siding/": URLS["siding"],
    "/testimonials/": URLS["projects"],
    "/jacuzzi-bath-remodel/": URLS["servicePages"]["bathroom-remodeling"],
    "/bathroom-remodel-seattle/walk-in-bathtub-with-shower/": URLS["servicePages"]["bathroom-remodeling"],
    "/bathroom-remodel-seattle/soaking-tub-with-shower/": URLS["servicePages"]["bathroom-remodeling"],
    "/general-contractor-in-renton/": "/service-areas/renton/",
    "/general-contractor-in-kirkland/": "/service-areas/kirkland/",
    "/general-contractor-in-bellevue/": "/service-areas/bellevue/",
}
_BLOG_INTERNAL_PATHS.update(_blog_urlparse(p.get("link", "")).path for p in _BLOG_RAW if _blog_urlparse(p.get("link", "")).path)

def _blog_img_key(url):
    u = _blog_urlparse(url)
    return u._replace(query="", fragment="").geturl()

def _blog_content(post):
    content = post.get("content", {}).get("rendered", "")
    return _BLOG_SAVED.get(post["slug"], {}).get("bodyHtml", _BLOG_OVERRIDES.get(post["slug"], content))

class _BlogClean(_BlogParser):
    allowed = {"h2", "h3", "h4", "h5", "h6", "p", "ul", "ol", "li", "a", "img", "figure", "figcaption", "blockquote", "table", "thead", "tbody", "tfoot", "tr", "th", "td", "strong", "b", "em", "i", "br", "hr"}
    void = {"img", "br", "hr"}
    drop = {"script", "style", "noscript", "svg", "form", "button"}
    def __init__(self, depth, base_path):
        super().__init__(convert_charrefs=True)
        self.depth = depth
        self.base_path = base_path
        self.out = []
        self.stack = []
        self.drop_depth = 0
    def _local(self, src):
        entry = _BLOG_IMAGE_MAP.get(_blog_img_key(src))
        if not entry: return src
        return "../" * self.depth + entry["local"]
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if d.get("id") == "nextsection":
            self.out.append('<span id="nextsection"></span>')
        if tag == "iframe":
            if d.get("src"):
                self.out.append('<p><a href="' + esc(d["src"]) + '">Open embedded media</a></p>')
            return
        if tag in self.drop:
            self.drop_depth += 1
            return
        if self.drop_depth: return
        if tag not in self.allowed: return
        keep = ""
        if tag == "a" and d.get("href"):
            href = d["href"]
            u = _blog_urlparse(_blog_urljoin(SITE + self.base_path, href))
            if u.netloc.lower() in _BLOG_SITE_HOSTS:
                suffix = ("?" + u.query if u.query else "") + ("#" + u.fragment if u.fragment else "")
                _path_in = u.path or "/"
                _path_in = _BLOG_OLD_PAGES.get(_path_in, _path_in)
                href = _path_in + suffix if _path_in in _BLOG_INTERNAL_PATHS else SITE + _path_in + suffix
            keep += ' href="' + esc(href) + '"'
            if d.get("target") == "_blank": keep += ' target="_blank" rel="noopener noreferrer"'
        elif tag == "img":
            src = d.get("data-src") or d.get("data-lazy-src") or d.get("src") or ""
            ent = _BLOG_IMAGE_MAP.get(_blog_img_key(src))
            if not ent: return
            local = self._local(src) if src else ""
            keep += ' src="' + esc(local) + '"'
            keep += ' alt="' + esc(d.get("alt", "")) + '"'
            if ent:
                keep += ' width="' + str(ent.get("width", "")) + '" height="' + str(ent.get("height", "")) + '"'
            keep += ' loading="lazy" decoding="async"'
        self.out.append("<" + tag + keep + ">")
        if tag not in self.void: self.stack.append(tag)
    def handle_endtag(self, tag):
        if tag in self.drop and self.drop_depth:
            self.drop_depth -= 1
            return
        if self.drop_depth or tag not in self.allowed or tag in self.void: return
        if tag in self.stack:
            while self.stack:
                open_tag = self.stack.pop()
                self.out.append("</" + open_tag + ">")
                if open_tag == tag: break
    def handle_data(self, data):
        if not self.drop_depth: self.out.append(esc(data))
    def close(self):
        super().close()
        while self.stack: self.out.append("</" + self.stack.pop() + ">")

def _blog_clean(source, depth, base_path):
    parser = _BlogClean(depth, base_path)
    parser.feed(source)
    parser.close()
    return "".join(parser.out)

def _blog_text(source):
    p = _BlogParser(convert_charrefs=True)
    p.parts = []
    p.handle_data = lambda data: p.parts.append(data)
    p.feed(source)
    return " ".join("".join(p.parts).split())

def _blog_date(value):
    from datetime import datetime as _dt
    d = _dt.fromisoformat(value.replace("Z", "+00:00"))
    return d.strftime("%B %d, %Y").replace(" 0", " ")

def _blog_image(url, depth, eager=False):
    entry = _BLOG_IMAGE_MAP[_blog_img_key(url)]
    src = "../" * depth + entry["local"]
    base = entry.get("srcBase")
    srcset = ", ".join("../" * depth + (f"{base}-{w}.webp" if base else entry["local"]) + " " + str(w) + "w" for w in entry.get("widths", []))
    sizes = ' sizes="(min-width: 900px) 860px, 100vw"' if (srcset and depth == 2) else (' sizes="(min-width: 1100px) 380px, (min-width: 700px) 50vw, 100vw"' if srcset else "")
    loading = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    return f'<img src="{esc(src)}"{f" srcset=\"{esc(srcset)}\"" if srcset else ""}{sizes} width="{entry["width"]}" height="{entry["height"]}" alt="{esc(entry.get("alt", ""))}" {loading}>'

_BLOG_POSTS = []
for _item in _BLOG_RAW:
    _yoast = _item.get("yoast_head_json") or {}
    _url = _item.get("link", "")
    _path = _blog_urlparse(_url).path
    if not _path.endswith("/"): _path += "/"
    _image_source = ((_yoast.get("og_image") or [{}])[0].get("url") or "")
    _image = _image_source
    _saved_image = _BLOG_SAVED.get(_item["slug"], {}).get("featuredImage")
    if _saved_image: _image = _saved_image   # a real project photo chosen in data/blog/posts.json
    _excerpt = _BLOG_SAVED.get(_item["slug"], {}).get("excerpt")
    if not _excerpt: raise SystemExit("Blog post is missing its saved excerpt: " + _item["slug"])
    _body = _blog_content(_item).replace("in the region.Consider", "in the region. Consider")
    if _image and _blog_img_key(_image) not in _BLOG_IMAGE_MAP:
        for _img_match in _blog_re.finditer(r'<img\b[^>]*\b(?:data-src|data-lazy-src|src)=["\']([^"\']+)', _body, _blog_re.I):
            _candidate = _img_match.group(1).replace("&amp;", "&")
            if _blog_img_key(_candidate) in _BLOG_IMAGE_MAP:
                _image = _candidate
                break
        else:
            _image = ""
    _post = {
        "title": _BLOG_SAVED.get(_item["slug"], {}).get("title") or html.unescape(_item["title"]["rendered"]), "slug": _item["slug"], "path": _path,
        "date": _item["date"], "modified": _item["modified"],
        "author": "Puget Sound BNR", "category": ", ".join(_BLOG_CATS.get(c, "") for c in _item.get("categories", [])),
        "excerpt": _excerpt, "bodyHtml": _body, "featuredImage": _image, "featuredImageSource": _image_source,
        "midImage": _BLOG_SAVED[_item["slug"]].get("midImage", ""),
        "seoTitle": _BLOG_SAVED[_item["slug"]]["seoTitle"],
        "metaDescription": _BLOG_SAVED[_item["slug"]].get("metaDescription"), "canonical": _yoast.get("canonical") or _url,
    }
    _BLOG_POSTS.append(_post)
_BLOG_POSTS.sort(key=lambda q: q["date"], reverse=True)
_BLOG_UP = "../"
_BLOG_CARDS = []
for _p in _BLOG_POSTS:
    _img_url = _p["featuredImage"]
    _card_img = _blog_image(_img_url, 1) if _img_url else ""
    _card_image = f'<a class="blog-card__image" href="/blog/{esc(_p["slug"])}/" data-blog-slug="{esc(_p["slug"])}" aria-label="Read {esc(_p["title"])}">{_card_img}</a>' if _card_img else ""
    _BLOG_CARDS.append(f'''<article class="blog-card">
  {_card_image}
  <div class="blog-card__copy"><p class="blog-card__date"><time datetime="{esc(_p['date'])}">{esc(_blog_date(_p['date']))}</time></p>
    <h2><a href="/blog/{esc(_p['slug'])}/" data-blog-slug="{esc(_p['slug'])}">{esc(_p['title'])}</a></h2><p>{esc(_p['excerpt'])}</p>
    <a class="blog-card__more" href="/blog/{esc(_p['slug'])}/" data-blog-slug="{esc(_p['slug'])}">Read article<span aria-hidden="true"> ↗</span></a></div>
</article>''')

_BLOG_INDEX_PATH = "/blog/"
_BLOG_INDEX = (head("Blog | Puget Sound BNR", "Home remodeling articles from Puget Sound BNR on kitchens, bathrooms, decks, siding, insulation and choosing a general contractor.", _BLOG_INDEX_PATH, _BLOG_UP)
    + "<body>\n" + '<a class="skip" href="#main">Skip to content</a>\n' + banner() + header(_BLOG_UP, "blog", False)
    + f'''<main id="main"><section class="sec sec--dark blog-index" aria-labelledby="blog-title"><div class="wrap">
  <div class="blog-intro"><p class="eyebrow">From the blog</p><h1 class="h1" id="blog-title">Blog</h1></div>
  <div class="blog-grid">{"".join(_BLOG_CARDS)}</div>
</div></section></main>\n'''
    + footer(_BLOG_UP) + mbar(_BLOG_UP) + scripts(_BLOG_UP, False) + "</body>\n</html>\n")
w("blog/index.html", _BLOG_INDEX)

_BLOG_FORM = _form({"chip": "", "formHeading": "Free consultation", "formService": "Blog"}, "blog")
for _p in _BLOG_POSTS:
    _up = "../../"
    _ld = {"@context": "https://schema.org", "@type": "Article", "headline": _p["title"], "datePublished": _p["date"],
           "dateModified": _p["modified"], "author": {"@type": "Person", "name": _p["author"]},
           "articleSection": _p["category"], "image": [SITE + _p["featuredImage"]] if _p["featuredImage"].startswith("/") else ([_p["featuredImage"]] if _p["featuredImage"] else []),
           "mainEntityOfPage": {"@type": "WebPage", "@id": _p["canonical"]}, "publisher": {"@type": "Organization", "name": "Puget Sound Builders & Renovation"}}
    _desc = _p["metaDescription"] or ""
    _seo_head = f'<meta name="author" content="{esc(_p["author"])}">\n' if _p["author"] else ""
    _hero = _blog_image(_p["featuredImage"], 2, True) if _p["featuredImage"] else ""
    _body_html = _blog_clean(_p["bodyHtml"], 2, _p["path"])
    if _p["midImage"]:
        _ends = [m.end() for m in _blog_re.finditer(r"</p>", _body_html)]
        _at = _ends[len(_ends) // 3] if _ends else 0
        _body_html = _body_html[:_at] + "<figure>" + _blog_image(_p["midImage"], 2) + "</figure>" + _body_html[_at:]
    _post_html = (head(_p["seoTitle"], _desc, _p["path"], _up, extra_head=_seo_head, jsonld=[_ld])
        + "<body>\n" + '<a class="skip" href="#main">Skip to content</a>\n' + banner() + header(_up, "blog", False)
        + f'''<main id="main" class="blog-post"><article class="sec sec--dark" aria-labelledby="post-title"><div class="wrap blog-reading">
  <nav class="crumbs blog-crumbs" aria-label="Breadcrumb"><a href="/blog/">Blog</a><span aria-hidden="true">/</span><span aria-current="page">{esc(_p['title'])}</span></nav>
  <header class="blog-post__head"><p class="blog-post__meta"><time datetime="{esc(_p['date'])}">{esc(_blog_date(_p['date']))}</time><span aria-hidden="true"> · </span><span>{esc(_p['author'])}</span></p><h1 class="h1" id="post-title">{esc(_p['title'])}</h1>{_hero}</header>
  <div class="blog-article__body">{_body_html}</div><p class="blog-back"><a href="/blog/">← Back to Blog</a></p>
</div></article></main>\n'''
        + lead_block("blog-contact", "blog-contact-title", "Let's talk about your project.", "Send a few details and we will take it from there. We reply within one business day.", _BLOG_FORM, htag="p")
        + footer(_up) + mbar(_up) + scripts(_up, False) + "</body>\n</html>\n")
    if not _desc:
        _post_html = _post_html.replace('<meta name="description" content="">\n', "")
    w("blog/" + _p["slug"] + "/index.html", _post_html)

print("generated blog index and", len(_BLOG_POSTS), "posts")
