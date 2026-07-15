import { marked } from 'marked'
import katex from 'katex'
import 'katex/dist/katex.min.css'

marked.setOptions({ breaks: true, gfm: true })

const mathStore = []
const PLACEHOLDER = (i) => `@@MATH${i}@@`

function renderMath(tex, display) {
  try {
    return katex.renderToString(tex, { displayMode: display, throwOnError: false, output: 'html' })
  } catch {
    return tex
  }
}

function preProcess(text) {
  mathStore.length = 0
  let out = String(text)
  // Display math $$...$$ first (multiline allowed)
  out = out.replace(/\$\$([\s\S]+?)\$\$/g, (_, tex) => {
    mathStore.push(renderMath(tex.trim(), true))
    return PLACEHOLDER(mathStore.length - 1)
  })
  // Inline math $...$  (no newline inside)
  out = out.replace(/\$([^\$\n]+?)\$/g, (_, tex) => {
    mathStore.push(renderMath(tex.trim(), false))
    return PLACEHOLDER(mathStore.length - 1)
  })
  // Escaped \$ literal dollar sign
  out = out.replace(/\\\$/g, '$')
  return out
}

function postProcess(html) {
  return html.replace(/@@MATH(\d+)@@/g, (_, i) => mathStore[+i] || '')
}

export function renderMarkdown(text) {
  if (!text) return ''
  const pre = preProcess(text)
  const html = marked.parse(pre)
  return postProcess(html)
}

export function stripMarkdown(text) {
  if (!text) return ''
  let s = String(text)
  s = s.replace(/\$\$([\s\S]+?)\$\$/g, ' ')
  s = s.replace(/\$([^\$\n]+?)\$/g, ' ')
  s = s.replace(/^#{1,6}\s+/gm, '')
  s = s.replace(/\*\*([^*]+)\*\*/g, '$1')
  s = s.replace(/`([^`]+)`/g, '$1')
  s = s.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
  s = s.replace(/\n+/g, ' ').replace(/\s+/g, ' ').trim()
  return s
}
