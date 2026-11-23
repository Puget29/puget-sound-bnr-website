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

// The generators write the live WordPress addresses (/contact-us/, /kitchen-remodel-seattle/, /cedar-decking/ ...). The staged site has its own layout,
// so every internal link is mapped to the page the build really creates. Built pages in site/v4/_root stay untouched (tools/home-live.py needs the live addresses).
fs.cpSync(path.join('site', 'assets'), path.join(stage, 'assets'), { recursive: true });
const links = JSON.parse(fs.readFileSync('tools/v4-links.json', 'utf8'));
const routes = new Map([[links.contact, '/contact/'], [links.privacy, '/privacy/']]);
for (const [key, live] of Object.entries(links.servicePages || {})) if (key !== 'overview') routes.set(live, `/our-services/${key}/`);
const blogSlugs = fs.existsSync('data/blog/posts.json') ? JSON.parse(fs.readFileSync('data/blog/posts.json', 'utf8')).map(p => p.slug) : [];
for (const slug of blogSlugs) if (!routes.has(`/${slug}/`)) routes.set(`/${slug}/`, `/blog/${slug}/`);   // a slug that is also a service address (siding-replacement) stays the service page
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
console.log(`staged in build/stage (${adsPages} Google Ads pages, ${remapped} links mapped to staged pages, ${urls.length} pages in sitemap${PREVIEW ? ', PREVIEW noindex' : ''})`);
