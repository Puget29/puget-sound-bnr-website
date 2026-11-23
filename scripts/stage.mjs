// Build the site into build/stage: bundles the CSS and JS, generates the pages, adds content hashes to asset URLs and lays the files out as the site root.
//   node scripts/stage.mjs
// Run from the repository root. tools/home-live.py runs this first unless it is called with --no-stage.
import { spawnSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
process.chdir(root);
const PY = process.env.PYTHON || (process.platform === 'win32' ? 'python' : 'python3');

function run(cmd, args, env = {}) {
  const r = spawnSync(cmd, args, { stdio: ['ignore', 'ignore', 'inherit'], env: { ...process.env, ...env } });
  if (r.status !== 0) { console.error(`failed: ${cmd} ${args.join(' ')}`); process.exit(r.status || 1); }
}

run(process.execPath, ['scripts/build-assets.mjs']);
run(PY, ['tools/v4-gen.py'], { V4_ROOT: '1' });
run(process.execPath, ['scripts/version-assets.mjs']);

const stage = path.join('build', 'stage');
fs.rmSync(stage, { recursive: true, force: true });
fs.mkdirSync(stage, { recursive: true });
fs.cpSync(path.join('site', 'v4', '_root'), stage, { recursive: true });
fs.cpSync(path.join('site', 'assets'), path.join(stage, 'assets'), { recursive: true });
fs.mkdirSync(path.join(stage, 'contact-us'), { recursive: true });
fs.copyFileSync(path.join(stage, 'contact', 'index.html'), path.join(stage, 'contact-us', 'index.html'));
// Service pages are written directly to their public addresses by the generators (via tools/v4-links.json
// and _SPU in the service-page generators), so no folder-to-alias copy step is needed here.
for (const [from, to] of [['css/site.min.css', 'css/site.min.css'], ['js/site.min.js', 'js/site.min.js'], ['vendor/gsap.min.js', 'vendor/gsap.min.js'], ['favicon.ico', 'favicon.ico'], ['apple-touch-icon.png', 'apple-touch-icon.png']]) {
  fs.mkdirSync(path.dirname(path.join(stage, to)), { recursive: true });
  fs.copyFileSync(path.join('site', from), path.join(stage, to));
}

fs.cpSync(path.join('site', 'assets'), path.join(stage, 'assets'), { recursive: true });
// Service and all other pages are written directly to their public addresses by the generators
// (tools/v4-links.json + _SPU), so their internal links need no remapping. (The earlier WordPress-layout
// remap did not match this layout and rewrote correct /our-services/<svc>/ URLs to non-existent ones.)
// The one fix-up still needed: blog posts cross-link using a bare /<slug>/ - map those to /blog/<slug>/,
// but never a slug that is also a real staged page (e.g. /siding-replacement/ is the siding service page).
const blogSlugs = fs.existsSync('data/blog/posts.json') ? JSON.parse(fs.readFileSync('data/blog/posts.json', 'utf8')).map(p => p.slug) : [];
const routes = new Map();
for (const slug of blogSlugs)
  if (!fs.existsSync(path.join(stage, slug, 'index.html')) && fs.existsSync(path.join(stage, 'blog', slug, 'index.html')))
    routes.set(`/${slug}/`, `/blog/${slug}/`);
let remapped = 0;
(function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const f = path.join(dir, e.name);
    if (e.isDirectory()) { walk(f); continue; }
    if (!e.name.endsWith('.html')) continue;
    const html = fs.readFileSync(f, 'utf8');
    const out = html.replace(/(\shref=")(\/[^"#?]*)([^"]*")/g, (all, a, p, rest) => { const to = routes.get(p); if (!to) return all; remapped++; return a + to + rest; });
    if (out !== html) fs.writeFileSync(f, out);
  }
})(stage);

// Canonical and og:url of every staged page point at the page's own address on the production host (the blog posts still carried their old WordPress address).
const SITE = /^SITE = "([^"]+)"/m.exec(fs.readFileSync('tools/v4-gen.py', 'utf8'))[1];
const PREVIEW = process.env.PREVIEW === '1';

