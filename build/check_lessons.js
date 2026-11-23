// Check a lesson file before it goes live: node build/check_lessons.js data/lessons-101.js [GOAT_LESSONS_101]
// Loads the real card data, runs the lesson file with stand-in helpers, and reports every problem:
// card names that don't exist in data/cards.js, missing fields, too few flashcards, em dashes and hype words.
const fs = require('fs'), path = require('path'), vm = require('vm');
const root = path.join(__dirname, '..');
const file = process.argv[2], key = process.argv[3] || (/step0/.test(file) ? 'GOAT_STEP0' : /101/.test(file) ? 'GOAT_LESSONS_101' : 'GOAT_LESSONS_201');
const ctx = { window: {}, console };
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(root, 'data/cards.js'), 'utf8'), ctx);
vm.runInContext(fs.readFileSync(path.join(root, file), 'utf8'), ctx);
const names = new Set(ctx.window.GOAT_CARDS.map(c => c.n));
['Sheep Token', 'Fluff Token', 'Emissary of Darkness Token'].forEach(n => names.add(n));
const problems = [];
const esc = s => String(s).replace(/[&<>"]/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[m]));
const cn = (n, label) => { if (!names.has(n)) problems.push(`cn(): unknown card "${n}"`); return `<b>${esc(label || n)}</b>`; };
const call = (type, tag, html) => { if (!['analogy', 'key', 'rule', 'mistake'].includes(type)) problems.push(`call(): unknown type "${type}"`); return `<div class="call ${type}"><b>${tag}</b>${html}</div>`; };
const fn = ctx.window[key];
if (typeof fn !== 'function') { console.log(`No function window.${key} in ${file}`); process.exit(1); }
const lessons = fn({ cn, call, esc });
for (const l of lessons) {
  const id = `Lesson ${l.n}`;
  for (const f of ['n', 'title', 'sub', 'min', 'cards', 'html', 'flash']) if (l[f] == null) problems.push(`${id}: missing ${f}`);
  (l.cards || []).forEach(n => { if (!names.has(n)) problems.push(`${id}: unknown card in cards list "${n}"`); });
  if ((l.flash || []).length < 4) problems.push(`${id}: only ${(l.flash || []).length} flashcards (need 4+)`);
  const text = (l.html || '') + JSON.stringify(l.flash || []) + l.title + l.sub;
  if (/—/.test(text)) problems.push(`${id}: contains an em dash`);
  const hype = text.match(/\b(insane|crazy|unreal|epic|broken|busted|game-changing|must-have)\b/gi);
  if (hype) problems.push(`${id}: hype words ${[...new Set(hype)].join(', ')}`);
  if (!/class="goals"/.test(l.html || '')) problems.push(`${id}: no "What you will learn" goals box`);
  if (!/class="recap"/.test(l.html || '')) problems.push(`${id}: no recap box`);
  const words = (l.html || '').replace(/<[^>]+>/g, ' ').split(/\s+/).filter(Boolean).length;
  console.log(`${id}: ${l.title} | ${words} words | ${(l.cards || []).length} cards | ${(l.flash || []).length} flashcards`);
}
console.log(problems.length ? `\n${problems.length} problem(s):\n- ` + problems.join('\n- ') : '\nNo problems found.');
process.exit(problems.length ? 1 : 0);
