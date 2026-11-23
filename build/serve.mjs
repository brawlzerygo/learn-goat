// A small static server for this folder that behaves like GitHub Pages: a path that is a folder serves its
// index.html, and a path with no file serves 404.html (else index.html), which the app then routes. Used by
// build/prerender.mjs and for local previews: node build/serve.mjs [port]
import http from 'http'; import fs from 'fs'; import path from 'path'; import { fileURLToPath } from 'url';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.json': 'application/json', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.xml': 'application/xml', '.txt': 'text/plain' };
// The site's folder on learnretro.com, read from <base href> in index.html ('/edison' for <base href="/edison/">). The
// server serves the folder at that path, like the live site, and sends / there.
export function mountOf(root = ROOT) {
  const m = fs.readFileSync(path.join(root, 'index.html'), 'utf8').match(/<base href="([^"]*)">/);
  return m ? m[1].replace(/\/$/, '') : '';
}
export function serve(port = 0, root = ROOT) {
  const MOUNT = mountOf(root);
  const srv = http.createServer((req, res) => {
    let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
    if (MOUNT) {
      if (p === '/' || p === MOUNT) { res.writeHead(302, { Location: MOUNT + '/' }); return res.end(); }
      if (!p.startsWith(MOUNT + '/')) { res.writeHead(404, { 'Content-Type': 'text/plain' }); return res.end('Not part of this site'); }
      p = p.slice(MOUNT.length);
    }
    let f = path.join(root, p);
    if (!f.startsWith(root)) { res.writeHead(403); return res.end(); }
    if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
    let code = 200;
    if (!fs.existsSync(f)) { code = 404; f = fs.existsSync(path.join(root, '404.html')) ? path.join(root, '404.html') : path.join(root, 'index.html'); }
    res.writeHead(code, { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream', 'Cache-Control': 'no-store' });
    fs.createReadStream(f).pipe(res);
  });
  return new Promise(r => srv.listen(port, '127.0.0.1', () => r(srv)));
}
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const port = +(process.argv[2] || process.env.PORT || 8782);
  const root = process.argv[3] ? path.resolve(process.argv[3]) : ROOT;
  serve(port, root).then(() => console.log(`Serving ${root} on http://127.0.0.1:${port}${mountOf(root)}/`));
}
