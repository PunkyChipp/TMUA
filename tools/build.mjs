// Build: bundles content + app into a single self-contained HTML file.
//   dist/index.html     full document (GitHub Pages / open from disk, works offline)
//   dist/artifact.html  same app as a page fragment (for hosts that add their own <head>)
import { build } from 'esbuild';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const r = (...p) => path.join(root, ...p);
const watch = process.argv.includes('--watch');

function writeContent() {
  const qdir = r('content/questions');
  const ndir = r('content/notes');
  const questions = [];
  for (const f of fs.readdirSync(qdir).filter(f => f.endsWith('.json')).sort()) {
    const arr = JSON.parse(fs.readFileSync(path.join(qdir, f), 'utf8'));
    for (const q of arr) questions.push(q);
  }
  const notes = {};
  for (const f of fs.readdirSync(ndir).filter(f => f.endsWith('.md')).sort()) {
    notes[f.replace(/\.md$/, '')] = fs.readFileSync(path.join(ndir, f), 'utf8');
  }
  fs.mkdirSync(r('src/generated'), { recursive: true });
  fs.writeFileSync(r('src/generated/content.js'),
    `export const QUESTIONS = ${JSON.stringify(questions)};\nexport const NOTES = ${JSON.stringify(notes)};\n`);
  return { q: questions.length, n: Object.keys(notes).length };
}

function katexCss() {
  const dir = r('node_modules/katex/dist');
  let css = fs.readFileSync(path.join(dir, 'katex.min.css'), 'utf8');
  // Inline woff2 only; drop woff/ttf fallbacks to keep the file small.
  css = css.replace(/src:([^;}]*)/g, (m, srcs) => {
    const w = srcs.match(/url\((fonts\/[^)]+\.woff2)\)/);
    if (!w) return m;
    const b64 = fs.readFileSync(path.join(dir, w[1])).toString('base64');
    return `src:url(data:font/woff2;base64,${b64}) format("woff2")`;
  });
  return css;
}

async function bundle() {
  const stats = writeContent();
  const res = await build({
    entryPoints: [r('src/main.js')], bundle: true, minify: true, format: 'iife',
    target: ['es2020'], write: false, legalComments: 'none',
  });
  const js = res.outputFiles[0].text.replace(/<\/script/gi, '<\\/script');
  const css = fs.readFileSync(r('src/styles.css'), 'utf8') + '\n' + katexCss();
  const tpl = fs.readFileSync(r('src/index.html'), 'utf8');
  const body = tpl.split('<!--BODY-->')[1].split('<!--/BODY-->')[0];
  const head = tpl.split('<!--HEAD-->')[1].split('<!--/HEAD-->')[0];
  const full = `<!doctype html>\n<html lang="en-GB">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n${head}\n<style>${css}</style>\n</head>\n<body>\n${body}\n<script>${js}</script>\n</body>\n</html>\n`;
  const frag = `${head}\n<style>${css}</style>\n${body}\n<script>${js}</script>\n`;
  fs.mkdirSync(r('dist'), { recursive: true });
  fs.writeFileSync(r('dist/index.html'), full);
  fs.writeFileSync(r('dist/artifact.html'), frag);
  const kb = (Buffer.byteLength(full) / 1024).toFixed(0);
  console.log(`built dist/index.html (${kb} KB) — ${stats.q} questions, ${stats.n} notes`);
}

await bundle();
if (watch) {
  console.log('watching src/ and content/ …');
  let t;
  for (const d of ['src', 'content']) {
    fs.watch(r(d), { recursive: true }, (e, f) => {
      if (f && f.startsWith('generated')) return;
      clearTimeout(t); t = setTimeout(() => bundle().catch(e => console.error(e.message)), 150);
    });
  }
}
