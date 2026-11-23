// Pre-render every page of the site as its own HTML file, so search engines index each lesson, card and deck at a
// real address (Zack, 2026-11-22: "remove the hashes so we get proper seo"). Runs at publish (build/publish.sh).
//
// It serves this folder (build/serve.mjs), opens the site once in headless Chrome (the copy Remotion already
// downloaded, or Google Chrome), and for every page key asks the app to render it, then writes index.html's shell with
// that page's title, description, canonical address and content filled in: lessons/<n>-<title>/index.html,
// cards/<name>/index.html, decks/..., opponents/..., rules/..., and one folder per section page. In the browser the app
// takes over as before. It also writes sitemap.xml and 404.html (the shell, which routes any other path and sends old
// #links to their new address). Folders it wrote last time are listed in build/prerendered.json and removed first,
// so a renamed lesson leaves no stale page behind.
import fs from 'fs'; import path from 'path'; import os from 'os'; import { spawn } from 'child_process'; import { fileURLToPath } from 'url';
import { serve } from './serve.mjs';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SITE = 'https://edison.learnretro.com';
const MANIFEST = path.join(ROOT, 'build/prerendered.json');
const SHELL = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
const KEEP = new Set(['build', 'data', 'design', 'hub', 'img', 'js', 'redirect', 'themes', 'video', '.git']);
const BINS = [path.join(ROOT, 'video/node_modules/.remotion/chrome-headless-shell/mac-arm64/chrome-headless-shell-mac-arm64/chrome-headless-shell'),
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'];
const BIN = BINS.find(b => fs.existsSync(b));
if (!BIN) { console.error('No headless Chrome found. Run npm install in video/, or install Google Chrome.'); process.exit(1); }

const attr = s => String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');
const text = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
function page(p) {
  return SHELL.replace(/<title>[^<]*<\/title>/, `<title>${text(p.t)}</title>`)
    .replace(/<meta name="description" content="[^"]*">/, `<meta name="description" content="${attr(p.d)}">`)
    .replace(/<link rel="canonical" href="[^"]*">/, `<link rel="canonical" href="${attr(p.c)}">`)
    .replace('<main id="app"></main>', () => `<main id="app">${p.h}</main>`);
}

// Chrome DevTools protocol over the WebSocket Node has built in.
async function browser() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'prerender-'));
  const proc = spawn(BIN, ['--headless', '--remote-debugging-port=0', '--no-first-run', '--no-default-browser-check', `--user-data-dir=${dir}`, 'about:blank'], { stdio: ['ignore', 'ignore', 'pipe'] });
  const wsUrl = await new Promise((res, rej) => { let buf = ''; proc.stderr.on('data', d => { buf += d; const m = buf.match(/DevTools listening on (ws:\/\/\S+)/); if (m) res(m[1]); }); proc.on('exit', c => rej(new Error('Chrome exited ' + c))); setTimeout(() => rej(new Error('Chrome did not start')), 20000); });
  const ws = new WebSocket(wsUrl); await new Promise(r => ws.addEventListener('open', r));
  let id = 0; const wait = new Map();
  ws.addEventListener('message', ev => { const m = JSON.parse(ev.data); if (m.id && wait.has(m.id)) { const [res, rej] = wait.get(m.id); wait.delete(m.id); m.error ? rej(new Error(JSON.stringify(m.error))) : res(m.result); } });
  const send = (method, params = {}, sessionId) => new Promise((res, rej) => { const i = ++id; wait.set(i, [res, rej]); ws.send(JSON.stringify({ id: i, method, params, sessionId })); });
  const close = async () => { try { ws.close(); } catch {} proc.kill(); await new Promise(r => proc.once('exit', r)); try { fs.rmSync(dir, { recursive: true, force: true }); } catch {} };
  return { send, close };
}

const srv = await serve(0); const port = srv.address().port;
const B = await browser();
try {
  const { targetId } = await B.send('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await B.send('Target.attachToTarget', { targetId, flatten: true });
  const ev = async expr => { const r = await B.send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }, sessionId); if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text); return r.result.value; };
  await B.send('Page.navigate', { url: `http://127.0.0.1:${port}/` }, sessionId);
  for (let i = 0; i < 100; i++) { await new Promise(r => setTimeout(r, 200)); try { if (await ev(`typeof go==='function'&&!!document.getElementById('app').innerHTML`)) break; } catch {} }
  const keys = await ev(`[...PAGEKEYS, ...ALL.map(l=>'lesson-'+l.n), ...DECKS.map(d=>'deck-'+encodeURIComponent(d.name)),
    ...(OPP.decks||[]).map(d=>'opponents-'+d.id), ...(window.EDISON_RULES?EDISON_RULES.sections.map(x=>'rules-'+x.id):[]),
    ...DB.filter(r=>r.k!=='token').map(r=>'card-'+r.id)]`);
  // Remove last run's pages, then write this run's.
  const old = fs.existsSync(MANIFEST) ? JSON.parse(fs.readFileSync(MANIFEST, 'utf8')) : [];
  for (const d of old) { const top = d.split('/')[0]; if (!top || KEEP.has(top)) continue; fs.rmSync(path.join(ROOT, d), { recursive: true, force: true }); }
  const written = new Set(), urls = [];
  let n = 0;
  for (const k of keys) {
    const p = JSON.parse(await ev(`(async()=>{window.__KEY=${JSON.stringify(k)};route();await new Promise(r=>setTimeout(r,0));
      return JSON.stringify({p:keyToPath(window.__KEY),t:document.title,d:document.querySelector('meta[name=description]').content,c:document.querySelector('link[rel=canonical]').href,h:document.getElementById('app').innerHTML})})()`));
    urls.push(SITE + p.p);
    if (p.p === '/') { n++; continue; } // the home page is index.html itself: left as is, the app renders it
    const rel = p.p.replace(/^\/|\/$/g, ''); const top = rel.split('/')[0];
    if (KEEP.has(top)) throw new Error(`Page ${p.p} would overwrite the ${top}/ folder`);
    fs.mkdirSync(path.join(ROOT, rel), { recursive: true });
    fs.writeFileSync(path.join(ROOT, rel, 'index.html'), page(p));
    written.add(top === rel ? rel : rel); n++;
    if (n % 500 === 0) console.log(`  ${n} of ${keys.length}`);
  }
  const tops = [...new Set([...written].map(r => r.split('/')[0]))].sort();
  fs.writeFileSync(MANIFEST, JSON.stringify(tops, null, 1) + '\n');
  const today = new Date().toISOString().slice(0, 10);
  fs.writeFileSync(path.join(ROOT, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${[...new Set(urls)].map(u => `<url><loc>${text(u)}</loc><lastmod>${today}</lastmod></url>`).join('\n')}\n</urlset>\n`);
  fs.writeFileSync(path.join(ROOT, '404.html'), SHELL.replace('<title>', '<meta name="robots" content="noindex">\n<title>'));
  console.log(`Pre-rendered ${n} pages (${tops.length} folders), sitemap.xml with ${new Set(urls).size} addresses, 404.html.`);
} finally { await B.close(); srv.close(); }
