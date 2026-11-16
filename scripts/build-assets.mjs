// Build the CSS and JS bundles. Build tool, nothing from here ships except the two output files.
//   node scripts/build-assets.mjs
// Needs esbuild (npm install in the repo root). Run by scripts/stage.mjs before the pages are generated.
//   css/site.min.css = css/site.css + css/hero-v3.css + v4/css/v4.css, minified, in that order (the order of the page's <link> tags)
//   js/site.min.js   = the site's own scripts in the exact order the pages load them, each wrapped so a failure in one cannot stop the next
// vendor/gsap.min.js stays a separate deferred file.
import fs from 'fs';
import path from 'path';
import * as esbuild from 'esbuild';

const SITE = path.resolve('site');

const CSS = ['css/site.css', 'css/hero-v3.css', 'v4/css/v4.css'];
// order as loaded by the home page (inner pages load a subset in the same relative order). hero-draft.js is the scroll cue's progress, it is still needed.
const JS = ['v4/js/forms.js', 'v4/js/motion.js', 'v4/js/v4.js', 'v4/js/hero-v4.js', 'js/hero-draft.js', 'js/dock.js', 'v4/js/who.js', 'v4/js/services.js', 'v4/js/trust.js', 'v4/js/wrf.js', 'v4/js/hero-v4-flip.js', 'v4/js/svc.js', 'v4/js/sx.js', 'v4/js/pj.js'];

const cssSrc = CSS.map(f => fs.readFileSync(path.join(SITE, f), 'utf8')).join('\n');
const cssOut = esbuild.transformSync(cssSrc, { loader: 'css', minify: true }).code;
fs.writeFileSync(path.join(SITE, 'css/site.min.css'), cssOut);

// each script is already an IIFE or strict-mode wrapper; wrap in try/catch blocks so one error does not stop the rest
const jsSrc = JS.map(f => `try{\n${fs.readFileSync(path.join(SITE, f), 'utf8')}\n}catch(e){console.error("[site] ${path.basename(f)}",e)}`).join('\n');
const jsOut = esbuild.transformSync(jsSrc, { loader: 'js', minify: true, target: 'es2018' }).code;
fs.writeFileSync(path.join(SITE, 'js/site.min.js'), jsOut);

const kb = f => (fs.statSync(path.join(SITE, f)).size / 1024).toFixed(1) + ' KB';
console.log('css/site.min.css', kb('css/site.min.css'), '| js/site.min.js', kb('js/site.min.js'));