// ---- Adopt external-automation blog posts (public/blog/) into the staged site --------------------
// The blog automation tool pushes standalone pages to public/blog/<slug>/index.html plus a manifest
// public/blog/posts.json. The build does not otherwise read public/, so adopt any NEW post here, BEFORE
// the canonical/sitemap/tracking steps below, so those existing steps give each adopted page a non-www
// self-canonical, a sitemap entry and (production only) the GTM container. Generated posts are never
// touched: a slug already staged under build/stage/blog/ is skipped. Missing/malformed files fail safe.
let adopted = 0;
try {
  const autoDir = path.join('public', 'blog');
  const manifestFile = path.join(autoDir, 'posts.json');
  const blogDir = path.join(stage, 'blog');
  if (fs.existsSync(manifestFile) && fs.existsSync(blogDir)) {
    let posts = [];
    try {
      const parsed = JSON.parse(fs.readFileSync(manifestFile, 'utf8'));
      posts = Array.isArray(parsed) ? parsed : (parsed && Array.isArray(parsed.posts) ? parsed.posts : []);
    } catch (err) {
      console.error('stage: public/blog/posts.json is not valid JSON - automation blog adoption skipped');
    }
    const escHtml = (v) => String(v == null ? '' : v).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    // One robots directive, PREVIEW-aware: production = index,follow; preview = noindex (matches generated pages).
    const robotsTag = PREVIEW ? '<meta name="robots" content="noindex">' : '<meta name="robots" content="index, follow">';
    // Adopted pages style their article text with dark inline colours on a transparent container, which
    // assumes a light page. The site body is dark (--ink), so that body text would be invisible. Give the
    // article container a white "paper" panel so all of its text is readable (its inner blocks already set
    // their own light backgrounds). Scoped to .gs-blog-main, so the dark site header/footer are untouched.
    const themeFix = '<style id="gs-adopt-theme">.gs-blog-main{background:#fff;color:#374151;border-radius:14px;margin:28px auto;box-shadow:0 2px 10px rgba(0,0,0,.18)}</style>';
    // Automation card thumbnails live under /blog-images/uploads/...; copy them once if present.
    if (fs.existsSync(path.join('public', 'blog-images')) && !fs.existsSync(path.join(stage, 'blog-images')))
      fs.cpSync(path.join('public', 'blog-images'), path.join(stage, 'blog-images'), { recursive: true });
    let indexHtml = fs.existsSync(path.join(blogDir, 'index.html')) ? fs.readFileSync(path.join(blogDir, 'index.html'), 'utf8') : '';
    const seen = new Set();
    const newCards = [];
    for (const p of posts) {
      const slug = p && typeof p.slug === 'string' ? p.slug : '';
      // Validate/sanitize: lowercase slug, no separators or traversal, before using it in a filesystem path.
      if (!/^[a-z0-9][a-z0-9-]*$/.test(slug)) { if (slug) console.error(`stage: automation blog slug ${JSON.stringify(slug)} is unsafe - skipped`); continue; }
      if (seen.has(slug)) continue;                 // manifest listed the slug more than once
      seen.add(slug);
      const src = path.join(autoDir, slug, 'index.html');
      const dest = path.join(blogDir, slug);
      if (fs.existsSync(dest) || !fs.existsSync(src)) continue;   // never overwrite a generated post; need a source page
      let page = fs.readFileSync(src, 'utf8');
      // Exactly one robots directive: inject only when the page has none (the canonical walk below then
      // rewrites the page's single www canonical to the non-www self address - no second canonical added).
      if (!/<meta\s+name="robots"/i.test(page)) page = page.replace(/<\/head>/i, `  ${robotsTag}\n</head>`);
      if (!page.includes('id="gs-adopt-theme"')) page = page.replace(/<\/head>/i, `  ${themeFix}\n</head>`);
      fs.mkdirSync(dest, { recursive: true });
      fs.writeFileSync(path.join(dest, 'index.html'), page);
      adopted++;
      if (indexHtml && !indexHtml.includes(`data-blog-slug="${slug}"`))   // one card per slug, no duplicates
        newCards.push({ slug, title: escHtml(p.title), excerpt: escHtml(p.excerpt), image: typeof p.image === 'string' ? escHtml(p.image) : '', date: typeof p.publishedAt === 'string' ? p.publishedAt : '' });
    }
    if (newCards.length && /class="[^"]*blog-grid/.test(indexHtml)) {
      const cardsHtml = newCards.map((c) => {
        const img = c.image ? `  <a class="blog-card__image" href="/blog/${c.slug}/" data-blog-slug="${c.slug}" aria-label="Read ${c.title}"><img src="${c.image}" width="960" height="720" alt="${c.title}" loading="lazy" decoding="async"></a>\n` : '';
        const date = c.date ? `<p class="blog-card__date"><time datetime="${escHtml(c.date)}">${escHtml(c.date.slice(0, 10))}</time></p>\n    ` : '';
        return `<article class="blog-card">\n${img}  <div class="blog-card__copy">\n    ${date}<h2><a href="/blog/${c.slug}/" data-blog-slug="${c.slug}">${c.title}</a></h2><p>${c.excerpt}</p>\n    <a class="blog-card__more" href="/blog/${c.slug}/" data-blog-slug="${c.slug}">Read article<span aria-hidden="true"> ↗</span></a></div>\n</article>`;
      }).join('\n');
      indexHtml = indexHtml.replace(/(<[^>]*class="[^"]*blog-grid[^"]*"[^>]*>)/, `$1\n${cardsHtml}`);
      fs.writeFileSync(path.join(blogDir, 'index.html'), indexHtml);
    }
    if (adopted) console.log(`stage: adopted ${adopted} automation blog post(s) from public/blog/`);
  }
} catch (err) {
  console.error('stage: automation blog adoption skipped due to error:', err && err.message);
}

