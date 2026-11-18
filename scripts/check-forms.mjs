// Check the staged site for Netlify Forms. Run after npm run stage:   node scripts/check-forms.mjs
// Every <form> must be the static form "lead" with data-netlify, the honeypot, the hidden form-name and a unique id, and nothing may call wp-json.
import fs from 'fs';
import path from 'path';

const root = process.argv[2] || 'build/stage';
const problems = [];
let forms = 0, pages = 0;
const fieldSets = new Map();

(function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const f = path.join(dir, e.name);
    if (e.isDirectory()) { walk(f); continue; }
    if (/\.(html|js|css|xml|txt)$/.test(e.name) && fs.readFileSync(f, 'utf8').includes('wp-json')) problems.push(`${f}: mentions wp-json`);
    if (!e.name.endsWith('.html')) continue;
    pages++;
    const html = fs.readFileSync(f, 'utf8');
    const ids = new Set();
    for (const m of html.matchAll(/<form\b([^>]*)>([\s\S]*?)<\/form>/g)) {
      forms++;
      const [, attrs, inner] = m;
      const where = f.replace(/\\/g, '/');
      const need = [['data-netlify="true"', /data-netlify="true"/], ['name="lead"', /\sname="lead"/], ['data-netlify-honeypot="bot-field"', /data-netlify-honeypot="bot-field"/], ['method="post"', /method="post"/], ['action="/thank-you/"', /action="\/thank-you\/"/]];
      for (const [label, re] of need) if (!re.test(attrs)) problems.push(`${where}: form missing ${label}`);
      const id = /\sid="([^"]+)"/.exec(attrs);
      if (!id) problems.push(`${where}: form has no id`);
      else if (ids.has(id[1])) problems.push(`${where}: duplicate form id ${id[1]}`);
      else ids.add(id[1]);
      if (!/<input type="hidden" name="form-name" value="lead">/.test(inner)) problems.push(`${where}: hidden form-name missing`);
      if (!/<input[^>]*name="bot-field"/.test(inner)) problems.push(`${where}: honeypot field missing`);
      for (const n of ['name', 'phone', 'email', 'zip', 'service']) if (!new RegExp(`name="${n}"`).test(inner)) problems.push(`${where}: field ${n} missing`);
      const names = [...new Set([...inner.matchAll(/<(?:input|select|textarea)\b[^>]*\sname="([^"]+)"/g)].map(x => x[1]))].sort().join(',');
      fieldSets.set(names, (fieldSets.get(names) || 0) + 1);
    }
  }
})(root);

console.log(`pages ${pages}, forms ${forms}, field sets ${fieldSets.size}`);
for (const [k, v] of fieldSets) console.log(`  ${v} forms: ${k}`);
if (problems.length) { console.log(`PROBLEMS ${problems.length}`); problems.slice(0, 30).forEach(p => console.log('  ' + p)); process.exit(1); }
console.log('OK: every form is a Netlify form named "lead", no wp-json anywhere');
