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
// Some service pages are linked at a public address that is not the folder they are generated in.
const serviceLinks = JSON.parse(fs.readFileSync(path.join('tools', 'v4-links.json'), 'utf8')).servicePages;
const serviceFiles = {
  'kitchen-remodeling': 'our-services/kitchen-remodeling/index.html',
  'bathroom-remodeling': 'our-services/bathroom-remodeling/index.html',
  'roofing': 'our-services/roofing/index.html',
  'deck-building': 'our-services/deck-building/index.html',
  'adu-garage-conversion': 'our-services/adu-garage-conversion/index.html',
  siding: 'our-services/siding/index.html',
  flooring: 'our-services/flooring/index.html',
  painting: 'our-services/painting/index.html',
};
for (const [key, file] of Object.entries(serviceFiles)) {
  const published = '/' + file.replace(/index\.html$/, '');
  const target = serviceLinks[key];
  if (!target || target === published) continue;
  const dest = path.join(stage, target.replace(/^\/|\/$/g, ''), 'index.html');
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.copyFileSync(path.join(stage, file), dest);
}
for (const [from, to] of [['css/site.min.css', 'css/site.min.css'], ['js/site.min.js', 'js/site.min.js'], ['vendor/gsap.min.js', 'vendor/gsap.min.js'], ['favicon.ico', 'favicon.ico'], ['apple-touch-icon.png', 'apple-touch-icon.png']]) {
  fs.mkdirSync(path.dirname(path.join(stage, to)), { recursive: true });
  fs.copyFileSync(path.join('site', from), path.join(stage, to));
}
console.log('staged in build/stage');
