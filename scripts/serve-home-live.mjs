// Local stand in for the WordPress plugin, for previewing dist-live-home/ at a root. Local use only.
//   node scripts/serve-home-live.mjs [port=8830] [livePages=home,about]
// Preview paths (/home-new/, /home-new/about/ ...) always serve pages/<slug>.preview.html with X-Robots-Tag noindex.
// Pages named in livePages also take over their real path and serve pages/<slug>.live.html (no noindex header). Everything else is static files from dist-live-home/.
import http from 'http';
import fs from 'fs';
import path from 'path';

const ROOT = path.resolve('dist-live-home');
const PORT = +(process.argv[2] || 8830);
const LIVE = (process.argv[3] || '').split(',').filter(Boolean);
const PD = path.join(ROOT, 'wp-content', 'plugins', 'bnr-home-loader', 'pages');
const PAGES = JSON.parse(fs.readFileSync(path.join(PD, 'pages.json'), 'utf8'));
const norm = p => p.toLowerCase().replace(/\/+$/, '') + '/';
const T = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.png': 'image/png', '.mp4': 'video/mp4', '.woff2': 'font/woff2', '.ico': 'image/x-icon', '.bin': 'application/octet-stream' };

// Local stand in for the lead handler (wp-plugin/bnr-lead-handler): same route, same checks and replies, nothing is sent anywhere. Accepted leads are appended to build/lead-log.jsonl.
const LEADLOG = path.resolve('build', 'lead-log.jsonl');
function lead(req, res) {
  let raw = '';
  req.on('data', c => { raw += c; if (raw.length > 20000) req.destroy(); });
  req.on('end', () => {
    const reply = (st, body) => { res.writeHead(st, { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' }); res.end(JSON.stringify(body)); };
    let d; try { d = JSON.parse(raw); } catch { return reply(400, { ok: false, error: 'bad_json' }); }
    if (d.website || (+d.elapsed || 0) < 3000) return reply(200, { ok: true });          // spam traps look successful, nothing is kept
    const digits = String(d.phone || '').replace(/\D+/g, '');
    const err = String(d.name || '').trim().length < 2 ? 'name' : (digits.length < 10 || digits.length > 15) ? 'phone' : !/^\d{5}$/.test(String(d.zip || '')) ? 'zip' : !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(d.email || '')) ? 'email' : '';
    if (err) return reply(400, { ok: false, error: 'invalid_' + err });
    fs.mkdirSync(path.dirname(LEADLOG), { recursive: true });
    fs.appendFileSync(LEADLOG, JSON.stringify({ at: new Date().toISOString(), name: d.name, service: d.service, origin_service: d.origin_service, page: d.origin_page, source: d.source, utm_source: d.utm_source || '' }) + '\n');
    reply(200, { ok: true });
  });
}

http.createServer((req, res) => {
  const u = new URL(req.url, 'http://x');
  if (req.method === 'POST' && u.pathname === '/wp-json/bnr/v1/lead') return lead(req, res);
  const p = decodeURIComponent(u.pathname), np = norm(p);
  for (const [slug, v] of Object.entries(PAGES)) {
    let kind = null;
    if (norm(v.preview) === np) kind = 'preview';
    else if (v.live && LIVE.includes(slug) && norm(v.live) === np) kind = 'live';
    if (!kind) continue;
    const f = path.join(PD, `${slug}.${kind}.html`);
    if (!fs.existsSync(f)) break;
    const h = { 'Content-Type': 'text/html; charset=UTF-8', 'Cache-Control': 'public, max-age=300' };
    if (kind === 'preview') h['X-Robots-Tag'] = 'noindex, nofollow';
    res.writeHead(200, h); return res.end(fs.readFileSync(f));
  }
  const f = path.join(ROOT, p);
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end('not found'); }
  const st = fs.statSync(f), h = { 'Content-Type': T[path.extname(f)] || 'application/octet-stream', 'Accept-Ranges': 'bytes' };
  const r = /bytes=(\d*)-(\d*)/.exec(req.headers.range || '');
  if (r) {
    const a = +r[1] || 0, b = r[2] ? Math.min(+r[2], st.size - 1) : st.size - 1;
    res.writeHead(206, { ...h, 'Content-Range': `bytes ${a}-${b}/${st.size}`, 'Content-Length': b - a + 1 });
    return fs.createReadStream(f, { start: a, end: b }).pipe(res);
  }
  res.writeHead(200, { ...h, 'Content-Length': st.size }); fs.createReadStream(f).pipe(res);
}).listen(PORT, '127.0.0.1', () => console.log(`serving ${ROOT} on ${PORT}, live pages: ${LIVE.join(',') || 'none'}`));
