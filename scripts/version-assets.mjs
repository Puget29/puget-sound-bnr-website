// Add a content hash (?v=xxxxxxxx) to every local CSS, JS, image, video and font reference in the published pages and in the bundled CSS,
// so the files can be cached for a year with "immutable" and still update the moment their content changes. Dev tool.
//   node scripts/version-assets.mjs
// Run after scripts/build-assets.mjs and after the root pages are generated (scripts/stage.mjs does all three). Safe to run twice.
// Large media (the hero videos) are also renamed by hand when they change (hero-m.mp4 to hero-m-2.mp4): immutable means a browser never asks again.
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';

const SITE = path.resolve('site');
const PAGES = ['v4/_root/index.html', 'v4/_root/about/index.html', 'v4/_root/contact/index.html', 'v4/_root/privacy/index.html', 'v4/_root/404.html'];
const EXT = /\.(css|js|webp|avif|jpe?g|png|svg|mp4|webm|woff2?|ico|bin|json)$/i;
const hash = f => crypto.createHash('sha1').update(fs.readFileSync(f)).digest('hex').slice(0, 8);

// where a reference lives on disk. The published layout is flat (css/, js/, assets/, vendor/ at the root), the source layout is site/.
function resolveFile(ref) {
  const clean = ref.replace(/^(\.\.\/)+/, '').replace(/^\.?\//, '');
  for (const c of [clean, clean.replace(/^v4\//, 'v4/'), 'v4/' + clean]) { const f = path.join(SITE, c); if (fs.existsSync(f) && fs.statSync(f).isFile()) return f; }
  return null;
}
const strip = u => u.replace(/\?v=[0-9a-f]{8}/, '');
function rewrite(text, isCss) {
  const re = isCss ? /url\((["']?)([^)"']+)\1\)/g : /(\b(?:src|href|poster|data-src-m|data-src-d|data-poster-d|data-hud|data-seq|data-seq-index|imagesrcset)=")([^"]+)(")/g;
  return text.replace(re, (all, a, ref, c) => {
    if (isCss) { c = a; a = 'url(' + a; }
    const clean = strip(ref);
    if (/^(https?:|\/\/|data:|mailto:|tel:|#)/.test(clean) || !EXT.test(clean.split('?')[0])) return all;
    const f = resolveFile(clean.split('?')[0]); if (!f) return all;
    const out = clean.split('?')[0] + '?v=' + hash(f) + (clean.includes('?') ? '&' + clean.split('?')[1] : '');
    return isCss ? `url(${c}${out}${c})` : a + out + c;
  });
}

// 1. the bundled CSS first (its font urls point at files, the CSS hash must be computed after they are rewritten)
const cssFile = path.join(SITE, 'css/site.min.css');
if (fs.existsSync(cssFile)) fs.writeFileSync(cssFile, rewrite(fs.readFileSync(cssFile, 'utf8'), true));
// 2. the pages
let n = 0;
for (const p of PAGES) {
  const f = path.join(SITE, p); if (!fs.existsSync(f)) continue;
  const before = fs.readFileSync(f, 'utf8'), after = rewrite(before, false);
  if (before !== after) { fs.writeFileSync(f, after); n++; }
}
console.log('versioned', n, 'pages');