const urls = [];
(function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const f = path.join(dir, e.name);
    if (e.isDirectory()) { walk(f); continue; }
    if (e.name !== 'index.html') continue;
    const rel = path.relative(stage, dir).split(path.sep).join('/');
    const self = SITE + '/' + (rel ? rel + '/' : '');
    let html = fs.readFileSync(f, 'utf8');
    // Canonicalize every page to its own address (this fixes the blog posts, which carried their old
    // WordPress root path). /contact/ is the one deliberate exception: it consolidates to /contact-us/
    // (and is 301'd there by netlify.toml), so its canonical stays /contact-us/ and it is kept out of
    // the sitemap below.
    if (rel !== 'contact') {
      const out = html.replace(/(<link rel="canonical" href=")[^"]*(")/, `$1${self}$2`).replace(/(<meta property="og:url" content=")[^"]*(")/, `$1${self}$2`)
        .replace(/("mainEntityOfPage":\s*\{"@type":\s*"WebPage",\s*"@id":\s*")[^"]*(")/, `$1${self}$2`);
      if (out !== html) { html = out; fs.writeFileSync(f, out); }
    }
    // sitemap.xml: indexable, self-canonical pages only - no redirected/aliased URLs (e.g. /contact/),
    // no noindex pages, no duplicates. thank-you is always excluded.
    const robots = (html.match(/<meta name="robots" content="([^"]*)"/) || ['', ''])[1];
    const canon = (html.match(/<link rel="canonical" href="([^"]*)"/) || ['', ''])[1];
    if (rel !== 'thank-you' && /\bindex\b/.test(robots) && !/\bnoindex\b/.test(robots) && canon === self) urls.push(self);
  }
})(stage);
// robots.txt and sitemap.xml. PREVIEW=1 blocks crawlers, the default build allows everything.
urls.sort();
const nl = '\n';
fs.writeFileSync(path.join(stage, 'sitemap.xml'), '<?xml version="1.0" encoding="UTF-8"?>' + nl + '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + nl + urls.map(u => `  <url><loc>${u}</loc></url>`).join(nl) + nl + '</urlset>' + nl);
fs.writeFileSync(path.join(stage, 'robots.txt'), PREVIEW ? 'User-agent: *' + nl + 'Disallow: /' + nl : ['User-agent: *', 'Allow: /', '', `Sitemap: ${SITE}/sitemap.xml`, ''].join(nl));

// Production tracking (GTM + Google Ads) and the "Leave us a review" widget, injected into the staged
// main-site pages after they are generated/remapped/canonicalized but BEFORE the ads/ pages are copied
// in (those ship with their own tracking). Both injectors are idempotent. Tracking is skipped on a
// PREVIEW build so a preview never counts as live analytics/ad traffic; the review widget is content,
// not analytics, and already excludes the /service-areas/ location pages itself, so it always runs.
if (!PREVIEW) run(PY, ['tools/inject-tracking.py', stage]);
run(PY, ['tools/inject-review-widget.py', stage]);

// Google Ads landing pages. They are built once from the original PPC project and kept as static files in ads/ (81 city pages at /<City>-WA/, 5 service pages and ppc-assets/).
// They are noindex, stay out of the sitemap and post their form to Netlify Forms. PREVIEW=1 also removes the Google tags so a preview never counts as ad traffic.
let adsPages = 0;
if (fs.existsSync('ads')) {
  for (const e of fs.readdirSync('ads', { withFileTypes: true })) {
    if (!e.isDirectory()) continue;
    const to = path.join(stage, e.name);
    if (fs.existsSync(to)) { console.error(`ads/${e.name} clashes with a staged path`); process.exit(1); }
    fs.cpSync(path.join('ads', e.name), to, { recursive: true });
    if (e.name !== 'ppc-assets') adsPages += fs.existsSync(path.join(to, 'index.html')) ? 1 : 0;
    if (PREVIEW) (function walk(dir) {
      for (const f of fs.readdirSync(dir, { withFileTypes: true })) {
        const fp = path.join(dir, f.name);
        if (f.isDirectory()) { walk(fp); continue; }
        if (f.name !== 'index.html') continue;
        const h = fs.readFileSync(fp, 'utf8');
        const out = h.replace(/<!-- Google Tag Manager -->[\s\S]*?<!-- End Google Tag Manager -->\s*/, '')
          .replace(/<!-- Google Ads tag -->[\s\S]*?<\/script>\s*<script>[\s\S]*?<\/script>\s*/, '')
          .replace(/<!-- Google Tag Manager \(noscript\) -->[\s\S]*?<!-- End Google Tag Manager \(noscript\) -->\s*/, '');
        if (out !== h) fs.writeFileSync(fp, out);
      }
    })(to);
  }
}
console.log(`staged in build/stage (${adsPages} Google Ads pages, ${remapped} blog links mapped, ${urls.length} pages in sitemap${PREVIEW ? ', PREVIEW noindex' : ''})`);
