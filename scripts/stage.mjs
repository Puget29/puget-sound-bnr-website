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
// Regenerate the published page tree from scratch so renamed or removed pages leave no stale files.
fs.rmSync(path.join('site', 'v4', '_root'), { recursive: true, force: true });
run(PY, ['tools/v4-gen.py'], { V4_ROOT: '1' });
run(process.execPath, ['scripts/version-assets.mjs']);

const stage = path.join('build', 'stage');
fs.rmSync(stage, { recursive: true, force: true });
fs.mkdirSync(stage, { recursive: true });
fs.cpSync(path.join('site', 'v4', '_root'), stage, { recursive: true });
fs.cpSync(path.join('site', 'assets'), path.join(stage, 'assets'), { recursive: true });
fs.mkdirSync(path.join(stage, 'contact-us'), { recursive: true });
fs.copyFileSync(path.join(stage, 'contact', 'index.html'), path.join(stage, 'contact-us', 'index.html'));
// Service pages (general /our-services/ pages and the separate Seattle pages) are each written by the
// generator straight to their real public folder (tools/v4-gen-svcpages.py _rel_of), so no copying here.
for (const [from, to] of [['css/site.min.css', 'css/site.min.css'], ['js/site.min.js', 'js/site.min.js'], ['vendor/gsap.min.js', 'vendor/gsap.min.js'], ['favicon.ico', 'favicon.ico'], ['apple-touch-icon.png', 'apple-touch-icon.png']]) {
  fs.mkdirSync(path.dirname(path.join(stage, to)), { recursive: true });
  fs.copyFileSync(path.join('site', from), path.join(stage, to));
}

// Production tracking: inject GTM + Google Ads (from data/tracking.json, via tools/tracking.py)
// into every staged page. Skipped with --no-tracking so tools/home-live.py (the WordPress pipeline,
// which runs this script and then injects tracking itself) does not end up with two containers.
if (!process.argv.includes('--no-tracking')) {
  run(PY, ['tools/inject-tracking.py', stage]);
}

// robots.txt: allow crawling, point crawlers at the non-www sitemap.
const SITE = 'https://pugetsoundbnr.com';
fs.writeFileSync(path.join(stage, 'robots.txt'), `User-agent: *\nAllow: /\n\nSitemap: ${SITE}/sitemap.xml\n`);

// sitemap.xml: only pages that are indexable (robots = index) AND self-canonical. Individual
// city/location pages carry noindex and drop out; duplicate/aliased URLs (e.g. /contact/,
// /our-services/<svc>/ that canonical to a public alias) are not self-canonical and drop out;
// 404.html is not an index.html and is never scanned.
const locs = [];
const walk = dir => {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const fp = path.join(dir, e.name);
    if (e.isDirectory()) { walk(fp); continue; }
    if (e.name !== 'index.html') continue;
    const h = fs.readFileSync(fp, 'utf8');
    const robots = (h.match(/<meta name="robots" content="([^"]*)"/) || [])[1] || '';
    const canonical = (h.match(/<link rel="canonical" href="([^"]*)"/) || [])[1] || '';
    if (/\bnoindex\b/.test(robots) || !/\bindex\b/.test(robots)) continue;
    const relDir = path.relative(stage, dir).split(path.sep).join('/');
    const own = relDir ? `${SITE}/${relDir}/` : `${SITE}/`;
    if (canonical === own) locs.push(own);
  }
};
walk(stage);
locs.sort();
const sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
  + locs.map(u => `  <url><loc>${u}</loc></url>`).join('\n') + '\n</urlset>\n';
fs.writeFileSync(path.join(stage, 'sitemap.xml'), sitemap);

console.log(`staged in build/stage (sitemap: ${locs.length} url(s))`);
