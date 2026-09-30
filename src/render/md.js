// Markdown + KaTeX rendering. Maths is pulled out before Markdown parsing so
// underscores and asterisks inside TeX are never mangled.
import katex from 'katex';
import { marked } from 'marked';

marked.setOptions({ gfm: true, breaks: false });

const cache = new Map();

function tex(src, display) {
  try {
    return katex.renderToString(src, { displayMode: display, throwOnError: false, strict: 'ignore', output: 'html' });
  } catch (e) {
    return `<code>${src}</code>`;
  }
}

function extractMath(s) {
  const store = [];
  const put = html => `@@M${store.push(html) - 1}@@`;
  // $$…$$ display, then \[…\], then $…$ inline (not escaped \$).
  s = s.replace(/\$\$([\s\S]+?)\$\$/g, (_, m) => put(tex(m.trim(), true)));
  s = s.replace(/\\\[([\s\S]+?)\\\]/g, (_, m) => put(tex(m.trim(), true)));
  s = s.replace(/(^|[^\\])\$([^$\n]+?)\$/g, (_, pre, m) => pre + put(tex(m, false)));
  s = s.replace(/\\\$/g, '$');
  return { s, store };
}

const restore = (html, store) => html.replace(/@@M(\d+)@@/g, (_, i) => store[+i]);

const CALLOUT = /^<blockquote>\s*<p><strong>(Trap|Tip|Key idea|Note|Warning|Exam tip):?<\/strong>:?/i;

export function md(src, { inline = false } = {}) {
  if (src == null) return '';
  const key = (inline ? 'i:' : 'b:') + src;
  if (cache.has(key)) return cache.get(key);
  const { s, store } = extractMath(String(src));
  let html = inline ? marked.parseInline(s) : marked.parse(s);
  // Coloured callouts for "> **Trap:** …" style blockquotes.
  html = html.replace(/<blockquote>[\s\S]*?<\/blockquote>/g, block => {
    const m = block.match(CALLOUT);
    if (!m) return block;
    const kind = m[1].toLowerCase().replace(/\s+/g, '-');
    return block.replace('<blockquote>', `<blockquote class="callout callout-${kind}">`);
  });
  html = restore(html, store);
  if (cache.size > 3000) cache.clear();
  cache.set(key, html);
  return html;
}

export const mdi = src => md(src, { inline: true });
export const texi = s => tex(s, false);
